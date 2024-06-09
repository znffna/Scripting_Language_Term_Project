#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import Telegram_bot


def replyDayMatchData(date_param, user):
    print(user, date_param)
    res_list = Telegram_bot.getData(date_param)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>Telegram_bot.MAX_MSG_LENGTH:
            Telegram_bot.sendMessage(user, msg)
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        Telegram_bot.sendMessage( user, msg )
    else:
        Telegram_bot.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        Telegram_bot.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        Telegram_bot.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        Telegram_bot.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        Telegram_bot.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')
    now = datetime.now()
    if text.startswith('오늘의경기'):
        replyDayMatchData(int(now.year * 10000 + now.month * 100 + now.day), chat_id)
    elif text.startswith('경기') and len(args)>1:
        print('try to selected day 경기', args[1])
        replyDayMatchData(args[1], chat_id)
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    else:
        Telegram_bot.sendMessage(chat_id, '모르는 명령어입니다.\n경기 [경기날짜(YYYYMMDD)],'
                                          ' 오늘의경기 중 하나의 명령을 입력하세요.')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', Telegram_bot.TOKEN )

bot = telepot.Bot(Telegram_bot.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)