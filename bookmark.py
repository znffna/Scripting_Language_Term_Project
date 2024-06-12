import threading
from tkinter import *
from tkinter import font, simpledialog

import pickle

import requests

import MonthCalendar


class Bookmark:
    def __init__(self, main, mainframe):
        self.main = main  # MainGUI와의 연결

        self.titlefont = font.Font(mainframe, size=30, weight='bold', family='Consolas')

        # 즐겨찾기한 팀 목록 리스트 박스 생성
        self.bookmarkFrame = Frame(mainframe)
        self.bookmarkFrame.pack(side=LEFT)

        Label(self.bookmarkFrame, text='즐겨찾기 팀', font=self.titlefont).pack(side=TOP)

        listboxframe = Frame(self.bookmarkFrame)
        listboxframe.pack(side=TOP)

        self.bookmark_listbox = Listbox(listboxframe, width=60, height=20)
        self.bookmark_listbox.pack(side=LEFT)

        # 스크롤 바 생성
        scrollbar = Scrollbar(listboxframe)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤 바와 리스트 박스 연결
        self.bookmark_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.bookmark_listbox.yview)

        self.bookmark_listbox.bind('<Double-Button-1>', self.findRecentlyMatch)

        # 추가 / 삭제를 위한 버튼
        buttonFrame = Frame(self.bookmarkFrame)
        buttonFrame.pack(side=TOP)
        self.Badd = Button(buttonFrame, text='+', command=self.addTeam)
        self.Badd.pack(side=LEFT)
        self.Bremove = Button(buttonFrame, text='-', command=self.removeTeam)
        self.Bremove.pack(side=LEFT)

        # 저장되어있던 즐겨찾기 리스트를 불러온다.
        self.bookmarkList = []
        self.loadBookmark()

        for team in self.bookmarkList:
            self.bookmark_listbox.insert(END, team)

        ##############################################################################
        # 즐겨찾기된 팀의 현재 달을 포함한 이전달, 다음 달의 경기 예정 및 결과 출력 listbox 생성 #
        ##############################################################################
        listboxframe = Frame(mainframe)
        listboxframe.pack(side=LEFT)

        self.match_listbox = Listbox(listboxframe, width=60, height=20)
        self.match_listbox.pack(side=LEFT)

        # 스크롤 바 생성
        scrollbar = Scrollbar(listboxframe)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤 바와 리스트 박스 연결
        self.match_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.match_listbox.yview)

    def findRecentlyMatch(self, event):
        widget = event

        year = MonthCalendar.year
        month = MonthCalendar.month
        monthlist = [(year + (month + i) // 13, (month + i - 1) % 12 + 1) for i in range(3)]

        print(monthlist)
        self.match_listbox.delete(0, END)

        selection = self.bookmark_listbox.curselection()
        if selection:
            selection = self.bookmark_listbox.curselection()[0]
        else:
            return

        target = self.bookmarkList[selection]
        threading.Thread(target=self.updateMatchlist, args=(monthlist, target), daemon=True).start()
        # for (year, month) in monthlist:
        #     # threading.Thread(target=self.readMonthData, args=(year, month, target), daemon=True).start()
        #     self.readMonthData(year, month, target)

    def updateMatchlist(self, monthlist, target):
        for (year, month) in monthlist:
            # threading.Thread(target=self.readMonthData, args=(year, month, target), daemon=True).start()
            self.readMonthData(year, month, target)

    def readMonthData(self, year, month, target):
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
                # print(Text)
            for word in node_info[1].split(' '):
                if target == word:
                    self.month_match[day].append(node_info)
                    break

        for day, gamelist in self.month_match.items():
            for game in gamelist:
                self.match_listbox.insert(END, str(year) + '-' + str(month) + '-' + str(day) + ' ' + game[1])
            # self.match_listbox.itemconfig(self.match_listbox.size() - 1, fg=fg)

        # 디버그용 출력
        # for days, matches in self.month_match.items():
        #     print(days)
        #     for match in matches:
        #         print(match)
        #     print()
        pass

    def addTeam(self):
        team_name = simpledialog.askstring('즐겨찾기에 팀 추가', "팀 이름 입력:", parent=self.main.window)
        if not team_name:
            return
        self.addBookmark(team_name)

    def removeTeam(self):
        iSearchIndex = self.bookmark_listbox.curselection()
        if iSearchIndex:
            iSearchIndex = self.bookmark_listbox.curselection()[0]
        else:
            return
        self.bookmarkList.pop(iSearchIndex)
        self.updateBookmarkList()

    def pressedBookmark(self, target):
        if target not in self.bookmarkList:
            self.addBookmark(target)
        else:
            self.removeBookmark(target)

    def saveBookmark(self):
        # 데이터를 파일에 저장
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.bookmarkList, f)

    def loadBookmark(self):
        # 파일에서 데이터를 로드
        with open('data.pickle', 'rb') as f:
            self.bookmarkList = pickle.load(f)

    def addBookmark(self, target):  # 팀 이름이 target에 들어옴. (ex : '삼성')
        if target not in self.bookmarkList:
            # print(target, "이 bookmark에 추가됨")
            self.bookmarkList.append(target)
            self.saveBookmark()
            self.updateBookmarkList()

    def removeBookmark(self, target):  # 팀 이름이 target에 들어옴. (ex : '삼성')
        if target in self.bookmarkList:
            # print(target, "이 bookmark에서 제거됨")
            self.bookmarkList.remove(target)
            self.saveBookmark()
            self.updateBookmarkList()

    def updateBookmarkList(self):
        self.bookmark_listbox.delete(0, END)

        for team in self.bookmarkList:
            self.bookmark_listbox.insert(END, team)

    def isBookmark(self, target):
        if target in self.bookmarkList:
            return True
        return False

    def pickle(self):
        # 저장할 데이터
        data = {'name': 'Alice', 'age': 30, 'city': 'New York'}

        # 데이터를 파일에 저장
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

        # 파일에서 데이터를 로드
        with open('data.pickle', 'rb') as f:
            loaded_data = pickle.load(f)

        print("Loaded data:", loaded_data)


if __name__ == '__main__':
    namelist = ['삼성']
    with open('data.pickle', 'wb') as f:
        pickle.dump(namelist, f)
