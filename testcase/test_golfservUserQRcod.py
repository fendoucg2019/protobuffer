#coding=utf-8

from pbtopythonfile import golfjoyServerProto_pb2
from utilst.login_helper import  pbMsg

class TestgetFunctionlist:
    def setup(self):
        self.s = pbMsg.socketConn(None)
        # User = pbMsg.get_yaml_data('User')
        # self.strid = User['strid']
        # self.locno = User['locno']
    def teardown(self):
        pbMsg.socketClose(self.s)
    def testFunctionlist(self):
        getfunctionbpb={
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(7, 300,getfunctionbpb,
                                                                 golfjoyServerProto_pb2.MsgGetFunctionLicenseAuthReq)
        bodydata = pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
        ser_ret_databody = golfjoyServerProto_pb2.MsgGetFunctionLicenseAuthRsp()
        ser_ret_databody.ParseFromString(bodydata)
        print('errorcode is:',ser_ret_databody.error_desc)