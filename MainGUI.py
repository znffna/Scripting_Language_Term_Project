from datetime import datetime
from tkinter import *
import tkinter.ttk

import requests
import json
import urllib.parse

import MonthCalendar

from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import Short_weather
from Match import Match

import Stadium_Map

# MonthCalendar.year 로 년도를 읽을 수 있음
# MonthCalendar.month 로 현재 선택된 달을 읽을 수 있음
# MonthCalendar.day 로 현재 선택된 달을 읽을 수 있음

width = 1280
height = 720

x_position = 20
y_position = 20

team_image_url = {'한화': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_HH.png',
                  'NC': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_NC.png',
                  '삼성': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_SS.png',
                  '키움': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_WO.png',
                  '두산': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_OB.png',
                  'LG': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_LG.png',
                  'SSG': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_SK.png',
                  '롯데': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_LT.png',
                  'KT': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_KT.png',
                  'KIA': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_HT.png'}


class MainGUI:
    def createCalendar(self, mainframe):
        Calendar_frame = Frame(mainframe)
        Calendar_frame.pack(side=LEFT)

        # 달력을 출력하기 위한 프레임
        self.MonthCalendar = MonthCalendar.MonthCalendar(self, Calendar_frame)


    def __init__(self):

        # 오늘의 날짜를 불러옴
        now = datetime.now()
        MonthCalendar.year = now.year
        MonthCalendar.month = now.month
        MonthCalendar.day = now.day


        # 윈도우 생성
        window = Tk()
        window.title('국내 축구 경기 일정')
        window.configure(bg='lightblue')


        # 달력 생성
        self.createCalendar(window)

        # 구분선 추가
        separator_frame = Frame(window, width=5, bg='black')  # 너비(width)와 배경색(bg) 설정
        separator_frame.pack(side=LEFT, fill='y', padx=(10, 0) )

        # Notebook 생성
        세부정보 = Frame(window)
        세부정보.pack()
        notebook = tkinter.ttk.Notebook(세부정보, width=width, height=height)
        notebook.pack(side=LEFT)

        frame1 = Frame(세부정보)
        notebook.add(frame1, text='경기 일정')
        # 경기 일정 생성
        self.match = Match(frame1)

        frame2 = Frame(세부정보)
        notebook.add(frame2, text='날씨 정보')
        Short_weather.create_weather_frame(frame2)
        # Label(frame2, text='페이지2의 내용',
        #       fg='blue', font='helvetica 48').pack()

        frame3 = Frame(세부정보)
        notebook.add(frame3, text='경기장')
        Stadium_Map.createStadiumFrame(frame3)
        # Label(frame3, text='페이지3의 내용',
        #       fg='orange', font='helvetica 48').pack()

        frame4 = Frame(세부정보)
        notebook.add(frame4, text='즐겨찾기 관리')
        Label(frame4, text='페이지4의 내용',
              fg='yellow', font='helvetica 48').pack()
        window.mainloop()

    def pressDay(self):
        # print(MonthCalendar.day, '일 선택됨')
        self.match.readMatchData()


if __name__ == '__main__':
    MainGUI()
