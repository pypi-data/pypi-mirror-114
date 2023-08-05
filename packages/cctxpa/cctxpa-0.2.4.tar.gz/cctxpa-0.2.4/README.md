[![](https://shields.io/pypi/v/cctxpa)](https://pypi.org/project/cctxpa/)

# Pcap-analyser

> This repository concerns only on extracting features from pcap files.
>
> The code which is used to pull feed and save them into database is in another repository.
>
> Please checkout support-email-extractor brunch which can be used to test. The master brunch is used for front-end and isn't completed.

## Getting Started 使用指南

### Prerequisites

```
python 3.8.6
```

### Usage

- install from pip

```sh
pip install cctxpa
```

- usage

```sh
usage: cctxpa [-h] [--host HOST] [--port PORT] [--https] [--register] [--path PATH] [--progress] -u USERNAME -p PASSWORD [-f PCAPFILE] [-o OUTPUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           CCTX pcap analyser server addresss
  --port PORT           CCTX pcap analyser server port
  --https               Use https or http
  --register            Just do register account
  --path PATH           CCTX pcap analyser server login path
  --progress            Print progress, if open, maybe lead slow extract speed.
  -u USERNAME, --username USERNAME
                        Username
  -p PASSWORD, --password PASSWORD
                        Password
  -f PCAPFILE, --pcapfile PCAPFILE
                        Pcap file need to parse!
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        A file to store output report
```

### Usage example 使用示例

- Register account:
    ```shell
    cctxpa -u zoeyyy -p 123456 --register
    ```

- Extract pcap
  > Test pcap files are:  ids1.pcap ftp.pcap ftp2.pcap ftp3.pcap imap.pcap smtp1.pcap pop3.pcap   
  Ids1.pcap file is a public dataset.

    ```sh
    cctxpa -u zoeyyy -p 123456 -f custom.pcap --progress -o report.json
    cctxpa -u zoeyyy -p 123456 -f ids1.pcap --progress -o report.json
    ```

### Report example

![command-tool-print](README.assets/command-tool-print.png)

```json
{
  "totalPacket": 19408,
  "totalIPAddress": 111,
  "totalIPv6Address": 2,
  "totalIPPacket": 19340,
  "totalIPv6Packet": 6,
  "duration": 258.7739198207855,
  "totalTCPFlowNum": 43,
  "totalHTTPNum": 6,
  "totalFTPNum": 0,
  "totalEmailNum": 0,
  "totalFileNum": 3,
  "totalDomainNum": 252,
  "totalMatchIpAddress": 3,
  "totalMatchIpv6Address": 0,
  "totalMatchEmailNum": 0,
  "totalMatchDomain": 5,
  "totalMatchFileHash": 0,
  "totalMatchUri": 0,
  "startTime": 1621386457.158518,
  "endTime": 1621386715.932438,
  "observables": {
    "celerium_10984:observable-d521f93e-9243-3200-ac4d-42758d50edc4": {
      "create_time": 1620875160.0,
      "id": 40195,
      "observableType": "domain",
      "stix_id": "celerium_10984:observable-d521f93e-9243-3200-ac4d-42758d50edc4",
      "value": "kgtwiakkdooplnihvali.com"
    },
    "CSE-CST:observable-eed73196-68c9-39ff-972b-b991e0c3daa0": {
      "create_time": 1576850400.0,
      "id": 71789,
      "observableType": "domain",
      "stix_id": "CSE-CST:observable-eed73196-68c9-39ff-972b-b991e0c3daa0",
      "value": "www.alam-group.com"
    },
    "CCCS:observable-eed73196-68c9-39ff-972b-b991e0c3daa0": {
      "create_time": 1620921960.0,
      "id": 87018,
      "observableType": "domain",
      "stix_id": "CCCS:observable-eed73196-68c9-39ff-972b-b991e0c3daa0",
      "value": "www.alam-group.com"
    },
    "celerium_10984:observable-b50e8ab8-9e8d-370f-8173-19c0dbadd11b": {
      "create_time": 1620875160.0,
      "id": 7624,
      "observableType": "domain",
      "stix_id": "celerium_10984:observable-b50e8ab8-9e8d-370f-8173-19c0dbadd11b",
      "value": "fotoeuropa.ro"
    },
    "CCCS:observable-4afb05d5-a0aa-3621-93e7-18c9a764fc44": {
      "create_time": 1620860760.0,
      "id": 6207,
      "observableType": "address",
      "stix_id": "CCCS:observable-4afb05d5-a0aa-3621-93e7-18c9a764fc44",
      "type": "ipv4-addr",
      "value": "123.57.185.66"
    },
    "celerium_10984:observable-835a3cbf-3114-377d-bcc9-d19cbf703ae3": {
      "create_time": 1620997560.0,
      "id": 14687,
      "observableType": "address",
      "stix_id": "celerium_10984:observable-835a3cbf-3114-377d-bcc9-d19cbf703ae3",
      "type": "ipv4-addr",
      "value": "123.57.185.66"
    }
  },
  "emailRecords": [],
  "fileHashRecords": [],
  "httpRecords": [
    {
      "request": {
        "uri": "/",
        "method": "GET",
        "headers": {
          "host": "fotoeuropa.ro",
          "upgrade-insecure-requests": "1",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "accept-encoding": "gzip, deflate",
          "connection": "keep-alive"
        },
        "version": "1.1",
        "domain": "fotoeuropa.ro",
        "url": "http://fotoeuropa.ro/"
      },
      "response": {
        "status": "301",
        "reason": "Moved Permanently",
        "headers": {
          "connection": "Keep-Alive",
          "keep-alive": "timeout=5, max=100",
          "x-powered-by": "PHP/7.0.33",
          "content-type": "text/html; charset=UTF-8",
          "location": "https://fotoeuropa.mediaro.ro/",
          "cache-control": "public, max-age=0",
          "expires": "Wed, 19 May 2021 01:10:21 GMT",
          "content-length": "0",
          "date": "Wed, 19 May 2021 01:10:21 GMT",
          "server": "LiteSpeed"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableId": "celerium_10984:observable-b50e8ab8-9e8d-370f-8173-19c0dbadd11b",
          "observableType": "domain"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60775,
      "dstIP": "188.213.19.167",
      "dstPort": 80
    },
    {
      "request": {
        "uri": "/",
        "method": "GET",
        "headers": {
          "host": "123.57.185.66",
          "upgrade-insecure-requests": "1",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "accept-encoding": "gzip, deflate",
          "connection": "keep-alive"
        },
        "version": "1.1",
        "domain": "123.57.185.66",
        "url": "http://123.57.185.66/"
      },
      "response": {
        "status": "404",
        "reason": "Not Found",
        "headers": {
          "date": "Wed, 19 May 2021 01:11:20 GMT",
          "content-type": "text/plain",
          "content-length": "0",
          "server": "cloudflare"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableId": "CCCS:observable-4afb05d5-a0aa-3621-93e7-18c9a764fc44",
          "observableType": "ipv4-addr"
        },
        {
          "observableId": "celerium_10984:observable-835a3cbf-3114-377d-bcc9-d19cbf703ae3",
          "observableType": "ipv4-addr"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60926,
      "dstIP": "123.57.185.66",
      "dstPort": 80
    },
    {
      "request": {
        "uri": "/favicon.ico",
        "method": "GET",
        "headers": {
          "host": "123.57.185.66",
          "connection": "keep-alive",
          "accept": "*/*",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "referer": "http://123.57.185.66/",
          "accept-encoding": "gzip, deflate"
        },
        "version": "1.1",
        "domain": "123.57.185.66",
        "url": "http://123.57.185.66/favicon.ico"
      },
      "response": {
        "status": "404",
        "reason": "Not Found",
        "headers": {
          "date": "Wed, 19 May 2021 01:11:20 GMT",
          "content-type": "text/plain",
          "content-length": "0",
          "server": "cloudflare"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableId": "CCCS:observable-4afb05d5-a0aa-3621-93e7-18c9a764fc44",
          "observableType": "ipv4-addr"
        },
        {
          "observableId": "celerium_10984:observable-835a3cbf-3114-377d-bcc9-d19cbf703ae3",
          "observableType": "ipv4-addr"
        },
        {
          "observableId": "CCCS:observable-4afb05d5-a0aa-3621-93e7-18c9a764fc44",
          "observableType": "ipv4-addr"
        },
        {
          "observableId": "celerium_10984:observable-835a3cbf-3114-377d-bcc9-d19cbf703ae3",
          "observableType": "ipv4-addr"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60927,
      "dstIP": "123.57.185.66",
      "dstPort": 80
    }
  ],
  "domainRecords": [
    {
      "domain": "kgtwiakkdooplnihvali.com",
      "domain_type": "A",
      "value": "198.54.117.244",
      "timestamp": 1621386563.829686,
      "observables": [
        {
          "observableId": "celerium_10984:observable-d521f93e-9243-3200-ac4d-42758d50edc4",
          "observableType": "domain"
        }
      ],
      "srcIP": "219.223.223.2",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "kgtwiakkdooplnihvali.com",
      "domain_type": "A",
      "value": "198.54.117.244",
      "timestamp": 1621386564.47294,
      "observables": [
        {
          "observableId": "celerium_10984:observable-d521f93e-9243-3200-ac4d-42758d50edc4",
          "observableType": "domain"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "www.alam-group.com",
      "domain_type": "A",
      "value": "51.75.190.140",
      "timestamp": 1621386613.520531,
      "observables": [
        {
          "observableId": "CSE-CST:observable-eed73196-68c9-39ff-972b-b991e0c3daa0",
          "observableType": "domain"
        },
        {
          "observableId": "CCCS:observable-eed73196-68c9-39ff-972b-b991e0c3daa0",
          "observableType": "domain"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "fotoeuropa.ro",
      "domain_type": "A",
      "value": "188.213.19.167",
      "timestamp": 1621386621.302886,
      "observables": [
        {
          "observableId": "celerium_10984:observable-b50e8ab8-9e8d-370f-8173-19c0dbadd11b",
          "observableType": "domain"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    }
  ]
}
```

### Compile self and upload to PyPI

- Fist, modify `setup.py`

- Second, compile and upload

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Authors 作者

* **Yangyi Zou**

