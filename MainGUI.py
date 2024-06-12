import threading
import urllib
from datetime import datetime
from io import BytesIO
from tkinter import *
import tkinter.ttk
from tkinter import simpledialog

import PIL

import API_Keys
import MonthCalendar

from PIL import Image, ImageTk
import Short_weather
from Match import Match

import Stadium_Map

from Gmail import get_email_details
from Telegram_Teller import Telegram

# MonthCalendar.year 로 년도를 읽을 수 있음
# MonthCalendar.month 로 현재 선택된 달을 읽을 수 있음
# MonthCalendar.day 로 현재 선택된 달을 읽을 수 있음

width = 1280
height = 720

x_position = 20
y_position = 20

team_image_url = {
    '한화': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_HH.png',
    'NC': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_NC.png',
    '삼성': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_SS.png',
    '키움': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_WO.png',
    '두산': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_OB.png',
    'LG': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_LG.png',
    'SSG': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_SK.png',
    '롯데': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_LT.png',
    'KT': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_KT.png',
    'KIA': 'https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/emblem/regular/2024/emblem_HT.png'
}

gmailImageURL = ('https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gmail_icon_%282020%29.svg/1024px'
                 '-Gmail_icon_%282020%29.svg.png')
telegramImageURL = ('https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/512px-Telegram_logo'
                    '.svg.png')
image_size = 80


class MainGUI:
    def __init__(self):
        # 윈도우 생성
        self.window = Tk()
        self.window.title('국내 축구 경기 일정')
        self.window.configure(bg='lightblue')

        # 오늘의 날짜를 불러옴
        self.now = datetime.now()
        MonthCalendar.year = self.now.year
        MonthCalendar.month = self.now.month
        MonthCalendar.day = self.now.day

        # 달력 생성
        self.createCalendar(self.window)

        # 구분선 추가
        separator_frame = Frame(self.window, width=5, bg='black')  # 너비(width)와 배경색(bg) 설정
        separator_frame.pack(side=LEFT, fill='y', padx=(10, 0))

        # Notebook 생성
        세부정보 = Frame(self.window)
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

        frame3 = Frame(세부정보)
        notebook.add(frame3, text='경기장')
        Stadium_Map.createStadiumFrame(frame3)

        frame4 = Frame(세부정보)
        notebook.add(frame4, text='즐겨찾기 관리')
        Label(frame4, text='페이지4의 내용',
              fg='yellow', font='helvetica 48').pack()

        self.telegram = Telegram()
        threading.Thread(target=self.telegram.running, daemon=True).start()
        self.telegramID = API_Keys.TelegramID

        self.window.mainloop()

    def createCalendar(self, mainframe):
        Calendar_frame = Frame(mainframe)
        Calendar_frame.pack(side=LEFT)

        # 달력을 출력하기 위한 프레임
        self.MonthCalendar = MonthCalendar.MonthCalendar(self, Calendar_frame)


        button_frame = Frame(Calendar_frame)
        button_frame.pack(side=TOP)
        # 이메일 전송 버튼 추가
        self.add_email_button(button_frame)

        # 텔레그램 전송 버튼 추가
        self.add_telegram_button(button_frame)

    def add_email_button(self, parent):
        with urllib.request.urlopen(gmailImageURL) as u:
            raw_data = u.read()

        original_image = Image.open(BytesIO(raw_data))
        resized_image = original_image.resize((image_size, image_size))
        image = ImageTk.PhotoImage(resized_image)

        email_button = Button(parent, text="이메일 보내기", command=self.open_email_dialog, image=image,
                              font=("Helvetica", 16), width=image_size, height=image_size)
        email_button.image = image

        email_button.pack(side=LEFT, padx=20, pady=20)

    def add_telegram_button(self, parent):
        with urllib.request.urlopen(telegramImageURL) as u:
            raw_data = u.read()

        original_image = Image.open(BytesIO(raw_data))
        resized_image = original_image.resize((image_size, image_size))
        image = ImageTk.PhotoImage(resized_image)
        # self.background = Label(self.window, image=image)
        # self.background.image = image
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        telegram_button = Button(parent, text="텔레그램 보내기",
                                 image=image,
                                 command=self.open_telegram_dialog,
                                 font=("Helvetica", 16), width=image_size, height=image_size)
        telegram_button.image = image

        telegram_button.pack(side=LEFT, padx=20, pady=20)

    def open_email_dialog(self):
        get_email_details(self.window)

    def open_telegram_dialog(self):
        # self.telegramID
        chat_id = simpledialog.askstring("텔레그램 보내기", "텔레그램 ID 입력:", initialvalue=self.telegramID,
                                         parent=self.window)
        if not chat_id:
            return
        self.telegram.replyDayMatchData(int(MonthCalendar.year * 10000 + MonthCalendar.month * 100 + MonthCalendar.day),
                                        chat_id)
        self.telegramID = chat_id

    def pressDay(self):
        self.match.readMatchData()


if __name__ == '__main__':
    MainGUI()
