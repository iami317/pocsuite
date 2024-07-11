import argparse
import json
import logging
import sys
from concurrent import futures

import grpc

import rpcPoc_pb2
import rpcPoc_pb2_grpc

sys.path.append("./lib")
sys.path.append("./config.py")
sys.path.append("./config.ini")

from lib.aesencryption import AesEncryption
from lib.loader import load_string_to_module
from config import Config

aes = AesEncryption("huaun666huaun666")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class CallServicer(rpcPoc_pb2_grpc.CallServicer):
    def ExecPythonSerialize(self, request, context):  # ExecPoc 执行poc
        try:
            poc_str = request.data.decode()
            # pocTest = request.data.decode()
            # poc_str = aes.decrypt(pocTest.strip())  # 对字符串进行解密
            logging.debug(f"Id:{request.id},攻击的目标:{request.addr}:{request.port}")
            if poc_str[0] == "﻿":
                poc_str = poc_str[1:].strip()
            module = load_string_to_module(poc_str)
            result = module.DemoPOC(request.addr, port=request.port)._verify()
            logging.debug(f"Id:{request.id},攻击的目标:{request.addr}:{request.port},结果{result}")
            return rpcPoc_pb2.ResultByte(data=json.dumps(result).encode())
        except Exception as e:
            logging.error(f"Id:{request.id},e:{e}")
            return rpcPoc_pb2.ResultByte(data=f"报错：{e}".encode())

    def CheckPythonSerialize(self, request, context):  # CheckPoc 测试poc
        try:
            poc_str = request.data.decode()
            if poc_str[0] == "﻿":
                poc_str = poc_str[1:].strip()
            module = load_string_to_module(poc_str)
            result = module.DemoPOC("127.0.0.1", port=80)
            re = {"id": result.cveID, "name": result.name, "tags": [result.appName]}
            return rpcPoc_pb2.ResultByte(data=json.dumps(re).encode())
        except Exception as e:
            return rpcPoc_pb2.ResultByte(data=f"报错：{e}".encode())

    def healthCheck(self, request, context):  # 测试连接
        try:
            healthCheck = request.data.decode()
            if "HealthCheck" != healthCheck:
                raise Exception("failed to connect client.")
            return rpcPoc_pb2.ResultByte(data=json.dumps("666").encode())
        except Exception as e:
            return rpcPoc_pb2.ResultByte(data=json.dumps(f"报错：{e}").encode())


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", type=str, help="输入端口")  # 通过 --echo xxx声明的参数，为int类型
    args = parser.parse_args()
    if args.port is None:
        raise "请输入端口"
    # with open('server.key', 'rb') as f:
    private_key = Config.serverKey.encode()
    # with open('server.crt', 'rb') as f:
    certificate_chain = Config.serverCrt.encode()
    # with open('ca.crt', 'rb') as f:
    root_certificates = Config.caCrt.encode()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=500))
    rpcPoc_pb2_grpc.add_CallServicer_to_server(CallServicer(), server)
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),), root_certificates, False)
    server.add_secure_port(f'0.0.0.0:{args.port}', server_credentials)
    server.start()
    print("grpc server start...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
