#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3

import requests
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import API_Keys

TOKEN = API_Keys.TelegramBot_API_Key
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getData(date_param):
    res_list = []
    today_data = {
        'leId': 1,
        'srId': '0,1,3,4,5,7,9',
        'Date': date_param,
    }
    # print(today_data)
    res = requests.post('https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList', data=today_data)
    res.encoding = 'utf-8'
    match_inform = []
    for game in res.json()['game']:
        print('GAME_STATE_SC = ', game['GAME_STATE_SC'])
        if game['GAME_STATE_SC'] == '3':  # 정상적으로 진행된 경기일 경우
            inform_match = (str(game['AWAY_NM']) + ' ' + str(game['T_SCORE_CN']) + ' vs ' + str(game['B_SCORE_CN']) +
                            ' ' + str(game['HOME_NM']) + ' ' + str(game['G_TM']) + ' ' + str(game['S_NM']))
        else:
            inform_match = (str(game['AWAY_NM']) + ' vs ' + str(game['HOME_NM']) + ' ' +
                            str(game['G_TM']) + ' ' + str(game['S_NM']))
        match_inform.append(inform_match)
    return match_inform


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user = data[0]
        print(user, date_param)
        res_list = getData(date_param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
