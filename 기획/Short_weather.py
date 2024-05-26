from tkinter import *
from tkinter import font
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom

#단기 예보 서비스
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params ={
    'serviceKey': '2pyqpMvhBE5SfkdQuutIa%2FP6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA%2BkgAg3ObxROFwxxyWhmMxQ%3D%3D',
    'pageNo': '1',
    'numOfRows': '10',
    'dataType': 'XML',
    'base_date': '20240526', #발표 일자
    'base_time': '0500',    # 발표 시각 (06시 발표(정시단위)-매시각 40분 이후 호출 )
    'nx': '55',
    'ny': '127'
}
# 단기예보
# - Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
# - API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
# - 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
# - 강수형태(PTY) 코드 : (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
#                       (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)


response = requests.get(url, params=params)
data = response.content

xml_str = xml.dom.minidom.parseString(data)
pretty_xml = xml_str.toprettyxml()

print(pretty_xml)

# XML 데이터 파싱
root = ET.fromstring(data)
items = root.find('body').find('items').findall('item')

weather_data = {}
for item in items:
    category = item.find('category').text
    fcstValue = item.find('fcstValue').text
    weather_data[category] = fcstValue

# Category 별 이름 맵핑
category_names = {
    'POP': '강수확률 %',
    'PTY': '강수형태 : ', # 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)
    'REH': '습도 %',
    'SKY': '하늘상태 : ', #맑음(1), 구름많음(3), 흐림(4)
    'WSD': '풍속 (m/s)',
    'UUU': '풍속 (동서성분, m/s)',
    'VVV': '풍속 (남북성분, m/s)',
    'VEC': '풍향 (deg)',
}

def convert_code(category, value):
    if category == 'SKY':
        return {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(value, value)
    elif category == 'PTY':
        return {'0': '없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기', '5': '빗방울', '6': '빗방울눈날림', '7': '눈날림'}.get(value, value)
    return value

# GUI 생성
def create_gui():
    root = Tk()
    root.geometry("400x600+750+200")
    root.title("Weather Data")

    font_style = font.Font(size=12)

    frame = Frame(root)
    frame.pack(pady=20)

    title_label = Label(frame, text="Weather Data", font=font.Font(size=14, weight='bold'))
    title_label.pack(pady=10)

    for key in category_names:
        category_name = category_names[key]
        value = weather_data.get(key, "데이터 없음")
        value = convert_code(key, value)
        label = Label(frame, text=f"{category_name}: {value}", font=font_style)
        label.pack(anchor='w')

    root.mainloop()

if __name__ == "__main__":
    create_gui()


