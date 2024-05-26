from datetime import datetime
from tkinter import *
from tkinter import font
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
        # 실제 경기 내용이 저장되는 공간
        self.month_match = {}  # {day : [한 경기], [한 경기], day : [한 경기], ..., ...}

        # 달력을 출력하기 위한 프레임
        self.달력프레임 = Frame(Calendar_frame)
        self.달력프레임.pack(side=TOP)
        self.MonthCalendar = MonthCalendar.MonthCalendar(self, self.달력프레임, self.month_match)

        # 달력 제어 컨트롤 객체
        cFrame2 = Frame(Calendar_frame)
        cFrame2.pack(side=TOP)
        self.MonthController = MonthCalendar.MonthController(cFrame2, self.MonthCalendar)

        pass

    def readTodayData(self):
        # print('MonthCalendar 의 readMonthData - ', year, '년 ',  month, '월')
        srId_encoded = '0%2C1%2C3%2C4%2C5%2C7'
        srId_decoded = urllib.parse.unquote(srId_encoded)
        today_data = {
            'leId': 1,
            'srId': '0,1,3,4,5,7,9',
            'Date': MonthCalendar.year * 10000 + MonthCalendar.month * 100 + MonthCalendar.day,
        }
        res = requests.post('https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList', data=today_data)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        print(res.status_code)
        print(res.json())
        pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        print(pretty_json)

        self.today_match = {}
        day = 1
        for game in res.json()['gameList']:
            # 1. stadium (경기장)
            # 2. stadiumFullName (경기장 이름)
            # 3. homeCode (홈 팀)
            # 4. homeName (홈 풀네임)
            # 5. awayCode (어웨이 팀)
            # 6. awayName (어웨이 풀네임)
            # 7. gameTime (시작 시간)
            # 8. 구장
            # 9. 비고
            node_info = []
            # print(info)
            for node in game:
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

    def readMatchData(self):
        # print('MonthCalendar 의 readMonthData - ', year, '년 ',  month, '월')
        today_data = {
            'leId': 1,
            'srId': '0,1,3,4,5,7,9',
            'Date': MonthCalendar.year * 10000 + MonthCalendar.month * 100 + MonthCalendar.day,
        }
        # print(today_data)
        res = requests.post('https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList', data=today_data)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        # print(res.status_code)
        # pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        # print(pretty_json)

        self.match_listbox.delete(0, END)

        self.match_list = []
        day = 1
        for game in res.json()['game']:
            self.match_list.append(game)
            # print(type(game))
            # 1. LE_ID                      X
            # 2. SR_ID                      X
            # 3. SEASON_ID (시즌 년도)        X
            # 4. G_DT (날짜)                 X
            # 5. G_DT_TXT (날짜를 풀어서)      X
            # 6. G_ID (경기 ID)              X
            # 7. HEADER_NO                  X
            # 8. G_TM (경기 시작시간)         O
            # 9. S_NM (경기장 위치)          O
            # 10. AWAY_ID (어웨이 팀 ID)       X
            # 11. HOME_ID (홈 팀 ID)          X
            # 12. AWAY_NM (어웨이 팀 이름)    -----------O
            # 13. HOME_NM (홈 팀 이름)      ------------O
            # T_PIT_P_ID (어웨이 팀 투수)
            # T_PIT_P_NM (어웨이 팀 투수 이름)
            # B_PIT_P_ID (홈 팀 투수 이름)
            # B_PIT_P_NM (홈 팀 투수 이름)
            # GAME_STATE_SC (게임 상태)
            # GAME_INN_NO (게임 진행 상황 - 몇 회인가(5))         O
            # GAME_TB_SC (게임 진행 상황 이름 - 초(T)/말(B))
            # GAME_TB_SC_NM (게임 진행 상황 이름 - 초/말 (말))     O
            # T_SCORE_CN (어웨이팀 점수)     --------------- O
            # B_SCORE_CN (홈팀 점수)        --------------- O
            # VS_GAME_CN (게임 카운트(1회초 끝나면 1번, 1회말 끝나면 1번, 5회 말 중이면 9))
            # STRIKE_CN (스트라이크 카운트)
            # BALL_CN (볼 카운트)
            # OUT_CN (아웃 카운트)
            # B1_BAT_ORDER_NO (1번 타자 번호)
            # B2_BAT_ORDER_NO (2번 타자 번호)
            # B3_BAT_ORDER_NO (3번 타자 번호)
            inform_match = str(game['AWAY_NM']) + ' ' + str(game['T_SCORE_CN']) + ' vs ' + \
                           str(game['B_SCORE_CN']) + ' ' + str(game['HOME_NM'])
            self.match_listbox.insert(END, inform_match)

        # 디버그용 출력
        # for days, matches in self.month_match.items():
        #     print(days)
        #     for match in matches:
        #         print(match)
        #     print()

    def search_a_match(self):
        iSearchIndex = self.match_listbox.curselection()
        if iSearchIndex:
            iSearchIndex = self.match_listbox.curselection()[0]
        else:
            return
        select_game = self.match_list[iSearchIndex]

        self.updateMatchInformation(select_game)
        pass

    def createMatchList(self, frame1):
        list_frame = Frame(frame1)
        list_frame.pack(side=LEFT)

        listbox_frame = Frame(list_frame)
        listbox_frame.pack(side=TOP)

        # 경기 목록 리스트 박스 생성
        self.match_listbox = Listbox(listbox_frame, width=60)
        self.match_listbox.pack(side=LEFT)

        # 스크롤 바 생성
        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤 바와 리스트 박스 연결
        self.match_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.match_listbox.yview)
        # 리스트 갱신
        self.readMatchData()

        # 리스트 갱신을 요청하는 버튼 생성
        search_btn = Button(list_frame, text='검색', command=self.search_a_match)
        search_btn.pack(side=TOP)

        # self.match_list.insert(END, '넣고 싶은 내용 입력')

    def loadimage(self, url):
        if url is not None:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()

            im = Image.open(BytesIO(raw_data))
            return ImageTk.PhotoImage(im)
        else:
            return None

    def createMatchInformation(self, frame):
        inform_main = Frame(frame)
        inform_main.pack(side=LEFT)

        summary_frame = Frame(inform_main)
        summary_frame.pack(side=TOP)

        # 어웨이팀 출력

        away_frame = Frame(summary_frame)
        away_frame.pack(side=LEFT)

        # 12. AWAY_NM (어웨이 팀 이름)    -----------O
        # 13. HOME_NM (홈 팀 이름)      ------------O

        self.away_team_image = None

        self.LAwayTeamImage = Label(away_frame, image=self.away_team_image, height=40, width=40)
        self.LAwayTeamImage.pack()

        self.LAwayTeamName = Label(away_frame, text='', font=self.fontstyle, fg='cyan')
        self.LAwayTeamName.pack()

        # 홈 팀 출력

        home_frame = Frame(summary_frame)
        home_frame.pack(side=RIGHT)

        self.home_team_image = None

        self.LHomeTeamImage = Label(home_frame, image=self.home_team_image, height=40, width=40)
        self.LHomeTeamImage.pack(side=TOP)

        self.LHomeTeamName = Label(home_frame, text='', font=self.fontstyle, fg='magenta')
        self.LHomeTeamName.pack(side=TOP)

        self.LVersus = Label(summary_frame, text='  VS  ', font=self.fontstyle, fg='black')
        self.LVersus.pack(side=LEFT)
        pass

    def updateMatchInformation(self, selectgame):
        self.away_team_image = \
            self.loadimage(team_image_url[selectgame['AWAY_NM']])
        self.LAwayTeamImage.configure(image=self.away_team_image)

        self.home_team_image = \
            self.loadimage(team_image_url[selectgame['HOME_NM']])
        self.LHomeTeamImage.configure(image=self.home_team_image)

        self.LAwayTeamName.configure(text=selectgame['AWAY_NM'])
        self.LHomeTeamName.configure(text=selectgame['HOME_NM'])

        # T_SCORE_CN (어웨이팀 점수)     --------------- O
        # B_SCORE_CN (홈팀 점수)        --------------- O
        self.LVersus.configure(text="   " + str(selectgame['T_SCORE_CN'] + "  VS  " + str(selectgame['B_SCORE_CN'])
                                                + "   " ))

    def __init__(self):

        # 오늘의 년/월 을 할당하는 변수
        now = datetime.now()
        MonthCalendar.year = now.year
        MonthCalendar.month = now.month
        MonthCalendar.day = now.day

        # 윈도우 생성
        window = Tk()
        window.title('국내 축구 경기 일정')

        # 폰트 생성
        self.fontstyle = font.Font(window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(window, size=16, weight='bold', family='Consolas')

        # 달력 생성
        self.createCalendar(window)

        # Notebook 생성
        세부정보 = Frame(window)
        세부정보.pack()
        notebook = tkinter.ttk.Notebook(세부정보, width=width, height=height)
        notebook.pack(side=LEFT)

        frame1 = Frame(세부정보)
        notebook.add(frame1, text='경기 일정')
        self.createMatchList(frame1)
        self.createMatchInformation(frame1)

        frame2 = Frame(세부정보)
        notebook.add(frame2, text='날씨 정보')
        Short_weather.create_weather_frame(frame2)
        # Label(frame2, text='페이지2의 내용',
        #       fg='blue', font='helvetica 48').pack()

        frame3 = Frame(세부정보)
        notebook.add(frame3, text='경기장')
        Label(frame3, text='페이지3의 내용',
              fg='orange', font='helvetica 48').pack()

        frame4 = Frame(세부정보)
        notebook.add(frame4, text='즐겨찾기 관리')
        Label(frame4, text='페이지4의 내용',
              fg='yellow', font='helvetica 48').pack()
        window.mainloop()

    def pressDay(self):
        print(MonthCalendar.day, '일 선택됨')
        self.readMatchData()


if __name__ == '__main__':
    MainGUI()
