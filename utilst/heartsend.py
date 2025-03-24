#coding=utf-8
#coding=utf-8
import socket
import struct
import time
import threading
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
    @staticmethod
    def pbbody(pbclass,data:dict):
        pb_msg=pbclass(**data)
        return pb_msg

    @staticmethod
    def pbloginbodyvalue():
        login_data={
        "locno": 103205,
        "strid": "zwp",
        "strpasswd": "123456",
        "ntype": 0
        }
        return login_data

    @staticmethod
    def pbloginUserCheck():
        userCheck={
        'locno':103205,
        'strid':[],
        'status':-1,
        'branch':0,
        'strVersion':'1.9.6.0'
        }
        return userCheck

def send_heartbeat(socket, packetheadervalue):
    while True:
        # 创建一个空的protobuf消息
        heartbeat = LoginFunctionProto_pb2.MsgCsUserLogin()
        # 序列化消息
        heartbeat_bytes = heartbeat.SerializeToString()
        # 创建包头
        header = struct.pack('>4b5iq',packetheadervalue.platformType,packetheadervalue.businessType,
        packetheadervalue.subType1,packetheadervalue.subType2,packetheadervalue.msgID,len(heartbeat_bytes),
        packetheadervalue.checkFlag,packetheadervalue.devID,packetheadervalue.word1,packetheadervalue.packetTime)
        # 发送心跳
        socket.send(header + heartbeat_bytes)
        # 等待一段时间
        time.sleep(5)

if __name__=="__main__":
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('120.76.138.211',19999))
    packetheadervalue=HeaderInit()
    packetheadervalue.platformType=3
    packetheadervalue.businessType=2
    packetheadervalue.msgID=117
    packetheadervalue.devID=103205
    packetheadervalue.packetTime=int(time.time()*1000)
    packetheadervalue.AddCheckFlag()
    #用户登录
    login=pb_body.pbbody(LoginFunctionProto_pb2.MsgCsUserLogin,pb_body.pbloginbodyvalue())
    loginpbbodytobytes=login.SerializeToString()
    packetheadervalue.dataLen=len(loginpbbodytobytes)
    headers=struct.pack('>4b5iq',packetheadervalue.platformType,packetheadervalue.businessType,
    packetheadervalue.subType1,packetheadervalue.subType2,packetheadervalue.msgID,packetheadervalue.dataLen,
    packetheadervalue.checkFlag,packetheadervalue.devID,packetheadervalue.word1,packetheadervalue.packetTime)
    s.send(headers+loginpbbodytobytes)
    # 开启心跳线程
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(s, packetheadervalue))
    heartbeat_thread.start()
    ser_ret_data=s.recv(1024*12)  #接受服务器返回的数据
    headerdata=ser_ret_data[:32] #切包头
    bodydata=ser_ret_data[32:] #切包体
    ser_ret_databody=LoginFunctionProto_pb2.MsgScGolfjoyUserLoginAck() #实例化
    ser_ret_databody.ParseFromString(bodydata) #解析包体
    #下面是将包体打印出来
    print("ret:", ser_ret_databody.ret)
    print("sex:", ser_ret_databody.sex)
    print("error_code:", ser_ret_databody.error_code)
    # print("mobile:", ser_ret_databody.mobile)
