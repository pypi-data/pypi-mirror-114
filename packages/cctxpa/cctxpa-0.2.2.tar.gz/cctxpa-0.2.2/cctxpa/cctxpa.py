import argparse
import datetime
import json
import os
import sys
import dpkt
import requests

from .pcap_extractor.MyEncoder import MyEncoder
from .pcap_extractor.FlowExtractor import FlowExtractor
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.mail import Mail
from .pcap_extractor.HTTPParser import HTTPParser, HttpData
from .pcap_extractor.SMTPParser import SMTPParser
from .pcap_extractor.POP3Parser import POP3Parser
from .pcap_extractor.IMAPParser import IMAPParser
from .pcap_extractor.DNSExtractor import DNSExtractor, DNSItem
from .report import Report, FileHash
from progress.bar import Bar
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.columns import Columns
from rich.panel import Panel


class CCTXPcapAnalyser:
    def __init__(self, args):
        self.host = args.host                   # cctx-pcap-analyser 服务器地址（可以是ip或者域名，默认是 127.0.0.1）
        self.path = args.path                   # cctx-pcap-analyser server 的API相对路径
        self.port = args.port                   # cctx-pcap-analyser server 的端口，默认为 5000
        self.https = args.https                 # 是否使用 https，默认为 True
        self.username = args.username           # 用来登录或者注册 cctx-pcap-analyser server 的用户名
        self.password = args.password           # 用来登录或者注册 cctx-pcap-analyser server 的密码
        self.inputFile = args.pcapfile          # 要解析的 pcap 文件
        self.outputFile = args.outputfile       # 指定输出的 json 格式的report的名字，默认为 report.json
        self.progress = args.progress           # 是否输出提取进度条，默认为 True
        if self.port == -1:
            # 不指定端口，使用默认的80或者443
            if self.https:
                self.port = 443
            else:
                self.port = 80

        # 实例化一个 FlowExtractor，用来从 pcap 文件里面提取一个个 TCP 流
        # 并且每提取到一个 TCP 流，就会调用 self.dealStream 这个回调来处理它
        self.flowExtractor = FlowExtractor(valueCallback=self.dealStream)

        # 实例化一个 DNSExtractor，用来从 pcap 文件里面提取 DNS 查询记录
        # 并且每提取到一个 DNS 查询记录，就会调用 self.dealDNSRecord 这个回调来处理它
        self.dnsExtractor = DNSExtractor(valueCallback=self.dealDNSRecord)

        # 初始化一系列的 Parser，用来从 TCP 流量中解析应用层的数据（包括 HTTP 请求回复，和三种邮件协议的解析）
        self.httpParser = HTTPParser()
        self.smtpParser = SMTPParser()
        self.pop3Parser = POP3Parser()
        self.imapParser = IMAPParser()

        # 实例化 Report，提取过程中的相关记录都会存到该对象中
        self.report = Report()
        self.report.pcapFile = args.pcapfile
        self.report.outputCsvDir = args.outputcsvdirectory

        # 根据传入的参数构造出几个 URL
        # 用来注册的接口的URL => http://127.0.0.1:5000/user/register
        # 用来登录的接口的URL => http://127.0.0.1:5000/user/login
        # 用来查询 Observable 的接口的URL => http://127.0.0.1:5000/user/queryObservables
        self.url = f'{"https" if self.https else "http"}://{self.host}:{self.port}{self.path}'
        self.registerUrl = f'{self.url}/user/register'
        self.loginUrl = f'{self.url}/user/login'
        self.queryUrl = f'{self.url}/user/queryObservables'

        # 用来保存登录时返回的 token，因为查询 Observable 的接口需要登录后携带 token 才能请求
        self.token = ""
        # 用来保存 refreshToken （暂时没用到）
        # refreshToken 的有效时间一般比 token 长很多，当 token 过期时，可以使用 refreshToken 来申请更新 token
        self.refreshToken = ""

        self.report.begin()

        # 一个字典，用来缓存查询结果（主要用来查询加速）
        # {
        #   "google.com": {
        #                       "observables": []
        #                 },
        #   "217.31.42.56": {
        #                        "observables": []
        #                  },
        # }
        #
        # 1. 比如之前查询过 "abv.com" 这个域名，服务器返回 observables 为空表示没有 observable 和 这个域名匹配，使用 queryCache 保存
        #    这个结果，那么下一次再次查询这个域名的时候，直接从 queryCache 中就能查询到为空，不需要向服务器发起请求了，可以起到查询加速的目的。
        self.queryCache = {

        }

    def doAuthGet(self, url: str, params: dict):
        """
        携带 Token 发起一个 Get请求
        1. 因为有些 API 接口需要登录之后携带token才能访问
        :param url:
        :param params:
        :return:
        """
        r = requests.get(url, params=params, headers={
            "Authorization": f"Bearer {self.token}"         # 在请求头中携带 token
        })
        # print(r.json())
        if r.status_code == 401:
            # 如果权限验证过期，则表示token失效了，只要重新登录刷新token，并再次尝试发起刚才失败的请求即可
            # 通过这种方式，即便 token 的有效期很短，使用命令行工具的用户也感觉不到
            self.doLogin()
            return self.doAuthGet(url, params)
        elif r.status_code != 200:
            return {
                "code": 500,
                "msg": r.reason,
                "data": ""
            }
        responseData = r.json()
        return responseData

    def doAuthPost(self, url: str, jsonData: dict):
        """
        携带 Token 发起一个 post 请求
        1. 因为有些 API 接口需要登录之后携带token才能访问
        :param url:
        :param jsonData:
        :return:
        """
        r = requests.post(url, json=jsonData, headers={
            "Authorization": f"Bearer {self.token}"  # 在请求头中携带 token
        })
        responseData = r.json()
        if responseData == 401:
            # 如果权限验证过期，则表示token失效了，只要重新登录刷新token，并再次尝试发起刚才失败的请求即可
            # 通过这种方式，即便 token 的有效期很短，使用命令行工具的用户也感觉不到
            self.doLogin()
            return self.doAuthPost(url, jsonData)
        return responseData

    @staticmethod
    def buildQueryDomain(domain: str) -> dict:
        """
        构造一个查询 Domain 表的子任务
        :param domain:
        :return:
        """
        return {
            'queryType': 'domain',
            'value': domain
        }

    @staticmethod
    def buildQueryAddress(address: str) -> dict:
        """
        构造一个查询 Address 表的子任务
        :param address:
        :return:
        """
        return {
            'queryType': 'address',
            'value': address
        }

    @staticmethod
    def buildQueryUri(uri: str) -> dict:
        """
        构造一个查询 URI 表的子任务
        :param uri:
        :return:
        """
        return {
            'queryType': 'uri',
            'value': uri
        }

    @staticmethod
    def buildQueryFileHash(fileHash: FileHash) -> dict:
        """
        构造一个查询 FileHash 表的子任务
        :param fileHash:
        :return:
        """
        return {
            'queryType': 'fileHash',
            'md5': fileHash.md5,
            'sha1': fileHash.sha1,
            'sha256': fileHash.sha256
        }

    def doQuery(self, queryItems: [dict]) -> [dict]:
        """
        执行一组查询任务。执行下列步骤
        1. 遍历每一个查询任务，对每一个查询子任务，检查本地的 queryCache 是否有缓存对应value的结果，
           如果有直接使用，如果没有则将该子任务加到 remainQueryItems 列表当中；
        2. 然后检查 remainQueryItems 是否为空，不为空则向去服务发起一个查询请求；
        3. 然后合并步骤1和步骤2的结果，并返回
        :param queryItems:
                [
                    {
                        "queryType": "address",
                        "value": "192.168.21.45"
                    },
                    {
                        "queryType": "address",
                        "value": "21.3.23.45"
                    },
                    {
                        "queryType": "domain",
                        "value": "asb.com"
                    },
                ]
        :return:
        """
        def getValue(queryItem: dict):
            if queryItem["queryType"] == "fileHash":
                return f'{queryItem["md5"]}-{queryItem["sha1"]}-{queryItem["sha256"]}'
            return queryItem["value"]

        # results => 存储查询对比的结果
        # remainQueryItems => 存储本地缓存没有查到，需要到服务器后台查询的任务
        results, remainQueryItems = [], []
        for queryItem in queryItems:
            value = getValue(queryItem)
            if value in self.queryCache:
                if len(self.queryCache[value]["observables"]) > 0:
                    results.append(self.queryCache[value])
            else:
                remainQueryItems.append(queryItem)

        # 如果所有的查询任务都命中了本地缓存，则直接返回结果就可，不用请求服务器后台
        if len(remainQueryItems) == 0:
            return results

        # 如果还有没有命中缓存的查询任务需要查询，则向服务器后台发送查询请求
        response = self.doAuthGet(self.queryUrl, params={
            'queries': json.dumps(remainQueryItems),
        })
        if response['code'] == 200:
            if response['data'] and len(response['data']) > 0:
                for observable in response['data']:
                    self.queryCache[observable["value"]] = observable
                results += response['data']
        else:
            print(f'Query Observable failed, {response["msg"]}')
        return results

    def dealDNSRecord(self, dnsRecord: DNSItem):
        """
        处理每个提取到的 DNS 解析记录
        :param dnsRecord:
        :return:
        """
        # query DNSItem
        observables = self.doQuery([
            CCTXPcapAnalyser.buildQueryDomain(dnsRecord.domain),
            CCTXPcapAnalyser.buildQueryAddress(dnsRecord.value)
        ])
        self.report.addDNSRecord(dnsRecord, observables)

    def dealMail(self, mail: Mail, tcpFlow: TCPFlow):
        """
        处理每个解析出来的邮件
        :param mail:
        :param tcpFlow:
        :return:
        """
        # query email address, ip address, file hash
        queryTask = [
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
            CCTXPcapAnalyser.buildQueryAddress(mail.From),
            CCTXPcapAnalyser.buildQueryAddress(mail.To),
        ]
        for mailFile in mail.files:
            fileHash = FileHash(mailFile.fileData)
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addEmail(mail, tcpFlow, observables)

    def dealHttpData(self, httpData: HttpData, tcpFlow: TCPFlow):
        """
        处理每个解析出来的 HttpData
        :param httpData:
        :param tcpFlow:
        :return:
        """
        # query url, file hash, ip address, domain
        queryTask = [
            CCTXPcapAnalyser.buildQueryDomain(httpData.getDomain()),
            CCTXPcapAnalyser.buildQueryUri(httpData.getUrl()),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
        ]
        if httpData.fileHashes:
            fileHash = FileHash()
            fileHash.md5 = httpData.fileHashes["md5"]
            fileHash.sha1 = httpData.fileHashes["sha1"]
            fileHash.sha256 = httpData.fileHashes["sha256"]
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addHttp(httpData, tcpFlow, observables)

    def dealFTP(self, data: bytes, tcpFlow: TCPFlow):
        """
        处理每个 FTP
        :param data:
        :param tcpFlow:
        :return:
        """
        fileHash = FileHash(data)
        queryTask = [
            CCTXPcapAnalyser.buildQueryFileHash(fileHash),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP),
        ]
        observables = self.doQuery(queryTask)
        self.report.addFileHash(fileHash, tcpFlow, observables)

    def dealStream(self, tcpFlow: TCPFlow):
        """
        处理每个提取到的TCP流
        :param tcpFlow:
        :return:
        """
        self.report.addTCPFlow(tcpFlow)
        forwardBytes, reverseBytes = tcpFlow.getAllForwardBytes(), tcpFlow.getAllReverseBytes()
        if tcpFlow.dstPort == 21:
            pass
        elif tcpFlow.srcPort == 20 or tcpFlow.dstPort == 20:
            # 处理主动模式 FTP
            data1, data2 = forwardBytes, reverseBytes
            data = data1 if len(data2) == 0 else data2
            if len(data) > 0:
                # md1 = hashlib.md5()
                # md2 = hashlib.md5()
                # md3 = hashlib.md5()
                # with closing(BytesIO(data)) as data:
                #     for line in data.readlines():
                #         md1.update(line)
                #         if line.endswith(b"\r\n"):
                #             md2.update(line[:-2])
                #             md2.update(b'\r')
                #             md3.update(line[:-2])
                #             md3.update(b'\n')
                self.dealFTP(data, tcpFlow)
        elif tcpFlow.dstPort == 143:
            # 处理 IMAP
            for mail in self.imapParser.parse(forwardBytes, reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 110:
            # 处理 POP3
            for mail in self.pop3Parser.parse(reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 25:
            # 处理 SMTP
            for mail in self.smtpParser.parse(forwardBytes):
                self.dealMail(mail, tcpFlow)
        elif (len(forwardBytes) == 0 and len(reverseBytes) > 0) or (len(forwardBytes) > 0 and len(reverseBytes) == 0):
            # 处理被动模式 FTP
            # try to cal file hash for FTP passive mode
            if len(forwardBytes) == 0 and len(reverseBytes) > 0:
                self.dealFTP(reverseBytes, tcpFlow)
            else:
                self.dealFTP(forwardBytes, tcpFlow)
        else:
            # parse http
            for httpData in self.httpParser.parse(forwardBytes, reverseBytes):
                self.dealHttpData(httpData, tcpFlow)

    def doRegister(self):
        """
        执行注册
        :return:
        """
        r = requests.post(self.registerUrl, json={
            'username': self.username,
            'password': self.password
        })
        return r.json()

    def doLogin(self):
        """
        执行登录
        :return:
        """
        r = requests.post(self.loginUrl, json={
            'username': self.username,
            'password': self.password
        })
        # print("Do login")
        try:
            data = r.json()
        except Exception as e:
            print(f"Login failed, {r.reason}")
            return False
        if data['code'] != 200:
            print(f"Login failed, {data['msg']}")
            return False
        self.token = data['data']['token']
        self.refreshToken = data['data']['refresh_token']
        return True

    def start(self):
        """
        Start to parse pcap file
        :return:
        """

        # do login first
        if not self.doLogin():
            return

        # 判断是否要展示进度条
        if self.progress:
            bar = Bar('Extract Progress:', max=100)
        else:
            bar = None

        self.report.begin()
        with open(self.inputFile, 'rb') as pcap:
            progress = 0
            totalSize = os.path.getsize(self.inputFile)
            packets = dpkt.pcap.Reader(pcap)
            for ts, buf in packets:
                if self.progress:
                    currentProgress = int(pcap.tell() * 100 / totalSize)
                    if currentProgress != progress:
                        progress = currentProgress
                        bar.next()
                ethPacket = dpkt.ethernet.Ethernet(buf)
                self.report.addPacket(ethPacket, ts)
                self.flowExtractor.addPacket(ethPacket, ts)
                self.dnsExtractor.addPacket(ethPacket, ts)
        if self.progress:
            bar.finish()
        self.report.end()
        self.flowExtractor.done()


def printReport(report: Report, args):
    """
    将对比报告输出到控制台终端
    :param report:
    :return:
    """

    def getPanelContent(key, value: str = None):
        return Panel(f"[b]{key}[/b]\n[yellow]{getattr(report, key) if value is None else value}", expand=True, width=30)

    console = Console()
    console.print(Markdown("# Analyser Report"))
    durationSeconds = report.endTime - report.startTime
    durationMinutes = durationSeconds / 60
    durationSeconds = durationSeconds % 60
    durationHours = durationMinutes / 60
    durationMinutes = durationMinutes % 60
    fsize = os.path.getsize(args.pcapfile)
    renderAbles = [
                      getPanelContent('input pcap file', args.pcapfile),
                      getPanelContent('detail report', f"{args.pcapfile}-{args.outputfile}"),
                      getPanelContent('startTime',
                                      datetime.datetime.fromtimestamp(report.startTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('endTime',
                                      datetime.datetime.fromtimestamp(report.endTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('duration',
                                      f"{int(durationHours)} h : {int(durationMinutes)} m : {int(durationSeconds)} s"),
                      getPanelContent('fileSize', f"{round(fsize/float(1024*1024), 2)} MB")

                      # getPanelContent('duration', f"{report.endTime - report.startTime}"),
                  ] + [getPanelContent(item) for item in
                       ['totalPacket', 'totalIPAddress', 'totalIPv6Address', 'totalEmailAddress', 'totalIPPacket',
                        'totalIPv6Packet',
                        'totalTCPFlowNum', 'totalHTTPNum', 'totalFTPNum', 'totalEmailNum', 'totalFileNum',
                        'totalDomainNum',
                        'totalMatchIpAddress', 'totalMatchIpv6Address', 'totalMatchEmailNum', 'totalMatchDomain',
                        'totalMatchFileHash', 'totalMatchUri']]
    columns = Columns(renderAbles, equal=True, expand=True)
    console.print(columns)

    console.print(Markdown("## CCTX Observable Match Results"))
    table = Table(expand=True)
    table.add_column("Extracted Feature", justify='center', style='cyan')
    table.add_column("Extracted Feature Count", justify='center', style='cyan')
    table.add_column("Matched Observable Count", justify='center', style='magenta')
    table.add_column("Matching Percentage", justify='center', style='green')
    table.add_row('IPv4 address', f"{report.totalIPAddress}", f"{report.totalMatchIpAddress}",
                  f"{0 if report.totalIPAddress == 0 else round(report.totalMatchIpAddress * 100.0 / report.totalIPAddress, 2)}%")
    table.add_row("IPv6 address", f"{report.totalIPv6Address}", f"{report.totalMatchIpv6Address}",
                  f"{0 if report.totalIPv6Address == 0 else round(report.totalMatchIpv6Address * 100.0 / report.totalIPv6Address, 2)}%")
    table.add_row("Email address", f"{report.totalEmailAddress}", f"{report.totalMatchEmailNum}",
                  f"{0 if report.totalEmailNum == 0 else round(report.totalMatchEmailNum * 100.0 / report.totalEmailNum, 2)}%")
    table.add_row("Domain", f"{report.totalDomainNum}", f"{report.totalMatchDomain}",
                  f"{0 if report.totalDomainNum == 0 else round(report.totalMatchDomain * 100.0 / report.totalDomainNum, 2)}%")
    table.add_row("Uri", f"{report.totalHTTPNum}", f"{report.totalMatchUri}",
                  f"{0 if report.totalHTTPNum == 0 else round(report.totalMatchUri * 100.0 / report.totalHTTPNum, 2)}%")
    table.add_row("File hash", f"{report.totalFileNum}", f"{report.totalMatchFileHash}",
                  f"{0 if report.totalFileNum == 0 else round(report.totalMatchFileHash * 100.0 / report.totalFileNum, 2)}%")
    console.print(table)


def main():
    """
    cctxpa is a command lien tool for CCTX to parse pcap file and compare with CCTX's Observables
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="127.0.0.1", help="CCTX pcap analyser server addresss")
    parser.add_argument('--port', type=int, default=5000, help="CCTX pcap analyser server port")
    parser.add_argument('--https', action='store_true', help="Use https or http")
    parser.add_argument('--register', action='store_true', help="Just do register account")
    parser.add_argument('--path', type=str, default="", help="CCTX pcap analyser server login path")
    parser.add_argument('--progress', action='store_true',
                        help="Print progress, if open, maybe lead slow extract speed.")
    parser.add_argument('-u', '--username', type=str, required=True, help="Username")
    parser.add_argument('-p', '--password', type=str, required=True, help="Password")
    parser.add_argument('-f', '--pcapfile', type=str, default='test.pcap', help="Pcap file need to parse!")
    parser.add_argument('-o', '--outputfile', type=str, default="report.json", help="A file to store output report")
    parser.add_argument('-ocd', '--outputcsvdirectory', type=str, default='outputcsv',
                        help="A directory to store output csv file")
    args = parser.parse_args()

    cctxpa = CCTXPcapAnalyser(args)
    if args.register:
        # do register
        print(cctxpa.doRegister())
    else:
        begin = datetime.datetime.now().timestamp()
        cctxpa.start()
        with open(f"{args.pcapfile}-{args.outputfile}", 'w') as file:
            file.write(json.dumps(cctxpa.report.toDict(), ensure_ascii=False, cls=MyEncoder))
        printReport(cctxpa.report, args)
        print("Duration: ", datetime.datetime.now().timestamp() - begin)


if __name__ == '__main__':
    main()
