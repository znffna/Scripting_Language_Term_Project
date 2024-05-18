from tkinter import *
import tkinter.ttk

import requests
import json

import calendar

width = 1280
height = 720

x_position = 20
y_position = 20


class MainGUI:

    def readMonthData(self):
        month_data = {  # 'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'leId': 1,
            'srIdList': '0,9,6',
            'seasonId': self.year,
            'gameMonth': str(self.month).zfill(2),
            'teamID': ''
        }
        res = requests.post('https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList', data=month_data)
        res.encoding = 'utf-8'
        print(res.status_code)
        # print(res.json())
        # pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        # print(pretty_json)
        self.month_match = {}  # {day : [한 경기], [한 경기], day : [한 경기], ..., ...}
        for i in range(1, 32):
            self.month_match[i] = []
        day = 1
        for game in res.json()['rows']:
            info = game["row"]
            # 1. 날짜
            # 2. 시간
            # 3. 경기
            # 4. 게임센터
            # 5. 하이라이트
            # 6. TV
            # 7. 라디오
            # 8. 구장
            # 9. 비고
            node_info = []
            # print(info)
            for node in info:
                if node['Class'] == 'day':
                    day = int(str(node['Text'])[3:5])
                    # self.month_match[day] = []
                    continue
                Text = str(node['Text'])
                Text = Text.replace('class="win"', '')
                Text = Text.replace('class="lose"', '')
                Text = Text.replace('class="same"', '')
                # Text = Text.replace('class="win"', ' win ')
                # Text = Text.replace('class="lose"', ' lose ')
                Text = Text.replace('<b>', '')
                Text = Text.replace('</b>', '')
                Text = Text.replace('<', '')
                Text = Text.replace('>', '')
                Text = Text.replace('/em', ' ')
                Text = Text.replace('em', '')
                Text = Text.replace('/', '')
                Text = Text.replace('span', '')
                Text = Text.replace('vs', ' vs')
                # print(str(node['Class']) + " : " + Text)
                node_info.append(Text)
                # print(str(node['Class']) + " : " + str(node['Text']))
            self.month_match[day].append(node_info)
        # 디버그용 출력
        for days, matches in self.month_match.items():
            print(days)
            for match in matches:
                print(match)
            print()
        pass

    def setCalendar(self, frame):
        weekdays = ('일', '월', '화', '수', '목', '금', '토')
        calendar.setfirstweekday(calendar.SUNDAY)
        cal = calendar.monthcalendar(self.year, self.month)

        if self.CalendarButton:
            for week in self.CalendarButton:
                for day in week:
                    day.grid_remove()
            self.CalendarButton.clear()

        for week_num, week in enumerate(cal):
            self.CalendarButton.append([])
            for day_num, day in enumerate(week):
                # 버튼 생성
                btn = Button(frame, text='', width=5, height=5)
                btn.grid(row=week_num, column=day_num, padx=(x_position, 0), pady=(y_position, 0))
                btn.grid_remove()
                self.CalendarButton[week_num].append(btn)

        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                # x_position = 20 * day_num
                if day != 0:
                    # 버튼의 x 위치를 요일에 따라 계산
                    # 버튼의 y 위치를 주차에 따라 계산
                    # y_position = 50 + 50 * week_num
                    button_text = str(day) + '\n'
                    for match in self.month_match[day]:
                        button_text = button_text + match[1] + '\n'
                        # button_text = button_text + match[1] + '\n'
                    # 버튼 생성
                    self.CalendarButton[week_num][day_num]['text'] = button_text
                    self.CalendarButton[week_num][day_num].grid()
                    # btn = Button(frame, text=button_text, width=15, height=6)
                    # btn.grid(row=week_num, column=day_num, padx=(x_position, 0), pady=(y_position, 0))

                    # 버튼에 요일 이름 표시
                if week_num == 0:
                    label = Label(frame, text=weekdays[day_num])
                    label.grid(row=0, column=day_num, padx=(x_position, 0), sticky="n")


    def decreaseYear(self):
        self.year -= 1
        self.readMonthData()
        self.setCalendar(self.달력프레임)
        self.selectedYM['text'] = str(self.year) + "년 " + str(self.month) + "월"

    def decreaseMonth(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1
        self.readMonthData()
        self.setCalendar(self.달력프레임)
        self.selectedYM['text'] = str(self.year) + "년 " + str(self.month) + "월"

    def increaseMonth(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1
        self.readMonthData()
        self.setCalendar(self.달력프레임)
        self.selectedYM['text'] = str(self.year) + "년 " + str(self.month) + "월"

    def increaseYear(self):
        self.year += 1
        self.readMonthData()
        self.setCalendar(self.달력프레임)
        self.selectedYM['text'] = str(self.year) + "년 " + str(self.month) + "월"

    def __init__(self):
        window = Tk()
        window.title('국내 축구 경기 일정')

        # 달력 생성
        self.CalendarButton = []
        Calendar_frame = Frame(window)
        Calendar_frame.pack(side=LEFT)

        self.year = 2024
        self.month = 5

        self.달력프레임 = Frame(Calendar_frame)
        self.달력프레임.pack(side=TOP)
        self.readMonthData()
        self.setCalendar(self.달력프레임)

        cFrame2 = Frame(Calendar_frame)
        cFrame2.pack(side=TOP)
        Button(cFrame2, text='◀◀', command=self.decreaseYear).pack(side=LEFT)
        Button(cFrame2, text='◀', command=self.decreaseMonth).pack(side=LEFT)
        self.selectedYM = Label(cFrame2, text=str(self.year) + "년 " + str(self.month) + "월")
        self.selectedYM.pack(side=LEFT)
        Button(cFrame2, text='▶', command=self.increaseMonth).pack(side=LEFT)
        Button(cFrame2, text='▶▶', command=self.increaseYear).pack(side=LEFT)

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
