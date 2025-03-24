# coding=utf-8
import socket
import struct
import time

from pbtopythonfile import LoginFunctionProto_pb2


class HeadersInit:

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
        temp = self.packetTime // 5000
        self.checkFlag = self.platformType * 1 + self.businessType * 2 + self.msgID * 3 + self.devID * 4 + temp


class body:
    def pbfill(pbclass, pbContext: dict):
        pbfullbyte = pbclass(**pbContext)
        return pbfullbyte

    def loginpb():
        loginpbs = {
            'locno': 103205,
            'strid': '109099',
            'strpasswd': '12345678',
            'ntype': 0
        }
        return loginpbs


if __name__=="__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('120.76.138.211', 19999))
    headervalue = HeadersInit()
    headervalue.platformType = 3
    headervalue.businessType = 2
    headervalue.msgID = 117
    headervalue.devID = 103205
    headervalue.packetTime = int(time.time() * 1000)
    headervalue.AddCheckFlag()
    pbbody = body.pbfill(LoginFunctionProto_pb2.MsgCsUserLogin, body.loginpb())
    siralpb = pbbody.SerializeToString()
    headervalue.dataLen = len(siralpb)
    headerspack = struct.pack('>4b5iq', headervalue.platformType, headervalue.businessType, headervalue.subType1,
                              headervalue.subType2, headervalue.msgID,
                              headervalue.dataLen, headervalue.checkFlag, headervalue.devID, headervalue.word1,
                              headervalue.packetTime)
    s.send(headerspack + siralpb)
    recmsg = s.recv(1024 * 12)
    # headerdata = recmsg[:32]
    msgbody = recmsg[32:]
    Ackmsg = LoginFunctionProto_pb2.MsgScPlayerLoginCommonAck()
    Ackmsg.ParseFromString(msgbody)
    print('mobile is:', Ackmsg)
