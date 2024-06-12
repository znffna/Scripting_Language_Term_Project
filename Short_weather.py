from tkinter import *
from tkinter import font

import PIL.Image
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
from PIL import Image, ImageTk
from io import BytesIO
import urllib.request
from datetime import datetime
from collections import defaultdict
import Air_quality

def fetch_weather(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    current_date = datetime.now().strftime('%Y%m%d')

    params = {
        'serviceKey': '2pyqpMvhBE5SfkdQuutIa/P6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA+kgAg3ObxROFwxxyWhmMxQ==',
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'XML',
        'base_date': current_date,
        'base_time': '0500',
        'nx': str(nx),
        'ny': str(ny)
    }

    response = requests.get(url, params=params)
    data = response.content

    xml_str = xml.dom.minidom.parseString(data)
    pretty_xml = xml_str.toprettyxml()

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
        return {'0': '없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기', '5': '빗방울', '6': '빗방울눈날림', '7': '눈날림'}.get(value, value)
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
        'PTY': '강수형태 : ',
        'REH': '습도 %',
        'SKY': '하늘상태 : ',
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

def load_air_quality_data():
    air_quality_data = {}
    with open('air_quality_data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace(": ", ",")
            line = line.replace("\n", "")
            region = line.split(",")[1]
            Station = line.split(",")[3]
            PM10 = line.split(",")[5]
            if region not in air_quality_data:
                air_quality_data[region] = []
            air_quality_data[region].append((Station, PM10))

    print(air_quality_data)
    return air_quality_data

def create_weather_frame(parent_frame):
    main_frame = Frame(parent_frame)
    main_frame.pack(expand=True, fill=BOTH)

    top_frame = Frame(main_frame)
    top_frame.pack(side=TOP, expand=True, fill=BOTH)

    bottom_frame = Frame(main_frame)
    bottom_frame.pack(side=BOTTOM, fill=X)

    left_frame = Frame(top_frame, width=500, height=600, bd=2, relief="solid")
    left_frame.pack(side=LEFT, padx=10, pady=10, expand=True, fill=BOTH)

    img_url = "https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/KBOHome/resources/images/schedule/bg_map.png"
    with urllib.request.urlopen(img_url) as u:
        raw_data = u.read()
    im = PIL.Image.open(BytesIO(raw_data))
    ResizeImage = im.resize((300, 300))

    image = ImageTk.PhotoImage(ResizeImage)
    img_label = Label(left_frame, image=image, height=300, width=300)
    img_label.image = image
    img_label.pack(expand=True, fill=BOTH)

    middle_frame = Frame(top_frame, width=200, height=600, bd=2, relief="solid")
    middle_frame.pack(side=LEFT, padx=10, pady=10, expand=True, fill=BOTH)

    stadiums = [
        {"name": "잠실야구장", "nx": 62, "ny": 126, "region": "서울"},
        {"name": "고척스카이돔", "nx": 58, "ny": 125, "region": "서울"},
        {"name": "인천SSG랜더스필드", "nx": 54, "ny": 124, "region": "인천"},
        {"name": "수원KT위즈파크", "nx": 61, "ny": 121, "region": "x"},
        {"name": "청주야구장", "nx": 69, "ny": 107, "region": "충북"},
        {"name": "한화생명이글스파크", "nx": 68, "ny": 100, "region": "대전"},
        {"name": "대구삼성라이온즈파크", "nx": 89, "ny": 90, "region": "대구"},
        {"name": "포항야구장", "nx": 102, "ny": 95, "region": "경북"},
        {"name": "울산문수야구장", "nx": 101, "ny": 84, "region": "울산"},
        {"name": "사직야구장", "nx": 98, "ny": 76, "region": "부산"},
        {"name": "창원NC파크", "nx": 89, "ny": 77, "region": "경남"},
        {"name": "광주기아챔피언스필드", "nx": 59, "ny": 74, "region": "광주"}
    ]

    stadium_listbox = Listbox(middle_frame, selectmode=SINGLE, height=20)
    for stadium in stadiums:
        stadium_listbox.insert(END, stadium["name"])
    stadium_listbox.pack(side=LEFT, pady=10, expand=True, fill=BOTH)

    right_frame = Frame(top_frame, width=400, height=600, bd=2, relief="solid")
    right_frame.pack(side=LEFT, padx=10, pady=10, expand=True, fill=BOTH)

    air_quality_data = load_air_quality_data()

    def show_weather():
        selected_index = stadium_listbox.curselection()
        if selected_index:
            selected_stadium = stadiums[selected_index[0]]
            nx = selected_stadium["nx"]
            ny = selected_stadium["ny"]
            weather_data = fetch_weather(nx, ny)
            display_weather(weather_info_frame, weather_data)

    def show_air_quality():
        selected_index = stadium_listbox.curselection()
        if selected_index:
            selected_stadium = stadiums[selected_index[0]]
            region_name = selected_stadium["region"]
            relevant_info = air_quality_data.get(region_name, [])
            text_box.delete("1.0", END)
            outputstr = 'Air Quality Info for ' + region_name + "\n"
            for data in relevant_info:
                outputstr += data[0]+ ' 미세먼지 농도 = ' + data[1] + "\n"
            text_box.insert(END, outputstr)

    button_frame = Frame(bottom_frame, height=100)
    button_frame.pack(side=TOP, pady=10, fill=X)

    search_button = Button(button_frame, text="날씨 검색", command=show_weather)
    search_button.pack(side=LEFT, padx=10)

    air_quality_button = Button(button_frame, text="대기질 검색", command=show_air_quality)
    air_quality_button.pack(side=LEFT, padx=10)

    info_frame = Frame(middle_frame, height=500, bd=2, relief="solid")
    info_frame.pack(side=TOP, pady=10, expand=True, fill=BOTH)

    weather_info_frame = Frame(info_frame, width=400, height=200)
    weather_info_frame.pack(side=TOP, pady=10, expand=True, fill=BOTH)

    text_box = Text(info_frame, wrap=WORD)
    text_box.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10, pady=10)