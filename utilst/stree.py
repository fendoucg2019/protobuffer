#coding=utf-8
from locust import HttpUser, task, between
import time
import socket
import struct
from pbtopythonfile import LoginFunctionProto_pb2

class HeaderInit:
    def __init__(self):
        self.platformType = 0
        self.businessType = 0
        self.subType1 = 0
        self.subType2 = 0
        self.msgID = 0
        self.dataLen = 0
        self.checkFlag = 0
        self.devID = 0
        self.word1 = 0
        self.packetTime = 0

    def AddCheckFlag(self):
        temp=self.packetTime//5000
        self.checkFlag=self.platformType*1+self.businessType*2+self.msgID*3+self.devID*4+temp

class pb_body:
    def pbbody(pbclass,data:dict):
        pb_msg=pbclass(**data)
        return pb_msg

    def pbloginbodyvalue():
        login_data={
        "locno": 103205,
        "strid": "zwp",
        "strpasswd": "123456",
        "ntype": 0
        }
        return login_data

class UserBehavior(HttpUser):
    wait_time = between(5, 10)

    @task
    def login(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('120.76.138.211',19999))
        packetheadervalue=HeaderInit()
        packetheadervalue.platformType=3
        packetheadervalue.businessType=2
        packetheadervalue.msgID=117
        packetheadervalue.devID=103205
        packetheadervalue.packetTime=int(time.time()*1000)
        packetheadervalue.AddCheckFlag()
        login=pb_body.pbbody(LoginFunctionProto_pb2.MsgCsUserLogin,pb_body.pbloginbodyvalue())
        loginpbbodytobytes=login.SerializeToString()
        packetheadervalue.dataLen=len(loginpbbodytobytes)
        headers=struct.pack('>4b5iq',packetheadervalue.platformType,packetheadervalue.businessType,
        packetheadervalue.subType1,packetheadervalue.subType2,packetheadervalue.msgID,packetheadervalue.dataLen,
        packetheadervalue.checkFlag,packetheadervalue.devID,packetheadervalue.word1,packetheadervalue.packetTime)
        s.send(headers+loginpbbodytobytes)
        ser_ret_data=s.recv(1024*12)  #接受服务器返回的数据
        headerdata=ser_ret_data[:32] #切包头
        bodydata=ser_ret_data[32:] #切包体
        ser_ret_databody=LoginFunctionProto_pb2.MsgScGolfjoyUserLoginAck() #实例化
        ser_ret_databody.ParseFromString(bodydata) #解析包体
