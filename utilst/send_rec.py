#coding=utf-8

class Send_Rec:
    def send_Rec_Msg(self,s,headers,loginpbbodytobytes):
        s.send(headers+loginpbbodytobytes)
        ServerRetData=s.recv(1024*12)
        bodydata=ServerRetData[32:]
        return bodydata

    def ParseMsg(self,RetMsg,bodydata):
        RetMsg.ParseFromString(bodydata)
        return RetMsg
