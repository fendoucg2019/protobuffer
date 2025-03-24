# -*- coding: utf-8 -*-
import pytest
import socket
import struct
import time
from pbtopythonfile.LoginFunctionProto_pb2 import (
    MsgCsUserLogin,
    MsgScUserLoginAck,
    MsgScUserForceLogout,
)

# ------------------ 关键配置（需与服务端严格对齐）------------------
SERVER_HOST = "120.76.138.211"  # 服务端公网IP
SERVER_PORT = 19999  # 服务端开放端口
PLATFORM_TYPE = 3  # 平台类型（与服务端一致）
BUSINESS_TYPE = 2  # 业务类型（与服务端一致）
DEV_ID_CHECK = 0  # 服务端是否校验devID（调试用）


# ------------------ 协议头修正（核心改动）------------------
class PacketHead:
    """
    基于与服务端确认的实际结构定义：
    struct PacketHead {
        uint8_t platform;   // 1字节 平台类型
        uint8_t business;   // 1字节 业务类型
        int32_t msgID;      // 4字节 消息ID
        int32_t dataLen;    // 4字节 数据长度
        int32_t checkFlag;  // 4字节 校验码
        int64_t timestamp;  // 8字节 时间戳（毫秒）
    };
    总字节数：1 + 1 + 4 + 4 + 4 + 8 = 22 bytes
    """
    FORMAT = "!2B iii q"  # 平台(1)、业务(1) | msgID(4)、dataLen(4)、checkFlag(4) | timestamp(8)
    SIZE = struct.calcsize(FORMAT)  # 22 bytes

    def __init__(self):
        self.platform = PLATFORM_TYPE
        self.business = BUSINESS_TYPE
        self.msgID = 0
        self.dataLen = 0
        self.checkFlag = 0
        self.timestamp = int(time.time() * 1000)  # 毫秒时间戳

    def pack(self):
        return struct.pack(
            self.FORMAT,
            self.platform,
            self.business,
            self.msgID,
            self.dataLen,
            self.checkFlag,
            self.timestamp
        )

    def calculate_check_flag(self):
        """根据服务端真实算法实现的校验码计算"""
        # 示例：基于时间戳 + msgID的简单校验（需替换为真实算法）
        return self.timestamp % 10000 + self.msgID * 1024

    # ------------------ 通信核心模块优化 ------------------


def send_request(sock, msg_id, proto_msg, timeout=15):
    """发送请求并完整接收响应（关键功能增强）"""
    try:
        # --- 配置超时 ---
        sock.settimeout(timeout)

        # --- 构造完整请求数据 ---
        body_data = proto_msg.SerializeToString()
        body_len = len(body_data)

        header = PacketHead()
        header.msgID = msg_id
        header.dataLen = body_len
        header.checkFlag = header.calculate_check_flag()
        header_data = header.pack()

        full_request = header_data + body_data
        # [调试] 打印发送字节详情
        print(f"\n[Send Request] MsgID={msg_id}, BodySize={body_len}")
        print(f"Header Hex (first 16B): {header_data[:16].hex()}...")
        if body_len > 0:
            print(f"Body Hex (first 32B): {body_data[:32].hex()}...")

            # --- 发送请求 ---
        sock.sendall(full_request)

        # --- 接收包头 ---
        header_recv = b""
        while len(header_recv) < PacketHead.SIZE:
            chunk = sock.recv(PacketHead.SIZE - len(header_recv))
            if not chunk:
                raise ConnectionError("服务端关闭连接（包头接收中断）")
            header_recv += chunk

            # [调试] 包头解析验证
        print(f"[Recv Header] Bytes: {len(header_recv)}, Hex: {header_recv.hex()[:24]}...")
        try:
            fields = struct.unpack(PacketHead.FORMAT, header_recv)
        except struct.error as e:
            raise ValueError(f"包头解析失败 ({str(e)}), 原始数据: {header_recv.hex()}")

        _, _, recv_msg_id, body_len, check_flag, _ = fields

        # --- 接收包体 ---
        body_recv = b""
        while len(body_recv) < body_len:
            remain = body_len - len(body_recv)
            chunk = sock.recv(4096 if remain > 4096 else remain)
            if not chunk:
                raise ConnectionError("服务端关闭连接（包体接收中断）")
            body_recv += chunk

        print(f"[Recv Body] 期望:{body_len}, 实际:{len(body_recv)}")

        return header_recv + body_recv

    except socket.timeout as e:
        raise TimeoutError(f"与服务端通信超时: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"通信异常: {str(e)}")

    # ------------------ 响应解析模块 ------------------


def parse_response(response):
    """安全解析响应"""
    if len(response) < PacketHead.SIZE:
        raise ValueError("响应数据长度不足以解析包头")

    try:
        header = response[:PacketHead.SIZE]
        body = response[PacketHead.SIZE:]

        fields = struct.unpack(PacketHead.FORMAT, header)
        return {
            "platform": fields[0],
            "business": fields[1],
            "msg_id": fields[2],
            "data_len": fields[3],
            "check_flag": fields[4],
            "body": body
        }
    except struct.error:
        print(f"[ERROR] 包头解析失败！Hex: {header.hex()}")
        raise

    # ------------------ 测试用例模块 ------------------


@pytest.fixture(scope="function")
def socket_connection():
    """确保每个测试用例创建新连接"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"\n尝试连接到 {SERVER_HOST}:{SERVER_PORT} ...")
        sock.settimeout(10)
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("连接成功")
        yield sock
    except socket.error as e:
        pytest.skip(f"无法连接到服务端，跳过测试: {str(e)}")
    finally:
        sock.close()
        print("连接已关闭")


def test_user_login(socket_connection):
    """用户登录流程验证"""
    req = MsgCsUserLogin(
        locno=103937,
        strid="109099",
        strpasswd="12345678",
        ntype=0
    )

    try:
        # 发送登录请求
        response = send_request(socket_connection, 103, req, timeout=20)
        res = parse_response(response)

        # 校验包头消息ID
        assert res["msg_id"] == 104, f"期望响应MsgID 104，收到 {res['msg_id']}"

        # 解析Proto消息
        ack = MsgScUserLoginAck()
        ack.ParseFromString(res["body"])
        print(f"登录结果: 状态={ack.nret}, 错误码={ack.nErrorCode}, 用户ID={ack.strid}")

        assert ack.nret == 1, "登录失败！"
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_force_logout(socket_connection):
    """强制用户下线测试"""
    req = MsgScUserForceLogout(
        strid="109099",
        locno=103937,
        outsource=0
    )

    try:
        response = send_request(socket_connection, 106, req, timeout=20)
        res = parse_response(response)

        assert res["msg_id"] == 202, f"期望响应MsgID 202，收到 {res['msg_id']}"
        print("踢人指令发送成功")
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


if __name__ == "__main__":
    pytest.main(["-s", __file__])  # -s显示print输出