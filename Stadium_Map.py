import requests
import urllib.request
from PIL import Image, ImageTk
from googlemaps import Client
from io import BytesIO
import tkinter as tk
from tkinter import ttk

from GoogleAPI_Key import Google_API_Key

zoom = 18

# 경기장 데이터
stadiums = [
    {'name': '잠실야구장', 'address': '잠실야구장 프로야구장', 'lat': None, 'lng': None},
    {'name': '고척스카이돔', 'address': '고척스카이돔 프로야구장', 'lat': None, 'lng': None},
    {'name': '인천SSG랜더스필드', 'address': '인천SSG 랜더스필드 프로야구장', 'lat': None, 'lng': None},
    {'name': '수원KT위즈파크', 'address': '수원KT위즈파크 프로야구장', 'lat': None, 'lng': None},
    {'name': '청주야구장', 'address': '청주야구장 프로야구장', 'lat': None, 'lng': None},
    {'name': '한화생명이글스파크', 'address': '한화생명이글스파크 프로야구장', 'lat': None, 'lng': None},
    {'name': '대구삼성라이온즈파크', 'address': '대구삼성라이온즈파크 프로야구장', 'lat': None, 'lng': None},
    {'name': '포항야구장', 'address': '포항야구장 프로야구장', 'lat': None, 'lng': None},
    {'name': '울산문수야구장', 'address': '울산문수야구장 프로야구장', 'lat': None, 'lng': None},
    {'name': '사직야구장', 'address': '사직야구장 프로야구장', 'lat': None, 'lng': None},
    {'name': '창원NC파크', 'address': '창원NC파크 프로야구장', 'lat': None, 'lng': None},
    {'name': '광주기아챔피언스필드', 'address': '광주기아챔피언스필드 프로야구장', 'lat': None, 'lng': None}
]

# Google Maps API 클라이언트 생성
gmaps = Client(key=Google_API_Key)

# 경기장 좌표 가져오기
for stadium in stadiums:
    geocode_result = gmaps.geocode(stadium['address'])
    if geocode_result:
        stadium['lat'] = geocode_result[0]['geometry']['location']['lat']
        stadium['lng'] = geocode_result[0]['geometry']['location']['lng']

