package pocsuite

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"time"
)

type RpcPocClient struct {
	client         CallClient
	ctx            context.Context
	clientDeadline time.Duration
}

func NewRpcPocClient(target string, clientDeadline time.Duration) (*RpcPocClient, error) {
	var conn *grpc.ClientConn

	//cert, err := tls.LoadX509KeyPair("client.crt", "client.key")
	cert, err := tls.X509KeyPair(clientCrt, clientKey)

	if err != nil {
		panic(err)
	}

	certPool := x509.NewCertPool()
	//rootBuf, err := ioutil.ReadFile("ca.crt")
	rootBuf := caCrt
	if err != nil {
		panic(err)
	}
	if !certPool.AppendCertsFromPEM(rootBuf) {
		panic("Fail to append ca")
	}
	creds := credentials.NewTLS(&tls.Config{
		Certificates: []tls.Certificate{cert},
		ServerName:   "huaun",
		RootCAs:      certPool,
	})

	conn, err = grpc.Dial(target, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, err
	}
	c := &RpcPocClient{NewCallClient(conn), context.Background(), clientDeadline}
	_, err = c.HealthCheck()
	if err != nil {
		return nil, err
	}
	return c, nil
}

// ExecPythonSerialize 执行加密poc
func (t *RpcPocClient) ExecPythonSerialize(addr string, port string, id string, data []byte) (*[]byte, error) {
	ctx, cancel := context.WithTimeout(t.ctx, t.clientDeadline*time.Second)
	defer cancel()
	response, err := t.client.ExecPythonSerialize(ctx, &ExecPythonSerializeRequest{Data: data, Port: port, Addr: addr, Id: id})
	if err != nil {
		return nil, err
	}
	return &response.Data, nil
}

// CheckPythonSerialize 校验poc
func (t *RpcPocClient) CheckPythonSerialize(data []byte) (*[]byte, error) {
	response, err := t.client.CheckPythonSerialize(context.Background(), &ExecPythonSerializeRequest{Data: data})
	if err != nil {
		return nil, err
	}
	return &response.Data, nil
}

// HealthCheck 检测服务端
func (t *RpcPocClient) HealthCheck() (bool, error) {
	response, err := t.client.HealthCheck(context.Background(), &ResultByte{Data: []byte("HealthCheck")})
	if err != nil {
		return false, err
	}
	var result interface{}
	err = json.Unmarshal(response.Data, &result)
	if err != nil {
		return false, err
	}
	if result != "666" {
		return false, fmt.Errorf("failed to connect server")
	}
	return true, nil
}
