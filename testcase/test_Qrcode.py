#coding=utf-8

from pbtopythonfile import LoginFunctionProto_pb2
from utilst.login_helper import pbMsg


class TestcsGetQrcode:
    def setup(self):
        self.s = pbMsg.socketConn(None)
        User = pbMsg.get_yaml_data('User')
        self.strid = User['strid']
        self.locno = User['locno']
        self.pswd = User['pswod']

    def testQrcode(self):
        qrcode_pb={
            'ntype':1,
            'locno':self.locno
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(2, 107, qrcode_pb,
                                                                 LoginFunctionProto_pb2.MsgCsGetQrcode)
        bodydata = pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
        ser_ret_databody = LoginFunctionProto_pb2.MsgScGetQrcodeAck()
        ser_ret_databody.ParseFromString(bodydata)
        # print('ntype is:', ser_ret_databody.ntype)
        print('qrcodeaddr is:', ser_ret_databody.qrcodeaddr)