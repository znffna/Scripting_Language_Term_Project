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

        self.canvas.delete('graph')

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
        away_win = selectgame['T_SCORE_CN'] == selectgame['B_SCORE_CN']
        # 점수를 갱신
        self.LAwayScore.configure(text=str(selectgame['T_SCORE_CN']))
        self.LHomeScore.configure(text=str(selectgame['B_SCORE_CN']))
        # 승패에 따른 점수 색상 갱신
        if away_win:
            self.LAwayScore.configure(fg='black')
            self.LHomeScore.configure(fg='black')
        elif selectgame['T_SCORE_CN'] > selectgame['B_SCORE_CN']:
            self.LAwayScore.configure(fg='red')
            self.LHomeScore.configure(fg='blue')
        else:
            self.LAwayScore.configure(fg='blue')
            self.LHomeScore.configure(fg='red')

        self.LVersus.configure(text="     VS     ")

        self.readScoreBoard(selectgame)
        self.readBoxScore(selectgame)

    # 하루치 경기 리스트를 출력할 frame 생성
    def createMatchList(self, frame):
        list_frame = Frame(frame)
        list_frame.pack(side=LEFT)

        listbox_frame = Frame(list_frame)
        listbox_frame.pack(side=TOP)

        # 경기 목록 리스트 박스 생성
        self.match_listbox = Listbox(listbox_frame, width=60, height=20)
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
        inform_main.pack(side=LEFT, expand=True, fill=BOTH)

        data = str(MonthCalendar.year) + '년 ' + str(MonthCalendar.month) + '월 ' + str(MonthCalendar.day) + '일'
        self.LMatchDate = Label(inform_main, text=data, font=self.fontstyle, fg='black')
        self.LMatchDate.pack(side=TOP)

        summary_frame = Frame(inform_main)
        summary_frame.pack(side=TOP, fill=X)

        # 어웨이팀 출력

        away_frame = Frame(summary_frame)
        away_frame.pack(side=LEFT, anchor=W)

        self.LAwayScore = Label(away_frame, text='', font=self.fontScore, fg='black')
        self.LAwayScore.pack(side=RIGHT, padx=100)

        self.LAwayTeamImage = Label(away_frame, height=40, width=40)
        self.LAwayTeamImage.pack()

        self.LAwayTeamName = Label(away_frame, text='', font=self.fontstyle, fg='black')  # cyan
        self.LAwayTeamName.pack()

        # 홈 팀 출력

        home_frame = Frame(summary_frame)
        home_frame.pack(side=RIGHT, anchor=E)

        self.LHomeScore = Label(home_frame, text='', font=self.fontScore, fg='black')
        self.LHomeScore.pack(side=LEFT, padx=100)

        self.LHomeTeamImage = Label(home_frame, height=40, width=40)
        self.LHomeTeamImage.pack(side=TOP)

        self.LHomeTeamName = Label(home_frame, text='', font=self.fontstyle, fg='black')  # magenta
        self.LHomeTeamName.pack(side=TOP)

        # Versus 출력
        self.LVersus = Label(summary_frame, text='', font=self.fontstyle, fg='black')
        self.LVersus.pack(anchor=S)

        # 경기 결과 출력
        scoreboard_frame = Frame(inform_main)
        scoreboard_frame.pack(side=TOP)
        self.indexboard = ['TEAM', '', '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                           'R', 'H', 'E', 'B']
        self.scoreboard = [[] for _ in range(3)]  # 경기 출력할 결과 저장  [[idx][away_team][home_team]]
        self.LScoreboard = [[] for _ in range(3)]  # [[idx][away_team][home_team]]
        for row in range(3):
            for col in range(21):
                label = Label(scoreboard_frame, text='', font=self.fontstyle3, fg='black')
                label.grid(row=row, column=col, padx=(5, 0), sticky='EW')
                self.LScoreboard[row].append(label)

        # 경기 결과를 그래프로 출력
        graph_frame = Frame(inform_main)
        graph_frame.pack(side=TOP)

        self.canvas = Canvas(graph_frame, width=600, height=300, bg='white')
        self.canvas.pack()

    def __init__(self, frame):
        self.frame = Frame(frame)
        self.frame.pack(side=LEFT)

        # 폰트 생성
        self.fontstyle = font.Font(self.frame, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.frame, size=16, weight='bold', family='Consolas')
        self.fontstyle3 = font.Font(self.frame, size=13, weight='bold', family='Consolas')
        self.fontScore = font.Font(self.frame, size=30, weight='bold', family='Consolas')

        self.createMatchList(self.frame)
        self.createMatchInform(self.frame)
        self.updateScoreBoard()

    def readScoreBoard(self, selectgame):
        scoreboardURL = 'https://www.koreabaseball.com/ws/Schedule.asmx/GetScoreBoardScroll'
        scoreboardData = {
            'leId': 1,
            'srId': 0,
            'seasonId': selectgame['SEASON_ID'],
            'gameId': selectgame['G_ID']
        }

        res = requests.post(scoreboardURL, data=scoreboardData)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        # print(res.status_code)
        # pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        # print("읽어온 순수 데이터 : ", pretty_json)
        status = res.json()['code']
        if status != '100':
            if status == '200':
                print("해당 경기가 종료되지 않았음")
                self.resetScoreBoard()
                return
            else:
                print("error code =", res.json()['code'])
                return

        table1 = res.json()['table1'].replace('\r\n', '')
        table2 = res.json()['table2'].replace('\r\n', '')
        table3 = res.json()['table3'].replace('\r\n', '')

        dict1 = json.loads(table1)
        dict2 = json.loads(table2)
        dict3 = json.loads(table3)

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

        # print(dict1)
        # print(dict3)
        # print(dict2)
        # pretty_json = json.dumps(dict1, indent=4, ensure_ascii=False)
        # print(pretty_json)

        index_score1 = []

        away_score1 = []
        home_score1 = []
        # away_score1.append(selectgame['G_DT'])  # 경기 일자
        # away_score1.append(selectgame['SEASON_ID'])  # 시즌

        away_score1.append(selectgame['AWAY_NM'])  # 원정팀 이름
        a = dict1['rows'][0]['row'][1]['Text'].split('>')[3]
        away_score1.append(a)  # 원정팀 현재 기록
        b = dict1['rows'][0]['row'][0]['Text']
        away_score1.append(b)  # 원정팀 해당경기 승/패

        # home_score1.append(selectgame['G_DT'])
        # home_score1.append(selectgame['SEASON_ID'])
        home_score1.append(selectgame['HOME_NM'])  # 홈팀 이름

        a = dict1['rows'][1]['row'][1]['Text'].split('>')[3]
        home_score1.append(a)  # 홈팀 현재 기록
        b = dict1['rows'][1]['row'][0]['Text']
        home_score1.append(b)  # 홈팀 해당경기 승/패

        index_score2 = []
        away_score2 = []
        home_score2 = []

        for i in range(0, 12):
            idx = dict2['headers'][0]['row'][i]['Text']
            index_score2.append(idx)
            a = dict2['rows'][0]['row'][i]['Text']
            away_score2.append(a)
            b = dict2['rows'][1]['row'][i]['Text']
            home_score2.append(b)

        away_score3 = []
        home_score3 = []
        for i in range(0, 4):  # 스코어, 안타수, 에러수, 볼넷 수 반복문
            a = dict3['rows'][0]['row'][i]['Text']
            away_score3.append(a)
            b = dict3['rows'][1]['row'][i]['Text']
            home_score3.append(b)
        # print(away_score1, '\n', away_score2, '\n', away_score3)
        # print(home_score1, '\n', home_score2, '\n', home_score3)
        # print(index_score2)
        # score_board1 = pd.DataFrame([away_score1, home_score1], columns=['Date', 'Season', 'Team', 'Result', 'Record'])
        # score_board3 = pd.DataFrame([away_score3, home_score3], columns=['Score', 'Hit', 'Error', 'Base_on_balls'])
        # score_board = pd.concat([score_board1, score_board3], axis=1)  # 두 테이블에서 가져온 정보 합치기
        # score_board
        self.awayboard = away_score1 + away_score2 + away_score3
        self.homeboard = home_score1 + home_score2 + home_score3
        self.scoreboard[0] = self.indexboard
        self.scoreboard[1] = self.awayboard
        self.scoreboard[2] = self.homeboard

        # self.onlyAwayscore = away_score2
        # self.onlyHomescore = away_score2
        # 화면을 갱신시킨다.
        self.updateScoreBoard()

    def resetScoreBoard(self):
        for row in range(len(self.scoreboard)):
            for col in range(len(self.scoreboard[row])):
                self.LScoreboard[row][col].configure(text='')

    def updateScoreBoard(self):
        for row in range(len(self.scoreboard)):
            for col in range(len(self.scoreboard[row])):
                self.LScoreboard[row][col].configure(text=str(self.scoreboard[row][col]))

        self.canvas.delete('graph')
        homescore = 0
        awayscore = 0

        if self.scoreboard[1]:
            MaxScore = self.scoreboard[1][15] if float(self.scoreboard[1][15]) > float(self.scoreboard[2][15]) else \
                self.scoreboard[2][15]
            MaxScore = float(MaxScore)

            widthPerInning = 50.0
            heightPerScore = 250.0 / MaxScore

            awaycolor = 'red' if self.scoreboard[1][2] == '승' else 'blue'
            homecolor = 'red' if self.scoreboard[2][2] == '승' else 'blue'

            for i in range(12):
                valueIndex = i + 3
                if self.homeboard[valueIndex] != '-':
                    nextHomescore = homescore + int(self.homeboard[valueIndex])
                else:
                    nextHomescore = homescore

                if self.awayboard[valueIndex] != '-':
                    nextAwayscore = awayscore + int(self.awayboard[valueIndex])
                else:
                    nextAwayscore = awayscore
                
                # 점수를 잇는 그래프 생성
                self.canvas.create_line(i * widthPerInning, 300 - awayscore * heightPerScore,
                                        (i + 1) * widthPerInning,
                                        300 - nextAwayscore * heightPerScore, tags='graph', fill=awaycolor)
                self.canvas.create_line(i * widthPerInning, 300 - homescore * heightPerScore,
                                        (i + 1) * widthPerInning,
                                        300 - nextHomescore * heightPerScore, tags='graph', fill=homecolor)
                
                # 해당 이닝에 점찍기
                self.canvas.create_oval((i + 1) * widthPerInning - 5,
                                        300 - nextAwayscore * heightPerScore - 5,
                                        (i + 1) * widthPerInning + 5,
                                        300 - nextAwayscore * heightPerScore + 5,
                                        tags='graph', fill=awaycolor
                                        )
                self.canvas.create_oval((i + 1) * widthPerInning - 5,
                                        300 - nextHomescore * heightPerScore - 5,
                                        (i + 1) * widthPerInning + 5,
                                        300 - nextHomescore * heightPerScore + 5,
                                        tags='graph', fill=homecolor
                                        )
                
                awayscore = nextAwayscore
                homescore = nextHomescore

    def readBoxScore(self, selectgame):
        boxscoreURL = 'https://www.koreabaseball.com/ws/Schedule.asmx/GetBoxScoreScroll'
        boxscoreData = {
            'leId': 1,
            'srId': 0,
            'seasonId': selectgame['SEASON_ID'],
            'gameId': selectgame['G_ID']
        }
        self.boxscore = []

        res = requests.post(boxscoreURL, data=boxscoreData)
        res.encoding = 'utf-8'

        if 200 != res.status_code:
            print('읽어 오기 실패! -', res.status_code)
            return

        # print(res.status_code)
        # pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
        # print(pretty_json)

        # table1 = res.json()['tableEtc'].replace('\r\n', '')
        # dict1 = json.loads(table1)

        # pretty_json = json.dumps(dict1, indent=4, ensure_ascii=False)
        # print(pretty_json)
