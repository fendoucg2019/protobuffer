# coding=utf-8
import time

import pytest,os,sys
curpath=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(curpath)[0]
sys.path.append(rootpath)

from utilst.login_helper import pbMsg
from pbtopythonfile import LoginFunctionProto_pb2
from loguru import logger
from utilst import send_chat
# a="chenliwu","yuguojie","xuyilin"
SERVER_TO_USERS = {

    "produc_server_ip": {
        "mentioned_list": ["zhaoweiping"],  # 企业微信用户名
        "mentioned_mobile_list": ["13800000000"]  # 手机号
    },
    "America_socket": {
        "mentioned_list": ["zhaoweiping"],  # 企业微信用户名
        "mentioned_mobile_list": ["13900000000"]  # 手机号
    },
    "Europe_socket": {
        "mentioned_list": ["zhaoweiping"],  # 企业微信用户名
        "mentioned_mobile_list": ["13700000000"]  # 手机号
    }
}

@pytest.mark.parametrize(
    "serveraddr, serveruser",
    [
        ('produc_server_ip', 'ProducUser'),
        ('America_socket', 'AmericaUser'),
        ('Europe_socket', 'EuropeUser')
    ]
)
class TestLogin:

    def test_full_flow(self, serveraddr, serveruser):
        """
        测试完整链路：登录 → 确认 → 登出
        """
        # 定义 socket 属性和用户数据
        self.s = None
        try:
            logger.debug(f"执行完整链路用例 for {serveraddr}: Test Login → ACK → Logout")

            # ------- 步骤 1: 登录 -------
            logger.debug("Step 1: 登录")
            self.s = pbMsg.socketConn(serveraddr)  # 建立 socket 连接
            User = pbMsg.get_yaml_data(serveruser)  # 加载用户数据
            self.strid = User['strid']
            self.locno = User['locno']
            self.pswd = User['pswod']
            self.nickname = User['nickname']

            # 构造登录请求
            login_data = {
                "locno": self.locno,
                "strid": f"{self.strid}",
                "strpasswd": f"{self.pswd}",
                "ntype": 0
            }
            headers, loginpbbodytobytes = pbMsg.create_login_request(
                self.locno, 2, 117, login_data, LoginFunctionProto_pb2.MsgCsUserLogin
            )
            logger.debug(f"发送登录请求： {serveraddr}...")
            bodydata, start_time, end_time = pbMsg.send_Rec_Msg(None, self.s, headers, loginpbbodytobytes)
            logger.debug("登录:接受响应.")
            logger.debug("等待3秒，应对服务器返回慢导致解析失败")
            time.sleep(3)
            # 检查登录返回结果
            ser_ret_databody = LoginFunctionProto_pb2.MsgScPlayerLoginCommonAck()
            ser_ret_databody.ParseFromString(bodydata)
            if serveraddr=='produc_server_ip':
                loginsuccess="国内生产环境 登录服 正常(模拟G4 PC客户端发送 117 → 201 → 105 链路消息)."
            elif serveraddr=='America_socket':
                loginsuccess = "美服 登录服 正常(模拟G4 PC客户端发送 117 → 201 → 105 链路消息)."
            else:
                loginsuccess ="欧服 登录服 正常(模拟G4 PC客户端发送 117 → 201 → 105 链路 消息)."


            # 打印登录时间
            self._calculate_time(start_time, end_time)

            # ------- 步骤 2: 登录确认 -------
            logger.debug("Step 2: 登录确认")
            data_ack = {'id': f'{self.strid}'}
            headers, login_ack = pbMsg.create_login_request(
                self.locno, 2, 201, data_ack, LoginFunctionProto_pb2.MsgCsPlayerLoginResult
            )
            logger.debug(f"发送登录 ACK 到 {serveraddr}...")
            pbMsg.send_Rec_Msg(None, self.s, headers, login_ack)

            # ------- 步骤 3: 强制登出 -------
            logger.info("Step 3: 登出")
            body = {
                'strid': f'{self.strid}',
                'locno': self.locno
                # 'outsource': 0
            }
            headers, logout_ack = pbMsg.create_login_request(
                self.locno, 2, 105, body, LoginFunctionProto_pb2.MsgScUserForceLogout
            )
            pbMsg.send_Rec_Msg(None, self.s, headers, logout_ack)
            logger.debug("退出成功")

        except Exception as e:

            #服务器异常发送企业微信通知
            error_message = f"服务器 {serveraddr} 登录链路失败: {e}"
            if serveraddr in SERVER_TO_USERS:
                users = SERVER_TO_USERS[serveraddr]
                send_chat.send_wechat_notification(
                    content=error_message,
                    mentioned_list=users.get("mentioned_list", []),
                    mentioned_mobile_list=users.get("mentioned_mobile_list", [])
                )
            else:
                pass
                # send_chat.send_wechat_notification(content=error_message)

        finally:
            # 释放资源
            if self.s:
                pbMsg.socketClose(self.s)
                logger.debug(f"收尾: 关闭链接 {serveraddr}.")

    @staticmethod
    def _calculate_time(start_time, end_time):
        """计算并打印时间差"""
        total_time = end_time - start_time
        total_seconds = total_time.total_seconds()
        hours = int(total_seconds // 3600) % 24
        minutes = int(total_seconds // 60) % 60
        seconds = int(total_seconds) % 60
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        print(f'耗时：{hours}小时，{minutes}分钟，{seconds}秒, {milliseconds}毫秒')
        if seconds >= 20:
            print('服务异常，请检查！')
        else:
            print('服务正常。')