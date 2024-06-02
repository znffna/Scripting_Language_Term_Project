import pandas as pd
import urllib.request
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom

# NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
client_key = '18d7p2vs9l'
client_secret = "410wLTrekFwG5ynCIyMqLiogOH4TmWzQ2sgVu3Wy"

addresses = [
    '서울특별시 송파구 올림픽로 25',        # 잠실야구장
    '서울특별시 구로구 경인로 430',         # 고척시카이돔
    '인천광역시 미추홀구 매소홀로 618',       #인천 ssg 랜더스필드
    '문학동 482',       #인천 ssg 랜더스필드
    '경기도 수원시 장안구 경수대로 893',       #수원KT위즈파크
    '충청북도 청주시 서원구 사직동 888-1',       #청주야구장
    '대전광역시 중구 대종로 373',       #한화생명이글스파크
    '대구광역시 수성구 야구전설로 1',       #대구삼성라이온즈파크
    '경상북도 포항시 남구 희망대로 790',       #포항야구장
    '울산광역시 남구 문수로 44',       #울산문수야구장
    '부산광역시 동래구 사직로 45',       #사직야구장
    '경상남도 창원시 마산회원구 삼호로 63',       #창원NC파크
    '광주광역시 북구 서림로 10',       #광주기아챔피언스필드
]

# 결과를 저장할 리스트
results = []

for address in addresses:
    # 한글등 non-ASCII text를 URL에 넣을 수 있도록 "%" followed by hexadecimal digits 로 변경
    encAdd = urllib.parse.quote_plus(address)

    # 지오코딩 API 요청 URL 생성
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=%s' % (encAdd)

    # API 요청 생성
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_key)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    # urllib.request.urlopen 메서드로 크롤링할 웹페이지를 가져옴
    response = urllib.request.urlopen(request)

    # getcode() 메서드로 HTTP 응답 상태 코드를 가져올 수 있음
    rescode = response.getcode()

    # HTTP 요청 응답이 정상적일 경우, 해당 HTML 데이터를 수신되었기 때문에 필요한 데이터 추출이 가능함
    if rescode == 200:
        # response.read() 메서드로 수신된 HTML 데이터를 가져올 수 있음
        response_body = response.read()
        # JSON 포맷 데이터를 파싱해서 사전데이터로 만들어주는 json 라이브러리를 사용
        data = json.loads(response_body)

        # 첫 번째 주소 결과를 저장
        if data['addresses']:
            result = {
                'address': address,
                'x': data['addresses'][0]['x'],
                'y': data['addresses'][0]['y']
            }
            results.append(result)
            print(f"{address}: {result['x']}, {result['y']}")
        else:
            print(f"No results for {address}")
    else:
        print(f"Error: {rescode}")

# 결과를 XML로 변환
root = ET.Element("root")
for result in results:
    address_elem = ET.SubElement(root, "address")
    for key, value in result.items():
        child = ET.SubElement(address_elem, key)
        child.text = str(value)

# XML 문자열로 변환
xml_str = ET.tostring(root, encoding='utf-8')

# XML을 보기 좋게 포맷팅
dom = xml.dom.minidom.parseString(xml_str)
pretty_xml_as_string = dom.toprettyxml()

# 포맷팅된 XML 출력
print(pretty_xml_as_string)
