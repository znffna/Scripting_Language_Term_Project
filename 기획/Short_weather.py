from tkinter import *
from tkinter import font
import requests

#단기 예보 서비스
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : '2pyqpMvhBE5SfkdQuutIa%2FP6S7BUX1TeiJ5YMaimvONN633S9nHj5qccduIJHiIA%2BkgAg3ObxROFwxxyWhmMxQ%3D%3D',
         'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : '20240526', 'base_time' : '0600', 'nx' : '55', 'ny' : '127' }

response = requests.get(url, params=params)
print(response.content)


