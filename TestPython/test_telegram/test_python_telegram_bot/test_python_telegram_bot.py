# pip install python_telegram_bot

import telegram
from telegram.ext import Updater
from telegram.utils import request

telegram_token = '586032648:AAGB5DLs-J84z25y7zVZd8Ugobef-zTMJ2A'
# channel should be public and this is the channel link:
channel_name = '@test_channel_test_channel_test'
channel_user_name = '@user_test_telegram_bot'

bot = telegram.Bot(token=telegram_token)
msg = '<h1>hello from python ***</h1>'
status = bot.send_message(chat_id=channel_name, text=msg, parse_mode=telegram.ParseMode.HTML)
print(status)

# set proxy
# pip install pysocks
# updater = Updater(token=telegram_token, request_kwargs={
#     'proxy_url': 'socks5://192.168.1.193:1080/'
# })
#
# pp = request.Request(proxy_url='socks5://192.168.1.193:1080')
# bot2 = telegram.Bot(token=telegram_token, request=pp)
#
# status2 = bot2.send_message(chat_id=channel_name, text='hallo from python')
# print(status2)