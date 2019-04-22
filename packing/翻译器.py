import os                                   # 创建文件夹，删除文件
import time                                 # 引入时间模块，用作延迟
import base64                               # 将二进制转换为图片显示(软件logo)
import minimu                               # 播放音频
import requests                             # 爬取有道翻译，获取翻译结果
from tkinter import *                       # 制作GUI界面
from aip import AipSpeech                   # 调用百度API，语音合成
from mutagen.mp3 import MP3                 # 获取mp3时长
from icon import img1, img2                 # 导入图片转换后的二进制(软件logo)
from PIL import Image, ImageTk              # 可以让TK使用png格式的图片(TK默认只支持GIF格式)
from tkinter import messagebox              # TK弹窗
from json.decoder import JSONDecodeError    # 捕获json.decoder错误


# 获取翻译后的结果
def fanYi(event):
    global result, var, path
    try:
        entry2.delete(0, 'end')
        var = entry1.get()
        data = {
            'i': var,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': '15466010467912',
            'sign': '98565fc8e4ea2ab0bb49b082b474ed27',
            'ts': '1546601046791',
            'bv': '0ef078d6b7f3e6f8047a6cbd85c069cc',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false',
        }
        res = requests.post(
            'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule', data)
        result = res.json()['translateResult'][0][0]['tgt']
        name = os.environ['USERNAME']
        path = r"C:/Users/" + name + "/AppData/Local/Temp/"
    except JSONDecodeError:
        messagebox.showwarning(title="warning", message="翻译内容为空，请输入后重试")
    else:
        entry2.insert('end', result)


# 生成翻译前的音频
def say1():
    try:
        # 调用百度语音识别API
        """ 你的 APPID AK SK """
        APP_ID = '15704344'
        API_KEY = 'roM0RL4WS8ZzzF2Eu40HdUFD'
        SECRET_KEY = '1hRU2MPFGHRDGbRcRzIGveevORvY2Kbs'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        effect_data = client.synthesis(var, 'zh', 1, {
            'vol': 5,
            'spd': 4,
            'pit': 8,
            'per': 4
        })
        # 写入文件
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "data.mp3", 'wb+') as ff:
            ff.write(effect_data)
        # 获取mp3时长
        audio = MP3(path + "data.mp3")
        mp3_lenth = audio.info.length
        # 播放语音1
        song = minimu.load(path + "data.mp3")
        song.play()
        time.sleep(mp3_lenth)
        song.stop()
    except NameError:
        messagebox.showwarning(title="warning", message="请输入内容并点击翻译后重试")
    except TypeError:
        messagebox.showwarning(title="warning", message="请输入内容并点击翻译后重试")


# 生成翻译后的音频
def say2():
    try:
        # 调用百度语音识别API
        """ 你的 APPID AK SK """
        APP_ID = '15704344'
        API_KEY = 'roM0RL4WS8ZzzF2Eu40HdUFD'
        SECRET_KEY = '1hRU2MPFGHRDGbRcRzIGveevORvY2Kbs'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        effect_data = client.synthesis(result, 'zh', 1, {
            'vol': 5,
            'spd': 4,
            'pit': 8,
            'per': 4
        })
        # 写入文件
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path+"data.mp3", 'wb+') as ff:
            ff.write(effect_data)
        # 获取mp3时长
        audio = MP3(path+"data.mp3")
        mp3_lenth = audio.info.length
        # 播放语音2
        song = minimu.load(path+"data.mp3")
        song.play()
        time.sleep(mp3_lenth)
        song.stop()
    except NameError:
        messagebox.showwarning(title="warning", message="请输入内容并点击翻译后重试")


# 清空输入框
def clean():
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')


# 写入图片数据
with open("img1.ico", 'wb+') as f:
    f.write(base64.b64decode(img1))
with open(r'img2.png', 'wb+') as f:
    f.write(base64.b64decode(img2))

# 基本设置
root = Tk()
root.title('Translation')
root.iconbitmap("img1.ico")
os.remove("img1.ico")
root.geometry('485x150+560+250')      # 位置坐标随意

# 导入png图片
img_open = Image.open(r'img2.png')
img_png = ImageTk.PhotoImage(img_open)

# 设置标签
label1 = Label(root, text='输入内容：', font=('GB2312', 18))
label1.grid(row=0, column=0, padx=5)
label2 = Label(root, text='结    果：', font=('GB2312', 18))
label2.grid(row=1, column=0, padx=5)

# 设置文本
entry1 = Entry(root, fg='red', width=25, font=('GB2312', 18))
entry1.grid(row=0, column=1, pady=10)
entry2 = Entry(root, fg='red', width=25, font=('GB2312', 18))
entry2.grid(row=1, column=1, pady=10)

# 设置按钮
root.bind('<Return>', fanYi)        # 绑定回车键
button1 = Button(root, text='翻译', font=('GB2312', 18))
button1.bind('<Button-1>', fanYi)   # 绑定按钮
button1.grid(row=2, column=1, ipadx=20, sticky=E, columnspan=1)
button2 = Button(root, text='清空', font=('GB2312', 18), command=clean)
button2.grid(row=2, column=1, ipadx=20, sticky=W, rowspan=1, columnspan=1)
button4 = Button(root, text='发音1', image=img_png, command=say1)
button4.grid(row=0, column=2, padx=5)
button5 = Button(root, text='发音2', image=img_png, command=say2)
button5.grid(row=1, column=2, padx=5)
os.remove("img2.png")

root.mainloop()       # 让图形化软件出现
