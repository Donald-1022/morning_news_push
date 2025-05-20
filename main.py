import requests

# ✅ 直接写入你的 Token
ALAPI_TOKEN = "t7lmeyheeicjmwzqrodpefu2m72aly"  # 替换为你的实际 token
WPUSH_APIKEY = "WPUSHvR76iq827D8jDRw5N7wVMWrruj9"  # 替换为你的实际 apikey
CHANNEL = "wechat"  # 可选：wechat, sms, mail, feishu 等
SEND_TYPE = "image"  # 可选：image 或 text

# 获取早报信息
def get_news():
    url = 'https://v2.alapi.cn/api/zaobao'
    params = {'token': ALAPI_TOKEN}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('code') == 200:
        return data.get('data')
    else:
        print(f"获取早报失败：{data.get('msg')}")
        return None

# 推送消息
def push_message(title, content):
    url = 'https://api.wpush.cn/api/v1/send'
    params = {
        'apikey': WPUSH_APIKEY,
        'title': title,
        'content': content,
        'channel': CHANNEL
    }

    response = requests.post(url, data=params)
    data = response.json()
    if data.get("code") == 0:
        return True
    else:
        print(f"推送失败：{data.get('message')}")
        return False

# 主函数
def main():
    if not ALAPI_TOKEN or not WPUSH_APIKEY:
        print('请填写 ALAPI_TOKEN 和 WPUSH_APIKEY！')
        return

    if SEND_TYPE not in ["image", "text"]:
        print("SEND_TYPE 参数错误，已默认设置为 image")
        send_type = "image"
    else:
        send_type = SEND_TYPE

    news_data = get_news()
    if news_data:
        date = news_data.get('date')
        news_list = news_data.get('news')
        image_url = news_data.get('image')

        title = '每日60秒早报'
        content = f'### 日期：{date}\n\n'

        if send_type == "image":
            content += f'![image]({image_url})'
        else:
            content += '#### 新闻：\n'
            for news in news_list:
                content += f'- {news}\n'

        if push_message(title, content):
            print('✅ 消息推送成功！')
        else:
            print('❌ 消息推送失败！')
    else:
        print('❌ 获取早报信息失败！')

if __name__ == '__main__':
    main()
