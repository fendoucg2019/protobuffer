#coding=utf-8
import yaml
from pbtopythonfile import LoginFunctionProto_pb2
from utilst.login_helper import pbMsg


class TestUserLogout:
    def setup(self):
        self.s = pbMsg.socketConn(None)
    def teardown(self):
        pass
    def testUserCheck(self):
        UserCheck={
            'locno': 103205,
            'strid':['zwp',],
            'status': -1,
            'branch': 10220,
            'strVersion': '1.9.6.0'
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(2,115, UserCheck,LoginFunctionProto_pb2.MsgCsLoginUsersCheck)
        bodydata = pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
        ser_ret_databody = LoginFunctionProto_pb2.MsgScLoginUsersCheckAck()
        ser_ret_databody.ParseFromString(bodydata)
        print('mobile is:', ser_ret_databody.strid)