from datetime import datetime
from tkinter import *
import tkinter.ttk

import requests
import json

import MonthCalendar


# MonthCalendar.year 로 년도를 읽을 수 있음
# MonthCalendar.month 로 현재 선택된 달을 읽을 수 있음

width = 1280
height = 720

x_position = 20
y_position = 20


class MainGUI:

    def __init__(self):

        window = Tk()
        window.title('국내 축구 경기 일정')

        # 달력 생성
        Calendar_frame = Frame(window)
        Calendar_frame.pack(side=LEFT)

        # 실제 경기 내용이 저장되는 공간
        self.month_match = {}  # {day : [한 경기], [한 경기], day : [한 경기], ..., ...}
        
        # 달력을 출력하기 위한 프레임
        self.달력프레임 = Frame(Calendar_frame)
        self.달력프레임.pack(side=TOP)

        # 달력의 일을 선택하기 위한 버튼
        self.CalendarButton = []

        # 오늘의 년/월 을 할당하는 변수
        now = datetime.now()

        global year, month
        year = now.year
        month = now.month

        self.MonthCalendar = MonthCalendar.MonthCalendar(self.달력프레임, self.month_match)

        cFrame2 = Frame(Calendar_frame)
        cFrame2.pack(side=TOP)
        self.MonthController = MonthCalendar.MonthController(cFrame2, self.MonthCalendar)

        # Notebook 생성
        세부정보 = Frame(window)
        세부정보.pack()
        notebook = tkinter.ttk.Notebook(세부정보, width=width, height=height)
        notebook.pack(side=LEFT)

        frame1 = Frame(세부정보)
        notebook.add(frame1, text='경기 일정')

        frame2 = Frame(세부정보)
        notebook.add(frame2, text='날씨 정보')
        Label(frame2, text='페이지2의 내용',
              fg='blue', font='helvetica 48').pack()

        frame3 = Frame(세부정보)
        notebook.add(frame3, text='경기장')
        Label(frame3, text='페이지3의 내용',
              fg='orange', font='helvetica 48').pack()

        frame4 = Frame(세부정보)
        notebook.add(frame4, text='즐겨찾기 관리')
        Label(frame4, text='페이지4의 내용',
              fg='yellow', font='helvetica 48').pack()
        window.mainloop()


if __name__ == '__main__':
    MainGUI()
