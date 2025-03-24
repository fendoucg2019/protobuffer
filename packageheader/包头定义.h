#pragma once
/**
 * Title: PublicDefine.h
 * Detail: �������ݽṹ����
 * Author: liuquan
 * Date: 2022/01/20
 */

const int NET_MSG_HEARTBEAT = 0;//����
const int ACCOUNT_LEN = 64;//�˺ų���
const int PWD_LEN = 36;//���볤��
const int VER_LEN = 36;//�汾�ų���
const int URL_LEN = 255;//url����
const int NICK_LEN = 255;//�ǳƳ���
const int MAX_USER = 8;//ģ������¼������û�
const int MAX_HOLE_CNT = 18;
const int HALF_HOLE_CNT = 9;
const int MAX_DEV = 2;//������ս֧�ֵ�����豸����
const int TIME_LEN = 32;//ʱ�䳤��
const int PAGE_DEV = 8;//һҳ��ʾ���豸����

//ƽ̨����  �򻯳��ȣ��õ����ַ�����
enum PLATFORM_TYPE
{
	PLATFORM_TYPE_SIMULATOR = 1,//ģ����ƽ̨
	PLATFORM_TYPE_MINICENTERCONTROL = 2,//�����п�ƽ̨
};

//ҵ������-����  �򻯳��ȣ��õ����ַ�����
enum BUSINESS_TYPE
{
	BUSINESS_TYPE_CLUBMANAGER = 1,//��������ҵ��
	BUSINESS_TYPE_LOGIN = 2,//��¼ҵ��
	BUSINESS_TYPE_LICENSE = 3,//Licenseҵ��
	BUSINESS_TYPE_ONLINEBATTLE = 4,//������սҵ��
	BUSINESS_TYPE_BASEDATA = 5,//��������ҵ��

};

/**
 * @brief �������ݰ�ͷ
 * @note java�����û��unsigned���ͣ��ʱ���һ�£�ȫ�����з��ŵ�
 * @note �ֽ�����java���������ֽ���Ϊ׼��ͳһ���ô��
 * @note С�˿ͻ����ڷ��Ͱ�ͷ��ʱ����Ҫ����ͷ�����ֽ���ת������С��ת���
 * @note С�˿ͻ����ڽ��հ�ͷ��ʱ����Ҫ����ͷ�����ֽ���ת���������תС��
 * @note ��ͷ��Ƶ�ʱ�򣬿������ڴ���룬�ֶ�������һЩ�ֶΣ�����������Զ������ڴ�, ����޸İ�ͷ����Ҫ�ر�ע���ڴ������һ��
 */
struct PacketHead
{
	char platformType;//ƽ̨����  �򻯳��ȣ��õ����ַ�����

	char businessType;//ҵ������  �򻯳��ȣ��õ����ַ�����

	char subType1;//�����ֶ�1 ͬʱ�𵽲�������

	char subType2;//�����ֶ�2 ͬʱ�𵽲�������

	__int32 msgID;//��ϢID��������ϢID������ƽ̨���ͺ�ҵ������

	__int32 dataLen;//���ݳ���(ָbody)

	__int32 checkFlag;//У��λ

	__int32 devID;//�豸ID 

	__int32 word1;//�����ֶ�1 �𵽲�������� 

	__int64 packetTime;//��ʱ���, ʹ��64λʱ������������Ⱥ�δ�����÷�Χ

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

	//to do...�������У�麯����У�鷽ʽ����ͨ���豸Ψһʶ��ID�������������ͣ���ϢID���Լ�ʱ�������ɵ��ַ�������һ��MD5���м�У�飬���巽ʽ���Ժ��������ۣ�ǰ�ڿ�����ʱ����
	void AddCheckFlag()
	{
		__int32 temp = (packetTime / 5000);//ʱ�侫��Ϊ���룬����5���ڻ�õ���ͬ�Ľ��
		checkFlag = (__int32)platformType * 1 + (__int32)businessType * 2 + msgID * 3 + devID * 4 + temp;
	}

	__int32 GetCheckFlag()
	{
		__int32 temp = (packetTime / 5000);//ʱ�侫��Ϊ���룬����5���ڻ�õ���ͬ�Ľ��
		__int32 ret = (__int32)platformType * 1 + (__int32)businessType * 2 + msgID * 3 + devID * 4 + temp;
		return ret;
	}

};


class BaseBusinessData
{
public:
	BaseBusinessData() { msgID = 0; }
	virtual ~BaseBusinessData() {}//��������������֤�����ڴ�����ȷ�ͷ�

	int msgID;//
};

typedef void (*NetReconnectCallBack)(void);