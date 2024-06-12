from tkinter import *
import requests
import xml.etree.ElementTree as ET
import spam  # C 확장 모듈 임포트

# 야구장 정보
stadiums_data = {
    "서울": [
        {"name": "잠실야구장", "district": "송파구"},
        {"name": "고척스카이돔", "district": "구로구"}
    ],
    "인천": [
        {"name": "인천SSG랜더스필드", "district": "미추홀구"}
    ],
    "수원": [
        {"name": "수원KT위즈파크", "district": "수원시 장안구"}
    ],
    "충북": [
        {"name": "청주야구장", "district": "청주시 서원구"}
    ],
    "대전": [
        {"name": "한화생명이글스파크", "district": "중구"}
    ],
    "대구": [
        {"name": "대구삼성라이온즈파크", "district": "수성구"}
    ],
    "경북": [
        {"name": "포항야구장", "district": "포항시 남구"}
    ],
    "울산": [
        {"name": "울산문수야구장", "district": "남구"}
    ],
    "부산": [
        {"name": "사직야구장", "district": "동래구"}
    ],
    "경남": [
        {"name": "창원NC파크", "district": "창원시 마산회원구"}
    ],
    "광주": [
        {"name": "광주기아챔피언스필드", "district": "북구"}
    ]
}

def fetch_air_quality_by_district(district_name):
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'

    params = {
        'serviceKey': '2pyqpMvhBE5SfkdQuutIa/P6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA+kgAg3ObxROFwxxyWhmMxQ==',
        'sidoName': district_name,
        'returnType': 'XML',
        'numOfRows': '10',
        'pageNo': '1'
    }

    response = requests.get(url, params=params)
    print(f"API Response Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Failed to fetch data from API")
        return None

    data = response.content
    print(f"API Response Content:\n{data.decode('utf-8')}")

    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
        return None

    items = root.find('body').find('items').findall('item')
    print(f"Number of items found: {len(items)}")

    air_quality_data = []
    for item in items:
        stationName = item.find('stationName')
        pm10Value = item.find('pm10Value')
        if stationName is not None and pm10Value is not None:
            data_str = f"District: {district_name}, Station: {stationName.text}, PM10: {pm10Value.text}"
            print(data_str)  # 디버깅 메시지
            air_quality_data.append(data_str)
        else:
            print(f"Skipping item due to missing data: {ET.tostring(item, encoding='unicode')}")

    air_quality_str = "\n".join(air_quality_data)
    return air_quality_str

def fetch_and_save_air_quality():
    all_air_quality_data = []
    for region in stadiums_data.keys():
        for stadium in stadiums_data[region]:
            district_name = stadium["district"]
            air_quality_str = fetch_air_quality_by_district(district_name)
            if air_quality_str:
                all_air_quality_data.append(air_quality_str)

    complete_air_quality_str = "\n\n".join(all_air_quality_data)
    print(f"Air quality data to be saved:\n{complete_air_quality_str}")

    if not complete_air_quality_str.strip():
        print("No air quality data to save.")
        return

    result = spam.save_air_quality(complete_air_quality_str)
    if result:
        print("Data successfully saved to file.")
    else:
        print("Failed to save data to file.")

def display_info():
    fetch_and_save_air_quality()
    with open('air_quality_data.txt', 'r', encoding='utf-8') as file:
        air_quality_info = file.read()

    text_box.delete("1.0", END)
    text_box.insert(END, "Air Quality Info:\n" + air_quality_info)

# Tkinter GUI 설정
root = Tk()
root.title("야구장 날씨 및 대기질 정보 프로그램")
root.geometry("600x600")

fetch_button = Button(root, text="정보 가져오기", command=display_info)
fetch_button.pack(pady=10)

text_box = Text(root, wrap=WORD)
text_box.pack(expand=True, fill=BOTH, padx=10, pady=10)

root.mainloop()
