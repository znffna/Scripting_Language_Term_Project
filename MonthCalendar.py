from tkinter import Button, Label, LEFT
import calendar

import requests
import json



year = 2024
month = 5
day = 26

x_position = 20
y_position = 20


class MonthCalendar:

    def readMonthData(self):
        # print('MonthCalendar 의 readMonthData - ', year, '년 ',  month, '월')
        month_data = {  # 'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'leId': 1,
            'srIdList': '0,9,6',
            'seasonId': year,
            'gameMonth': str(month).zfill(2),
            'teamID': ''
        }
        res = requests.post('https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList', data=month_data)
        res.encoding = 'utf-8'
        # print(res.status_code)
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
        # for days, matches in self.month_match.items():
        #     print(days)
        #     for match in matches:
        #         print(match)
        #     print()
        pass

    def setCalendar(self):
        weekdays = ('일', '월', '화', '수', '목', '금', '토')
        calendar.setfirstweekday(calendar.SUNDAY)
        self.cal = calendar.monthcalendar(year, month)

        for week in self.CalendarButton:
            for day in self.CalendarButton:
                for button in day:
                    button.grid_remove()

        for week_num, week in enumerate(self.cal):
            for day_num, day in enumerate(week):
                # x_position = 20 * day_num
                if day != 0:
                    # 버튼의 x 위치를 요일에 따라 계산
                    # 버튼의 y 위치를 주차에 따라 계산
                    # y_position = 50 + 50 * week_num
                    button_text = str(day) + '\n'
                    if self.month_match[day]:
                        button_text += str(len(self.month_match[day])) + " 경기"
                    # for match in self.month_match[day]:
                    #     button_text = button_text + match[1] + '\n'
                    # button_text = button_text + match[1] + '\n'
                    # 버튼 생성
                    self.CalendarButton[week_num][day_num]['text'] = button_text
                    self.CalendarButton[week_num][day_num].grid()
                    # btn = Button(frame, text=button_text, width=15, height=6)
                    # btn.grid(row=week_num, column=day_num, padx=(x_position, 0), pady=(y_position, 0))
                else:
                    self.CalendarButton[week_num][day_num].grid_remove()

                    # 버튼에 요일 이름 표시
                if week_num == 0:
                    label = Label(self.frame, text=weekdays[day_num])
                    label.grid(row=0, column=day_num, padx=(x_position, 0), sticky="n")


    def updateCalendar(self):
        self.readMonthData()
        self.setCalendar()

    def pressDay(self, row, col):
        # print('button pressed', row, col)
        # print('day = ', self.cal[row][col])
        global day
        day = self.cal[row][col]
        self.GUI.refresh()

    def __init__(self, main, frame, month_match):
        self.GUI = main
        self.frame = frame
        self.month_match = month_match
        self.CalendarButton = []
        for week_num in range(6):
            self.CalendarButton.append([])
            for day_num in range(7):
                btn = Button(self.frame, text='', width=6, height=2,
                             command= lambda row=week_num, col=day_num: self.pressDay(row, col))
                btn.grid(row=week_num, column=day_num, padx=(x_position, 0), pady=(y_position, 0))
                btn.grid_remove()
                self.CalendarButton[week_num].append(btn)

        self.readMonthData()
        self.setCalendar()


class MonthController:
    def update(self):
        self.selectedYM['text'] = str(year) + "년 " + str(month) + "월"
        self.MonthCalendar.updateCalendar()

    def decreaseYear(self):
        global month, year
        year -= 1
        self.update()

    def decreaseMonth(self):
        global month, year
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1

        self.update()

    def increaseMonth(self):
        global month, year
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        self.update()

    def increaseYear(self):
        global month, year
        year += 1
        self.update()

    @property
    def year(self):
        return self.MonthCalendar.year

    @year.setter
    def year(self, value):
        self.MonthCalendar.year = value
        self.update()

    @property
    def month(self):
        return self.MonthCalendar.month

    @month.setter
    def month(self, value):
        self.MonthCalendar.month = value
        self.update()

    def __init__(self,  frame, monthcalendar):
        self.MonthCalendar = monthcalendar

        Button(frame, text='◀◀', command=self.decreaseYear).pack(side=LEFT)
        Button(frame, text='◀', command=self.decreaseMonth).pack(side=LEFT)
        self.selectedYM = Label(frame, text=str(year) + "년 " + str(month) + "월")
        self.selectedYM.pack(side=LEFT)
        Button(frame, text='▶', command=self.increaseMonth).pack(side=LEFT)
        Button(frame, text='▶▶', command=self.increaseYear).pack(side=LEFT)

