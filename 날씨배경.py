from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk

window = Tk()
window.geometry('500x500+500+200')

url="https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/KBOHome/resources/images/schedule/bg_map.png"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)
Label(window,image=image, height=400,width=1000).pack()

window.mainloop()