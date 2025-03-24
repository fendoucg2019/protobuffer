#coding=utf-8
import socket

class Conn:
    def socketConn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('120.76.138.211', 19999))
        return s
    def socketClose(s):
        s.close()