def createStadiumFrame(frame):
    global zoom

    def update_map(stadium_name):
        global zoom
        selected_stadium_info = next(stadium for stadium in stadiums if stadium['name'] == stadium_name)
        lat, lng = selected_stadium_info['lat'], selected_stadium_info['lng']
        stadium_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size=600x400&maptype=roadmap"  # size를 600x400으로 변경

        marker_url = f"&markers=color:red%7C{lat},{lng}"
        stadium_map_url += marker_url

        response = requests.get(stadium_map_url + '&key=' + Google_API_Key)
        image = Image.open(BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        map_label.configure(image=photo)
        map_label.image = photo

    def on_stadium_double_click(event):
        selected_index = stadium_list.curselection()
        if selected_index:
            selected_stadium_name = stadium_list.get(selected_index)
            update_map(selected_stadium_name)

    def zoom_in():
        global zoom
        zoom += 1
        selected_index = stadium_list.curselection()
        if selected_index:
            selected_stadium_name = stadium_list.get(selected_index)
            update_map(selected_stadium_name)

    def zoom_out():
        global zoom
        if zoom > 1:
            zoom -= 1
        selected_index = stadium_list.curselection()
        if selected_index:
            selected_stadium_name = stadium_list.get(selected_index)
            update_map(selected_stadium_name)

    left_frame = tk.Frame(frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    list_frame = tk.Frame(left_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    stadium_list = tk.Listbox(list_frame, width=60, yscrollcommand=scrollbar.set)
    stadium_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=stadium_list.yview)

    # 초기 목록에 모든 경기장 추가
    for stadium in stadiums:
        stadium_list.insert(tk.END, stadium['name'])

    right_frame = tk.Frame(frame)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    map_frame = tk.Frame(right_frame)
    map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    map_label = tk.Label(map_frame, width=700, height=600)  # 라벨 크기 설정
    map_label.pack()

    button_frame = tk.Frame(map_frame)
    button_frame.pack(side=tk.TOP, pady=1)  # 지도 아래에 버튼 프레임 배치

    zoom_in_button = tk.Button(button_frame, text="확대(+)", command=zoom_in)
    zoom_in_button.pack(side=tk.LEFT, padx=50)

    zoom_out_button = tk.Button(button_frame, text="축소(-)", command=zoom_out)
    zoom_out_button.pack(side=tk.RIGHT, padx=50)

    stadium_list.bind("<Double-1>", on_stadium_double_click)

    # 초기 지도 설정
    update_map(stadiums[0]['name'])

# # tkinter GUI 생성
# root = tk.Tk()
# root.title("경기장 위치 정보")
#
# # 경기장 선택 콤보박스 생성
# selected_stadium = tk.StringVar()
# selected_stadium.set(stadiums[0]['name'])  # 초기값 설정
# stadium_options = [stadium['name'] for stadium in stadiums]
# stadium_combo = ttk.Combobox(root, textvariable=selected_stadium, values=stadium_options)
# stadium_combo.pack()
#
# # 경기장 목록 표시 함수
# def show_stadiums():
#     stadium_list.delete(0, tk.END)
#
#     stadium_name = selected_stadium.get()
#     stadiums_in_selected = [stadium for stadium in stadiums if stadium['name'] == stadium_name]
#
#     # 경기장 목록에 추가
#     for stadium in stadiums_in_selected:
#         stadium_list.insert(tk.END, stadium['name'])
#
# # 지도 이미지 업데이트 함수
# def update_map():
#     global zoom
#     stadium_name = selected_stadium.get()
#     selected_stadium_info = next(stadium for stadium in stadiums if stadium['name'] == stadium_name)
#     lat, lng = selected_stadium_info['lat'], selected_stadium_info['lng']
#     stadium_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size=400x400&maptype=roadmap"
#
#     # 선택한 경기장의 위치 마커 추가
#     marker_url = f"&markers=color:red%7C{lat},{lng}"
#     stadium_map_url += marker_url
#
#     # 지도 이미지 업데이트
#     response = requests.get(stadium_map_url + '&key=' + Google_API_Key)
#     image = Image.open(io.BytesIO(response.content))
#     photo = ImageTk.PhotoImage(image)
#     map_label.configure(image=photo)
#     map_label.image = photo
#
#     # 경기장 목록 업데이트
#     show_stadiums()
#
# def on_stadium_select(event):
#     update_map()
#
# def zoom_in():
#     global zoom
#     zoom += 1
#     update_map()
#
# def zoom_out():
#     global zoom
#     if zoom > 1:
#         zoom -= 1
#     update_map()
#
# # 경기장 목록 리스트박스 생성
# stadium_list = tk.Listbox(root, width=60)
# stadium_list.pack(side=tk.LEFT, fill=tk.BOTH)
#
# # 스크롤바 생성
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
# # 스크롤바와 경기장 목록 연결
# stadium_list.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=stadium_list.yview)
#
# # 첫 번째 경기장의 위치를 중심으로 지도 이미지 다운로드
# initial_stadium = stadiums[0]
# initial_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={initial_stadium['lat']},{initial_stadium['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"
# initial_marker_url = f"&markers=color:red%7C{initial_stadium['lat']},{initial_stadium['lng']}"
# initial_map_url += initial_marker_url
#
# response = requests.get(initial_map_url + '&key=' + Google_API_Key)
# image = Image.open(io.BytesIO(response.content))
# photo = ImageTk.PhotoImage(image)
#
# # 지도 이미지 라벨 생성
# map_label = tk.Label(root, image=photo)
# map_label.pack()
#
# # 확대/축소 버튼 생성
# zoom_in_button = tk.Button(root, text="확대(+)", command=zoom_in)
# zoom_in_button.pack(side=tk.LEFT)
#
# zoom_out_button = tk.Button(root, text="축소(-)", command=zoom_out)
# zoom_out_button.pack(side=tk.LEFT)
#
# stadium_combo.bind("<<ComboboxSelected>>", on_stadium_select)
#
# update_map()
#
# root.mainloop()
