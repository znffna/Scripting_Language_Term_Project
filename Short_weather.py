from tkinter import *
from tkinter import font
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
from PIL import Image, ImageTk
from io import BytesIO
import urllib.request
from datetime import datetime


# 단기예보
# - Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
# - API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
# - 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
# - 강수형태(PTY) 코드 : (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
#                       (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)


def fetch_weather(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    # 현재 날짜를 'YYYYMMDD' 형식으로 가져오기
    current_date = datetime.now().strftime('%Y%m%d')

    params = {
        'serviceKey': '2pyqpMvhBE5SfkdQuutIa/P6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA+kgAg3ObxROFwxxyWhmMxQ==',
        # decoding
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'XML',
        'base_date': current_date,  # 발표 일자
        'base_time': '0500',  # 발표 시각 (06시 발표(정시단위)-매시각 40분 이후 호출)
        'nx': str(nx),
        'ny': str(ny)
    }

    response = requests.get(url, params=params)
    data = response.content

    xml_str = xml.dom.minidom.parseString(data)
    pretty_xml = xml_str.toprettyxml()

    # print(pretty_xml)

    # XML 데이터 파싱
    root = ET.fromstring(data)
    items = root.find('body').find('items').findall('item')

    weather_data = {}
    for item in items:
        category = item.find('category').text
        fcstValue = item.find('fcstValue').text
        weather_data[category] = fcstValue

    return weather_data


def convert_code(category, value):
    if category == 'SKY':
        return {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(value, value)
    elif category == 'PTY':
        return {'0': '없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기', '5': '빗방울', '6': '빗방울눈날림', '7': '눈날림'}.get(value,
                                                                                                                  value)
    return value


def filter_weather_data(weather_data):
    filtered_data = {}
    categories = ['POP', 'PTY', 'REH', 'SKY']
    for category in categories:
        if category in weather_data:
            filtered_data[category] = convert_code(category, weather_data[category])
    return filtered_data

def display_weather(frame, weather_data):
    for widget in frame.winfo_children():
        widget.destroy()

    font_style = font.Font(size=12)
    title_label = Label(frame, text="날씨 데이터", font=font.Font(size=14, weight='bold'))
    title_label.pack(pady=10)

    category_names = {
        'POP': '강수확률 %',
        'PTY': '강수형태 : ',  # 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)
        'REH': '습도 %',
        'SKY': '하늘상태 : ',  # 맑음(1), 구름많음(3), 흐림(4)
        'WSD': '풍속 (m/s)',
        'UUU': '풍속 (동서성분, m/s)',
        'VVV': '풍속 (남북성분, m/s)',
        'VEC': '풍향 (deg)',
        'TMP': '1 시간 기온 (℃)',
        'PCP': '1 시간 강수량 (범주 (1 mm))'
    }

    for key in category_names:
        category_name = category_names[key]
        value = weather_data.get(key, "데이터 없음")
        value = convert_code(key, value)
        label = Label(frame, text=f"{category_name}: {value}", font=font_style)
        label.pack(anchor='w')


def create_weather_frame(frame):
    # 좌측에 지도 이미지를 표시할 프레임
    left_frame = Frame(frame, width=400, height=600)
    left_frame.pack(side=LEFT, padx=20, pady=20)

    img_url = "https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/KBOHome/resources/images/schedule/bg_map.png"
    with urllib.request.urlopen(img_url) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    img_label = Label(left_frame, image=image, height=400, width=400)
    img_label.image = image  # 이미지가 가비지 컬렉션되지 않도록 참조 유지
    img_label.pack()

    # 우측에 경기장 리스트와 검색 버튼을 표시할 프레임
    right_frame = Frame(frame, width=400, height=600)
    right_frame.pack(side=LEFT, pady=10)

    stadiums = [
        {"name": "잠실야구장", "nx": 62, "ny": 126},
        {"name": "고척스카이돔", "nx": 58, "ny": 125},
        {"name": "인천SSG랜더스필드", "nx": 54, "ny": 124},
        {"name": "수원KT위즈파크", "nx": 61, "ny": 121},
        {"name": "청주야구장", "nx": 69, "ny": 107},
        {"name": "한화생명이글스파크", "nx": 68, "ny": 100},
        {"name": "대구삼성라이온즈파크", "nx": 89, "ny": 90},
        {"name": "포항야구장", "nx": 102, "ny": 95},
        {"name": "울산문수야구장", "nx": 101, "ny": 84},
        {"name": "사직야구장", "nx": 98, "ny": 76},
        {"name": "창원NC파크", "nx": 89, "ny": 77},
        {"name": "광주기아챔피언스필드", "nx": 59, "ny": 74}
    ]

    stadium_listbox = Listbox(right_frame, selectmode=SINGLE, height=20)
    for stadium in stadiums:
        stadium_listbox.insert(END, stadium["name"])
    stadium_listbox.pack(side=LEFT, pady=10)

    def show_weather():
        selected_index = stadium_listbox.curselection()
        if selected_index:
            selected_stadium = stadiums[selected_index[0]]
            nx = selected_stadium["nx"]
            ny = selected_stadium["ny"]
            weather_data = fetch_weather(nx, ny)
            display_weather(weather_info_frame, weather_data)

    search_button = Button(right_frame, text="검색", command=show_weather)
    search_button.pack(side=LEFT, pady=10)
    weather_info_frame = Frame(right_frame, width=400, height=400)
    weather_info_frame.pack(side=LEFT, pady=10)
