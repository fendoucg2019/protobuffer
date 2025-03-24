#coding=utf-8
import requests

def send_wechat_notification(content,mentioned_list=None, mentioned_mobile_list=None):
    """
    发送企业微信通知消息
    :param webhook_url: 企业微信机器人 webhook 地址
    :param content: 通知消息内容（文本）
    """
    webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9b610aaa-f948-49cf-92fd-78e0c0c17961' #小群
    # webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c19f720a-e34b-4b0a-be22-6dfac06798a7' #大群

    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list or [],  # 默认空列表
            "mentioned_mobile_list": mentioned_mobile_list or []  # 默认空列表
        }
    }
    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        response.raise_for_status()
        return True
        # print(f"企业微信通知发送成功: {content}")
    except Exception as e:
        print(f"企业微信通知发送失败: {e}")