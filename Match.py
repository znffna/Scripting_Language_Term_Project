from tkinter import *
from tkinter import font

import requests
import json
import urllib.parse

from io import BytesIO
import urllib
from PIL import Image, ImageTk

import MonthCalendar


# 선택된 경기의 모든 정보를 읽어와 '경기 정보' 탭에 출력
class Match:
    # self.match_list = 모든 경기 내용 저장
    # self.match_listbox = 경기 ListBox 작성
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

    # 선택된 날짜의 모든 경기정보를 읽어오고 self.match_list에 저장, ListBox를 갱신
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
        pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        print(pretty_json)

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
            self.match_listbox.insert(END, inform_match)  #

    # 리스트에서 선택된 경기로 갱신
    def pressedSearch(self):
        iSearchIndex = self.match_listbox.curselection()
        if iSearchIndex:
            iSearchIndex = self.match_listbox.curselection()[0]
        else:
            return
        select_game = self.match_list[iSearchIndex]

        self.updateMatchInform(select_game)
        pass

    # url을 통해 이미지를 load
    def loadimage(self, url):
        if url is not None:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()

            im = Image.open(BytesIO(raw_data))
            return ImageTk.PhotoImage(im)
        else:
            return None

    # MatchList를 갱신
    def updateMatchList(self):
        self.readMatchData()
        pass

    # 선택된 경기로 정보 갱신(self.match_list 에서 1경기를 가져와 갱신한다)
    def updateMatchInform(self, selectgame):
        self.LMatchDate.configure(text=selectgame['G_DT_TXT'])
        # 어웨이 갱신
        self.away_team_image = \
            self.loadimage(Match.team_image_url[selectgame['AWAY_NM']])  # 참조가 있어야 가비지 콜렉터를 막을 수 있다.
        self.LAwayTeamImage.configure(image=self.away_team_image)

        # 홈 갱신
        self.home_team_image = \
            self.loadimage(Match.team_image_url[selectgame['HOME_NM']])  # 참조가 있어야 가비지 콜렉터를 막을 수 있다.
        self.LHomeTeamImage.configure(image=self.home_team_image)

        self.LAwayTeamName.configure(text=selectgame['AWAY_NM'])
        self.LHomeTeamName.configure(text=selectgame['HOME_NM'])

        # T_SCORE_CN (어웨이팀 점수)     --------------- O
        # B_SCORE_CN (홈팀 점수)        --------------- O
        self.LVersus.configure(text="   " + str(selectgame['T_SCORE_CN'] + "  VS  " + str(selectgame['B_SCORE_CN'])
                                                + "   "))

    # 하루치 경기 리스트를 출력할 frame 생성
    def createMatchList(self, frame):
        list_frame = Frame(frame)
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
        search_btn = Button(list_frame, text='검색', command=self.pressedSearch)
        search_btn.pack(side=TOP)

        # self.match_list.insert(END, '넣고 싶은 내용 입력')

    # 선택된 경기를 출력하는 frame 생성
    def createMatchInform(self, frame):
        inform_main = Frame(frame)
        inform_main.pack(side=LEFT)

        data = str(MonthCalendar.year) + '년 ' + str(MonthCalendar.month) + '월 ' + str(MonthCalendar.day) + '일'
        self.LMatchDate = Label(inform_main, text=data, font=self.fontstyle, fg='black')
        self.LMatchDate.pack(side=TOP)

        summary_frame = Frame(inform_main)
        summary_frame.pack(side=TOP)

        # 어웨이팀 출력

        away_frame = Frame(summary_frame)
        away_frame.pack(side=LEFT)

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

        self.LVersus = Label(summary_frame, text='', font=self.fontstyle, fg='black')
        self.LVersus.pack(side=LEFT)

        
        self.readScoreBoard()
        self.readBoxScore()

        pass

    def __init__(self, frame):
        # 폰트 생성
        self.fontstyle = font.Font(frame, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(frame, size=16, weight='bold', family='Consolas')

        self.createMatchList(frame)
        self.createMatchInform(frame)

    def readScoreBoard(self):
        scoreboardURL = 'https://www.koreabaseball.com/ws/Schedule.asmx/GetScoreBoardScroll'
        scoreboardData = {
            'leId': 1,
            'srId': 0,
            'seasonId': 2024,
            'gameId': '20240529LGSK0'
        }
        self.scoreboard = []

        res = requests.post(scoreboardURL, data=scoreboardData)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        # print(res.status_code)
        pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        print(pretty_json)


    def readBoxScore(self):
        boxscoreURL = 'https://www.koreabaseball.com/ws/Schedule.asmx/GetBoxScoreScroll'
        boxscoreData = {
            'leId': 1,
            'srId': 0,
            'seasonId': 2024,
            'gameId': '20240529LGSK0'
        }
        self.boxscore = []

        res = requests.post(boxscoreURL, data=boxscoreData)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        # print(res.status_code)
        pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        print(pretty_json)


