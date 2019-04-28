# coding = utf-8

'''
httpserver V3.0 第三版！！！
httpserver + WebFrame(网页框架)
'''
from socket import *
import sys
from threading import Thread
from settings import * #导入配置文件
import re
import time

#和WebFrame(网页框架)通信
def connect_frame(METHOD, PATH_INFO):
    s = socket()
    try:
        s.connect(frame_address) #连接框架服务器地址
    except Exception as e:
        print('Connect error(连接错误)',e)
        return
    s.send(METHOD.encode())
    time.sleep(0.1)
    s.send(PATH_INFO.encode())
    response = s.recv(4096).decode()
    if not response:
        response = '404'
    s.close()
    return response


#封装httpserver类
class Httpserver(object):
    def __init__(self, address):
        self.address = address
        self.create_socket()
        self.bind(address)
    #创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #绑定地址
    def bind(self, address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)

    def server_forvever(self):
        self.sockfd.listen(5)
        print('listen the port %d' %self.port)
        while True:
            try:
                connfd, addr = self.sockfd.accept( )
            except KeyboardInterrupt:
                self.sockfd.close( )
                sys.exit('服务器退出')
            except Exception as e:
                print('Error',e)
                continue
            print('connect from',addr)
            # print('333333333333333333333333')
            #用Thread【创建线程】处理客户端请求
            handle_client = Thread(target=self.handle,args=(connfd,))
            handle_client.setDaemon(True)  # 主线程退出，其他线程也跟随退出
            handle_client.start( )

    #处理具体的客户端请求
    def handle(self, connfd):
        #接收浏览器发来的http请求
        request = connfd.recv(4096)
        # print(request)
        if not request:
            connfd.close()
            return
        # print(request.decode())
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode('utf-8')
        print(request_line)
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict()
            print(env)
        except:
            response_headers = 'HTTP/1.1 500 SERVER ERROR\r\n'
            response_headers += '\r\n'
            response_body = "server Error"
            response = response_headers + response_body
            connfd.send(response.encode())
            connfd.close()
            return

        response = connect_frame(**env)
        print(response)

        if response == '404':
            response_headers = 'HTTP/1.1 404 not found\r\n'
            response_headers += '\r\n'
            response_body = "----sorry!!!-----"
        else:
            response_headers = 'HTTP/1.1 200 OK\r\n'
            response_headers += '\r\n'
            response_body = response
        response = response_headers + response_body
        connfd.send(response.encode())
        connfd.close()




if __name__ == "__main__":
    httpd = Httpserver(ADDR)
    httpd.server_forvever() #启动HTTP服务