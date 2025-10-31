from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
addr = ('192.168.0.189', 12345)

sock.sendto('안녕하세요 저는 윤재성입니다'.encode('utf-8'), addr)
data, _ = sock.recvfrom(1024)
print(data.decode('utf-8'))