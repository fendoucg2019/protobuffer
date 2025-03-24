#coding=utf-8
from utilst.login_helper import pbMsg
from pbtopythonfile import LicenseServerProto_pb2
class TestLicenseOnlineFirstReq:
    def setup(self):
        self.s=pbMsg.socketConn(None)

    def teardown(self):
        pbMsg.socketClose(self.s)

    def testLicenseOnlineFirstReq(self):
        '''
        long sum = 0;
        int i = 0;
        for(i = 0; i < 9; i++){
            sum += aKeyList.get(i)/20;
        }
        /*a_key前十校验和算法*/
        sum += (nType /5 + nGameType / 3);
        sum += (aKeyList.get(0)/7
                + aKeyList.get(1)/6
                + aKeyList.get(3)/6
                + aKeyList.get(8)/8);

        上面为register_data的算法
        :return:
        '''
        LicenseOnLineFirstReqdata={
            'type':2100,
            'game_type':202,
            'register_data':[103205,351039305,200000,600000,400000,100000,120000,180000,400000,76328905],
            'addr':'B4-96-91-A0-40-23',
            'bInternational':0,
            'demo_version':1,
            'demo_version':1709827199
        }
        headers, loginpbbodytobytes = pbMsg.create_login_request(3, 100, LicenseOnLineFirstReqdata,
                                                                 LicenseServerProto_pb2.MsgLicenseOnlineFirstReq)
        bodydata = pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
        ser_ret_databody = LicenseServerProto_pb2.MsgLicenseOnlineFirstAck()
        ser_ret_databody.ParseFromString(bodydata)
        print('branch_no:',ser_ret_databody.ok)