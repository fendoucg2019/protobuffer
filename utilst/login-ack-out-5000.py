# coding=utf-8
import time,os,sys
curpath=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(curpath)[0]
sys.path.append(rootpath)
from locust import HttpUser, TaskSet, task, between
from utilst.login_helper import pbMsg
from pbtopythonfile import LoginFunctionProto_pb2
from loguru import logger
from utilst import send_chat

# 定义服务器和通知用户
# SERVER_TO_USERS = {
#     "produc_server_ip": {
#         "mentioned_list": ["zhaoweiping"],
#         "mentioned_mobile_list": ["13800000000"]
#     },
#     "America_socket": {
#         "mentioned_list": ["zhaoweiping"],
#         "mentioned_mobile_list": ["13900000000"]
#     },
#     "Europe_socket": {
#         "mentioned_list": ["zhaoweiping"],
#         "mentioned_mobile_list": ["13700000000"]
#     }
# }
SERVER_TO_USERS = {
    "produc_server_ip": {
        "mentioned_list": ["zhaoweiping"],
        "mentioned_mobile_list": ["13800000000"]
    },
    "America_socket": {
        "mentioned_list": ["zhaoweiping"],
        "mentioned_mobile_list": ["13900000000"]
    },
    "Europe_socket": {
        "mentioned_list": ["zhaoweiping"],
        "mentioned_mobile_list": ["13700000000"]
    }
}

class LoginBehavior(TaskSet):
    """
    定义用户行为：登录、确认、登出
    """
    @task
    def login_flow(self):
        # 修正：通过 self.user 访问父类 HttpUser 的属性
        serveraddr = self.user.serveraddr
        serveruser = self.user.serveruser

        try:
            logger.debug(f"执行完整链路用例 for {serveraddr}: Test Login → ACK → Logout")

            # ------- 步骤 1: 登录 -------
            logger.debug("Step 1: 登录")
            self.s = pbMsg.socketConn(serveraddr)  # 建立 socket 连接
            User = pbMsg.get_yaml_data(serveruser)  # 加载用户数据
            strid = User['strid']
            locno = User['locno']
            pswd = User['pswod']

            # 构造登录请求
            login_data = {
                "locno": locno,
                "strid": f"{strid}",
                "strpasswd": f"{pswd}",
                "ntype": 0
            }
            headers, loginpbbodytobytes = pbMsg.create_login_request(
                locno, 2, 117, login_data, LoginFunctionProto_pb2.MsgCsUserLogin
            )
            logger.debug(f"发送登录请求： {serveraddr}...")
            bodydata, start_time, end_time = pbMsg.send_Rec_Msg(
                None, self.s, headers, loginpbbodytobytes
            )
            logger.debug("登录:接受响应.")
            time.sleep(2)

            ser_ret_databody = LoginFunctionProto_pb2.MsgScPlayerLoginCommonAck()
            ser_ret_databody.ParseFromString(bodydata)
            print("server ret is:", ser_ret_databody)
            self._calculate_time(start_time, end_time)

            # ------- 步骤 2: 登录确认 -------
            logger.debug("Step 2: 登录确认")
            data_ack = {"id": f"{strid}"}
            headers, login_ack = pbMsg.create_login_request(
                locno, 2, 201, data_ack, LoginFunctionProto_pb2.MsgCsPlayerLoginResult
            )
            logger.debug(f"发送登录 ACK 到 {serveraddr}...")
            pbMsg.send_Rec_Msg(None, self.s, headers, login_ack)

            # ------- 步骤 3: 强制登出 -------
            logger.info("Step 3: 登出")
            body = {
                "strid": f"{strid}",
                "locno": locno
            }
            headers, logout_ack = pbMsg.create_login_request(
                locno, 2, 105, body, LoginFunctionProto_pb2.MsgScUserForceLogout
            )
            pbMsg.send_Rec_Msg(None, self.s, headers, logout_ack)
            logger.debug("退出成功")

        except Exception as e:
            error_message = f"服务器 {serveraddr} 登录链路失败: {e}"
            if serveraddr in SERVER_TO_USERS:
                users = SERVER_TO_USERS[serveraddr]
                send_chat.send_wechat_notification(
                    content=error_message,
                    mentioned_list=users.get("mentioned_list", []),
                    mentioned_mobile_list=users.get("mentioned_mobile_list", [])
                )
            else:
                logger.error("未定义的服务器通知用户！")

    @staticmethod
    def _calculate_time(start_time, end_time):
        total_time = end_time - start_time
        total_seconds = total_time.total_seconds()
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        print(f"耗时：{int(total_seconds)}秒, {milliseconds}毫秒")
        if total_seconds >= 20:
            print("服务异常，请检查！")
        else:
            print("服务正常。")


class LoginUser(HttpUser):
    """
    定义用户类
    """
    tasks = [LoginBehavior]
    wait_time = between(1, 2)  # 模拟用户操作的思考时间
    serveraddr = "test_server_ip"  # 默认服务器地址
    serveruser = "TestUser"  # 默认用户