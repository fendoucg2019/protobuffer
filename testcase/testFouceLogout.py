#coding=utf-8
from pbtopythonfile import LoginFunctionProto_pb2
from utilst.login_helper import pbMsg


class TestForuceLogouts:
    def setup_method(self):
        self.s = pbMsg.socketConn()
        User = pbMsg.get_yaml_data('User')
        self.strid = User['strid']
        self.locno = User['locno']

    def teardown(self):
        pbMsg.socketClose(self.s)

    def test_ForuceLogout(self):
        Logout={
            'strid':'zz',
            'locno':103205
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(2,105, Logout, LoginFunctionProto_pb2.MsgCsUserLogout)
        bodydata = pbMsg.send_Rec_Msg(None,self.s, headers, loginpbbodytobytes)