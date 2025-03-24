# coding=utf-8
import pytest
from utilst.login_helper import pbMsg
from pbtopythonfile import LoginFunctionProto_pb2


# @pytest.mark.parametrize(
#     'serveraddr, serveruser',
#     [
#         ('produc_server_ip', 'ProducUser'),
#         ('America_socket', 'AmericaUser'),
#         ('Europe_socket', 'EuropeUser')
#     ]
# )
class TestLogin:

    def setup_method(self):
        # sever_set=['produc_server_ip','America_socket','Europe_socket']
        sever_set=['produc_server_ip']
        for i in range(len(sever_set)):
            self.s = pbMsg.socketConn(f'{sever_set[i]}')
            if sever_set[i]=='produc_server_ip':
                User = pbMsg.get_yaml_data('ProducUser')
            elif sever_set[i]=='America_socket':
                User = pbMsg.get_yaml_data('AmericaUser')
            else:
                User = pbMsg.get_yaml_data('EuropeUser')
            self.strid = User['strid']
            self.locno = User['locno']
            self.pswd = User['pswod']
            self.nickname = User['nickname']
            print("Setup: Successfully established socket connection and initialized user data.")

    def teardown_method(self):
        pbMsg.socketClose(self.s)
        print("Teardown: Socket connection closed successfully.")

    @pytest.mark.run(order=1)
    # @pytest.mark.parametrize('serveraddr,serveruser',[('produc_server_ip','ProducUser'),('America_socket','AmericaUser')])
    def test_login(self):
        try:
            print('执行用例1: Test Login')
            login_data = {
                "locno": self.locno,
                "strid": f"{self.strid}",
                "strpasswd": f"{self.pswd}",
                "ntype": 0
            }
            headers, loginpbbodytobytes = pbMsg.create_login_request(self.locno,
                2, 117, login_data, LoginFunctionProto_pb2.MsgCsUserLogin)
            print("Test Login: Sending login request...")
            bodydata, starTime, endTime = pbMsg.send_Rec_Msg(
                None, self.s, headers, loginpbbodytobytes)
            print("Test Login: Received response.")
            ser_ret_databody = LoginFunctionProto_pb2.MsgScPlayerLoginCommonAck()
            ser_ret_databody.ParseFromString(bodydata)
            print("Test Login: Parsed server response successfully.")
            print('server ret is:',ser_ret_databody)
            totalTime = endTime - starTime
            days = totalTime.days
            total_seconds = totalTime.total_seconds()
            hours = int(total_seconds // 3600) % 24
            minutes = int(total_seconds // 60) % 60
            seconds = int(total_seconds) % 60
            milliseconds = int((total_seconds - int(total_seconds)) * 1000)
            print(f'登录共花了：{hours}小时，{minutes}分钟，{seconds}秒, {milliseconds}毫秒')
            if seconds >= 20:
                print('登录服异常，请迅速检查')
            else:
                print('登录服正常！')
            # print('睡眠5秒')
            # time.sleep(5)
        except Exception as e:
            print(f"Test Login: An error occurred: {e}")

    # @pytest.mark.run(order=1)
    # def test_loginverify(self):
    #     loginverify={
    #         'locno':self.locno,
    #         'strid':f'{self.strid}',
    #         'status':0,
    #         'branch':10246,
    #         'strVersion':'2.0.3.0'
    #     }
    #     headers,loginverifys=pbMsg.create_login_request(self.locno,2,115,loginverify,LoginFunctionProto_pb2.MsgCsLoginUsersCheck)
    #     retBodydata,*_=pbMsg.send_Rec_Msg(None,self.s,headers,loginverifys)
    #     ParseData=LoginFunctionProto_pb2.MsgGolfjoyLoginUsersCheckAck()
    #     ParseData.ParseFromString(retBodydata)
    #     print('用户登录校准返回：',ParseData)


    @pytest.mark.run(order=2)
    def test_loginack(self):
        try:
            print('执行用例3: Test Login Ack')
            data_ack = {
                'id': f'{self.strid}'
            }
            headers, login_ack = pbMsg.create_login_request(self.locno,
                2, 201, data_ack, LoginFunctionProto_pb2.MsgCsPlayerLoginResult)

            print("Test Login Ack: Sending login acknowledgment request...")
            pbMsg.send_Rec_Msg(None, self.s, headers, login_ack)
            print("Test Login Ack: Message sent successfully.")

        except Exception as e:
            print(f"Test Login Ack: An error occurred: {e}")

    @pytest.mark.run(order=3)
    def test_Foucelogout(self):
        print('执行用例2')
        body={
            'strid':f'{self.strid}',
            'locno':self.locno
            # 'outsource':0
        }
        headers, logout_ack = pbMsg.create_login_request(self.locno,2, 105, body, LoginFunctionProto_pb2.MsgScUserForceLogout)
        pbMsg.send_Rec_Msg(None,self.s,headers,logout_ack)