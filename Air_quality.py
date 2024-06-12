import requests
import xml.etree.ElementTree as ET
import spam  # C 확장 모듈 임포트

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
    base_url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    service_key = '2pyqpMvhBE5SfkdQuutIa/P6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA+kgAg3ObxROFwxxyWhmMxQ=='

    # First request to get totalCount
    params = {
        'serviceKey': service_key,
        'sidoName': district_name,
        'returnType': 'XML',
        'numOfRows': '1',
        'pageNo': '1'
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None

    data = response.content

    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        return None

    total_count = int(root.find('body').find('totalCount').text)
    print(f"Total count for {district_name}: {total_count}")

    air_quality_data = []
    params['numOfRows'] = '100'  # 한 페이지당 최대 항목 수로 설정

    for page in range(1, (total_count // 100) + 2):  # 페이지 순회
        params['pageNo'] = str(page)
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            continue

        data = response.content
        try:
            root = ET.fromstring(data)
        except ET.ParseError as e:
            continue

        items = root.find('body').find('items').findall('item')
        for item in items:
            stationName = item.find('stationName')
            pm10Value = item.find('pm10Value')
            if stationName is not None and pm10Value is not None:
                data_str = f"Station: {stationName.text}, PM10: {pm10Value.text}"
                air_quality_data.append(data_str)

    air_quality_str = "\n".join(air_quality_data)
    return air_quality_str

def fetch_and_save_air_quality():
    all_air_quality_data = []
    for region in stadiums_data.keys():
        for stadium in stadiums_data[region]:
            district_name = stadium["district"]
            air_quality_str = fetch_air_quality_by_district(district_name)
            if air_quality_str:
                all_air_quality_data.append(f"{stadium['name']} ({district_name}):\n{air_quality_str}")

    complete_air_quality_str = "\n\n".join(all_air_quality_data)

    if not complete_air_quality_str.strip():
        return

    result = spam.save_air_quality(complete_air_quality_str)
    if result:
        print("Data successfully saved to file.")
    else:
        print("Failed to save data to file.")
