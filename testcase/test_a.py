# coding=utf-8
import pytest
import threading
import time
from utilst.login_helper import pbMsg
from pbtopythonfile import LoginFunctionProto_pb2

class TestLogin:
    def setup_method(self):
        self.sever_set = ['America_socket']
        for i in range(len(self.sever_set)):
            self.s = pbMsg.socketConn(f'{self.sever_set[i]}')
            User = pbMsg.get_yaml_data('AmericaUser')
            self.strid = User['strid']
            self.locno = User['locno']
            self.pswd = User['pswod']
            self.nickname = User['nickname']
            self.keep_running = True
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeat)
            self.heartbeat_thread.start()
            print("Setup: Successfully established socket connection, initialized user data, and started heartbeat.")

    def teardown_method(self):
        self.keep_running = False
        self.heartbeat_thread.join()
        pbMsg.socketClose(self.s)
        print("Teardown: Socket connection closed and heartbeat stopped successfully.")

    def send_heartbeat(self):
        while self.keep_running:
            try:
                # Assuming an "empty" message can be used for heartbeat
                headers, heartbeat_msg = pbMsg.create_login_request(self.locno,
                    2, 200, {}, LoginFunctionProto_pb2.MsgCsUserLogin)
                pbMsg.send_Rec_Msg(None, self.s, headers, heartbeat_msg)
                print("Heartbeat sent.")
                time.sleep(5)
            except Exception as e:
                print(f"Heartbeat error: {e}")

    @pytest.mark.run(order=1)
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
            print('server ret is:', ser_ret_databody)
            totalTime = endTime - starTime
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
        except Exception as e:
            print(f"Test Login: An error occurred: {e}")

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