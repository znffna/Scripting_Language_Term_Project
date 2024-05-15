from tkinter import *
import tkinter.ttk

import requests
import json

width = 800
height = 600

month_data = {  # 'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'leId': 1,
    'srIdList': '0,9,6',
    'seasonId': 2024,
    'gameMonth': '05',
    'teamID': ''
}

class MainGUI:

    def readMonthHTML(self):
        res = requests.post('https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList', data=month_data)
        res.encoding = 'utf-8'
        print(res.status_code)
        # print(res.json())
        # pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        # print(pretty_json)
        self.month_match = []  # [[day, [한 경기], [한 경기]], [day, [한 경기], ...], ...]
        for game in res.json()['rows']:
            info = game["row"]
            node_info = []
            # print(info)
            for node in info:
                if str(node['Class']) == 'day':
                    self.month_match.append([])
                    self.month_match[-1].append(str(node['Text']))
                    continue
                Text = str(node['Text'])
                Text = Text.replace('class="win"', ' win ')
                Text = Text.replace('class="lose"', ' lose ')
                Text = Text.replace('<b>', '')
                Text = Text.replace('</b>', '')
                Text = Text.replace('<', '')
                Text = Text.replace('>', '')
                Text = Text.replace('/', '')
                Text = Text.replace('span', '')
                Text = Text.replace('em', ' ')

                # print(str(node['Class']) + " : " + Text)
                node_info.append(Text)
                # print(str(node['Class']) + " : " + str(node['Text']))
            # 1. 날짜
            # 2. 시간
            # 3. 경기
            # 4. 게임센터
            # 5. 하이라이트
            # 6. TV
            # 7. 라디오
            # 8. 구장
            # 9. 비고
            self.month_match[-1].append(node_info)
        for day in self.month_match:
            print(day)
            print()
            print()
        pass

    def setCalendar(self, frame):
        Label(frame, text='페이지1의 내용',
              fg='red', font='helvetica 48').pack(side=TOP)
        Label(frame, text='blah blah',
              fg='red', font='helvetica 48').pack(side=TOP)
        pass

    def __init__(self):
        window = Tk()
        window.title('국내 축구 경기 일정')
        notebook = tkinter.ttk.Notebook(window, width=width, height=height)
        notebook.pack()

        self.readMonthHTML()
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
