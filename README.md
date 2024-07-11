# pocsuite

## goClient为客户端 用于 Comal引用

- ExecPythonSerialize 用于执行poc
- CheckPythonSerialize 用于入库前校验poc
- HealthCheck 用于新建rpc客户端时验证是否能连接rpc服务端
## pyServer为服务端 用于 执行poc

## 相关文件生成

### 生成go与py pb
```bash
# 安装python依赖库 (当前路径)
python3 -m pip install grpcio-tools -i https://pypi.douban.com/simple
python3 -m pip install -r requirements.txt -i https://pypi.douban.com/simple

# 老版protoc生成 pb (当前路径)
protoc -I. --python_out=./pyServer --grpc_python_out=./pyServer --go_out=plugins=grpc:./goClient ./rpcPoc.proto

# 新版protoc生成go pb (当前路径)
protoc --go_out=./goClient --go-grpc_out=./goClient ./rpcPoc.proto
# 新版protoc生成py pb (当前路径)
python -m grpc_tools.protoc -I. --python_out=./pyServer --grpc_python_out=./pyServer  ./rpcPoc.proto
```
### 生成tls双向认证证书
- 如果重新生成需要手动写到gpClient和pyServer的config文件中
```bash
# 参考
http://liuqh.icu/2022/02/23/go/rpc/06-tls/

# 生成CA私钥
openssl genrsa -out ca.key 4096
# 生成CA证书
openssl req -new -x509 -days 365 -subj "/C=GB/L=Beijing/O=github/CN=huaun" -key ca.key -out ca.crt -config ca.conf

# 服务端
# 生成公私钥
openssl genrsa -out server.key 2048
# 生成CSR
openssl req -new  -subj "/C=GB/L=Beijing/O=github/CN=huaun" -key server.key -out server.csr -config server.conf
# 基于CA签发证书
openssl x509 -req -sha256 -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 -in server.csr -out server.crt -extensions req_ext -extfile server.conf

# 客户端
# 生成公私钥
openssl genrsa -out client.key 2048
# 生成CSR
openssl req -new -subj "/C=GB/L=Beijing/O=github/CN=huaun" -key client.key -out client.csr
# 基于CA签发证书
openssl x509 -req -sha256 -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 -in client.csr -out client.crt
```


# Docker
```bash
# 镜像 harbor.huaun.com:11443/ai.scan/vul-pocsuite:0.0.0 为基础镜像 根目录下python/bin/pyhton 安装了requirements.txt中包含的依赖库

# 打包命令 (当前路径)
docker build --no-cache -t harbor.huaun.com:11443/ai.scan/vul-pocsuite:* .
# 上传命令 (当前路径)
docker push harbor.huaun.com:11443/ai.scan/vul-pocsuite:*