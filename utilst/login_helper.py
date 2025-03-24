#coding=utf-8
from datetime import datetime
import struct
import time
import yaml
from pbtopythonfile import LoginFunctionProto_pb2
from utilst.header_init import HeaderInit
from utilst.pb_body import pb_bodys
import socket
class pbMsg:
    def get_yaml_data(key):
        with open('../config/values.yaml', 'r') as f:
            data = yaml.safe_load(f)
        return data.get(key)
    def socketConn(server):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vals=pbMsg.get_yaml_data('socketinfo')
        s.connect((vals[f'{server}'], vals['socket_port']))
        return s
    def socketClose(s):
        s.close()

    def create_login_request(locno, buisinesstype, msgID, pbbodys, pbclass):
        packetheadervalue = HeaderInit()
        packetheadervalue.platformType = 3
        packetheadervalue.businessType = buisinesstype
        packetheadervalue.msgID = msgID
        packetheadervalue.devID = locno  # 103205
        packetheadervalue.packetTime = int(time.time() * 1000)
        packetheadervalue.AddCheckFlag()
        login = pb_bodys.pbbody(pbclass, pbbodys)
        loginpbbodytobytes = login.SerializeToString()
        packetheadervalue.dataLen = len(loginpbbodytobytes)
        print('包体长度', len(loginpbbodytobytes))
        headers = struct.pack('>4b5iq', packetheadervalue.platformType, packetheadervalue.businessType,
                              packetheadervalue.subType1, packetheadervalue.subType2, packetheadervalue.msgID,
                              packetheadervalue.dataLen,
                              packetheadervalue.checkFlag, packetheadervalue.devID, packetheadervalue.word1,
                              packetheadervalue.packetTime)
        return headers, loginpbbodytobytes

    def send_Rec_Msg(self,s,headers,loginpbbodytobytes):
        starTime=datetime.now()
        print('登录请求时间：',starTime)
        s.send(headers+loginpbbodytobytes)
        ServerRetData=s.recv(1024*12)
        endTime=datetime.now()
        print('登录结束时间：',endTime)
        bodydata=ServerRetData[32:]
        return bodydata,starTime,endTime

    def ParseMsg(self,RetMsg,bodydata):
        RetMsg.ParseFromString(bodydata)
        return RetMsg
