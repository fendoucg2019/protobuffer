#coding=utf-8
import yaml

from utilst.login_helper import pbMsg
from pbtopythonfile import LoginFunctionProto_pb2

class Testlogout:
    def setup_method(self):
        with open('../config/values.yaml') as fpva:
            datas=yaml.safe_load(fpva)
            self.strid=datas['ProducUser']['strid']
            self.loc=datas['ProducUser']['strid']
            self.s = pbMsg.socketConn()

    def teardown(self):
        pbMsg.socketClose(self.s)

    def test_logout(self):
        logout_pb={
            'strid':f'{self.strid}',
            'locno':self.loc
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(2,105, logout_pb,LoginFunctionProto_pb2.MsgCsUserLogout)
        pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
        # ser_ret_databody = LoginFunctionProto_pb2.MsgCsUserLogout()
