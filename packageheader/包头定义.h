#pragma once
/**
 * Title: PublicDefine.h
 * Detail: 公共数据结构定义
 * Author: liuquan
 * Date: 2022/01/20
 */

const int NET_MSG_HEARTBEAT = 0;//心跳
const int ACCOUNT_LEN = 64;//账号长度
const int PWD_LEN = 36;//密码长度
const int VER_LEN = 36;//版本号长度
const int URL_LEN = 255;//url长度
const int NICK_LEN = 255;//昵称长度
const int MAX_USER = 8;//模拟器登录的最大用户
const int MAX_HOLE_CNT = 18;
const int HALF_HOLE_CNT = 9;
const int MAX_DEV = 2;//联网对战支持的最大设备数量
const int TIME_LEN = 32;//时间长度
const int PAGE_DEV = 8;//一页显示的设备数量

//平台类型  简化长度，用单个字符概括
enum PLATFORM_TYPE
{
	PLATFORM_TYPE_SIMULATOR = 1,//模拟器平台
	PLATFORM_TYPE_MINICENTERCONTROL = 2,//迷你中控平台
};

//业务类型-大类  简化长度，用单个字符概括
enum BUSINESS_TYPE
{
	BUSINESS_TYPE_CLUBMANAGER = 1,//会所管理业务
	BUSINESS_TYPE_LOGIN = 2,//登录业务
	BUSINESS_TYPE_LICENSE = 3,//License业务
	BUSINESS_TYPE_ONLINEBATTLE = 4,//联网对战业务
	BUSINESS_TYPE_BASEDATA = 5,//基础数据业务

};

/**
 * @brief 公用数据包头
 * @note java服务端没有unsigned类型，故保持一致，全部用有符号的
 * @note 字节序以java服务器的字节序为准，统一采用大端
 * @note 小端客户端在发送包头的时候，需要将包头进行字节序转换，即小端转大端
 * @note 小端客户端在接收包头的时候，需要将包头进行字节序转换，即大端转小端
 * @note 包头设计的时候，考虑了内存对齐，手动补齐了一些字段，避免编译器自动补齐内存, 如果修改包头，需要特别注意内存对齐这一块
 */
struct PacketHead
{
	char platformType;//平台类型  简化长度，用单个字符概括

	char businessType;//业务类型  简化长度，用单个字符概括

	char subType1;//保留字段1 同时起到补齐作用

	char subType2;//保留字段2 同时起到补齐作用

	__int32 msgID;//消息ID，不从消息ID上区分平台类型和业务类型

	__int32 dataLen;//数据长度(指body)

	__int32 checkFlag;//校验位

	__int32 devID;//设备ID 

	__int32 word1;//保留字段1 起到补齐的作用 

	__int64 packetTime;//包时间戳, 使用64位时间戳，提升精度和未来适用范围

	PacketHead()
	{
		platformType = 0;
		businessType = 0;
		subType1 = 0;
		subType2 = 0;
		msgID = 0;
		dataLen = 0;
		checkFlag = 0;
		devID = 0;
		word1 = 0;
		packetTime = 0;
	}

	//to do...后续添加校验函数，校验方式可以通过设备唯一识别ID，加上数据类型，消息ID，以及时间戳等组成的字符串生成一个MD5进行简单校验，具体方式可以后续再讨论，前期可以暂时不用
	void AddCheckFlag()
	{
		__int32 temp = (packetTime / 5000);//时间精度为毫秒，所以5秒内会得到相同的结果
		checkFlag = (__int32)platformType * 1 + (__int32)businessType * 2 + msgID * 3 + devID * 4 + temp;
	}

	__int32 GetCheckFlag()
	{
		__int32 temp = (packetTime / 5000);//时间精度为毫秒，所以5秒内会得到相同的结果
		__int32 ret = (__int32)platformType * 1 + (__int32)businessType * 2 + msgID * 3 + devID * 4 + temp;
		return ret;
	}

};


class BaseBusinessData
{
public:
	BaseBusinessData() { msgID = 0; }
	virtual ~BaseBusinessData() {}//虚析构函数，保证子类内存能正确释放

	int msgID;//
};

typedef void (*NetReconnectCallBack)(void);