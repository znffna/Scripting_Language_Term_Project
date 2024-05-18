from tkinter import *
import tkinter.ttk

import requests
import json

import calendar

width = 1280
height = 720

year = 2024
month = 5



class MainGUI:

    def readMonthData(self):
        month_data = {  # 'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'leId': 1,
            'srIdList': '0,9,6',
            'seasonId': year,
            'gameMonth': str(month).zfill(2),
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
        cal = calendar.monthcalendar(year, month)
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                x_position = 20
                # x_position = 20 * day_num
                if day != 0:
                    # 버튼의 x 위치를 요일에 따라 계산
                    # 버튼의 y 위치를 주차에 따라 계산
                    y_position = 20
                    # y_position = 50 + 50 * week_num
                    button_text = str(day) + '\n'
                    for match in self.month_match[day]:
                        button_text = button_text + match[1] + '\n'
                        # button_text = button_text + match[1] + '\n'
                    # 버튼 생성
                    btn = Button(frame, text=button_text, width=15, height=6)
                    btn.grid(row=week_num, column=day_num, padx=(x_position, 0), pady=(y_position, 0))

                    # 버튼에 요일 이름 표시
                if week_num == 0:
                    label = Label(frame, text=weekdays[day_num])
                    label.grid(row=0, column=day_num, padx=(x_position, 0), sticky="n")

        # for day in self.month_match:
        #     print(day[0])
        #     row = weekdays.index(day[0][-2])
        #     button = Button(frame, text = day, width=5, height=2)
        #     button.grid(row =row)
        #


        # Label(frame, text='페이지1의 내용',
        #       fg='red', font='helvetica 48').pack(side=TOP)
        # Label(frame, text='blah blah',
        #       fg='red', font='helvetica 48').pack(side=TOP)
        pass

    def __init__(self):
        window = Tk()
        window.title('국내 축구 경기 일정')
        notebook = tkinter.ttk.Notebook(window, width=width, height=height)
        notebook.pack()

        self.readMonthData()
        frame1 = Frame(window)
        notebook.add(frame1, text='경기 일정')
        self.setCalendar(frame1)

        frame2 = Frame(window)
        notebook.add(frame2, text='날씨 정보')
        Label(frame2, text='페이지2의 내용',
              fg='blue', font='helvetica 48').pack()

        frame3 = Frame(window)
        notebook.add(frame3, text='경기장')
        Label(frame3, text='페이지3의 내용',
              fg='orange', font='helvetica 48').pack()

        frame4 = Frame(window)
        notebook.add(frame4, text='즐겨찾기 관리')
        Label(frame4, text='페이지4의 내용',
              fg='yellow', font='helvetica 48').pack()
        window.mainloop()


if __name__ == '__main__':
    MainGUI()
