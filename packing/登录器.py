import os
import base64
import pymysql
from tkinter import *
from icon import img1, img2
from PIL import Image, ImageTk
from tkinter import messagebox


try:
    # 连接数据库
    db = pymysql.connect('********', '****', '****', '****')
    # 声明游标
    cur = db.cursor()
except pymysql.Error as e:
    messagebox.showerror(title="连接失败", message="连接数据库失败：" + str(e))


# #########################注册界面#########################
def add_user():
    # 注册
    def prove():
        # 查询数据
        name = []
        query = "SELECT * FROM USER"
        cur.execute(query)
        results = cur.fetchall()
        for i in results:
            name.append(i[0])
        if entry_new_user.get() in name:
            messagebox.showwarning(title='警告信息', message="该用户名已存在")
        elif entry_new_pwd.get() != entry_new_pwd2.get():
            messagebox.showwarning(title='警告信息', message="两次输入密码不一致")
        else:
            # 插入数据
            SQL = 'INSERT INTO USER (Name, Password) VALUE (%s,%s)'
            value = (entry_new_user.get(), entry_new_pwd.get())
            cur.execute(SQL, value)
            db.commit()
            messagebox.showinfo(title='提示信息', message="注册成功！")
            sign_up.destroy()

    # 基本属性
    sign_up = Toplevel(root)
    sign_up.title("注册账号")
    sign_up.geometry('310x165+300+150')
    # 标签
    label1_new_user = Label(sign_up, text="用户名：", fg='red', font=('GB2312', 12))
    label1_new_user.grid(row=0, column=0, padx=5, pady=8)
    label1_new_pwd = Label(sign_up, text="密  码：", fg='red', font=('GB2312', 12))
    label1_new_pwd.grid(row=1, column=0, padx=5, pady=8)
    label1_new_pwd2 = Label(sign_up, text="确认密码：", fg='red', font=('GB2312', 12))
    label1_new_pwd2.grid(row=2, column=0, padx=5, pady=8)
    # 文本
    entry_new_user = Entry(sign_up, width=18, font=('GB2312', 16))
    entry_new_user.grid(row=0, column=1)
    entry_new_pwd = Entry(sign_up, width=18, show="*", font=('GB2312', 16))
    entry_new_pwd.grid(row=1, column=1)
    entry_new_pwd2 = Entry(sign_up, width=18, show="*", font=('GB2312', 16))
    entry_new_pwd2.grid(row=2, column=1)
    # 按钮
    button1_new_user = Button(sign_up, text="注册", command=prove)
    button1_new_user.grid(row=3, column=1, ipadx=20, ipady=5, pady=5, sticky=E)


# 登录
def login_user():
    name = []
    pwd = []
    query = "SELECT * FROM USER"
    cur.execute(query)
    results = cur.fetchall()
    # 遍历所有的用户名和密码，并加入到列表中
    for i in results:
        name.append(i[0])
        pwd.append(i[1])
    # 判断用户是否存在
    if entry1.get() not in name:
        messagebox.showerror(title="警告信息", message='该用户不存在')
        if messagebox.askokcancel(title='警告信息', message="是否注册新用户？"):
            add_user()
    # 判断输入的用户名和密码是否正确
    elif entry1.get() in name and entry2.get() == pwd[name.index(entry1.get())]:
        messagebox.showinfo(title="欢迎登录", message='登录成功：' + entry1.get())
    else:
        messagebox.showwarning(title='提示信息', message='账号或密码输入错误！')


# 写入图片数据
with open("img1.ico", 'wb+') as f:
    f.write(base64.b64decode(img1))
with open(r'img2.png', 'wb+') as f:
    f.write(base64.b64decode(img2))

# #########################登录界面#########################
# 基本属性
root = Tk()
root.title('登录器')
root.iconbitmap('img1.ico')
os.remove("img1.ico")
root.geometry('460x265+560+250')

# 导入图片
img_open = Image.open('img2.png')
img_png = ImageTk.PhotoImage(img_open)

# 标签
image = Label(root, image=img_png, width=460)
image.grid(row=0, column=0, sticky=W)
os.remove("img2.png")
label1 = Label(root, text="用户名：", fg='red', font=('GB2312', 16))
label1.grid(row=1, column=0, sticky=W, padx=10)
label2 = Label(root, text="密  码：", fg='red', font=('GB2312', 16))
label2.grid(row=2, column=0, sticky=W, padx=10)

# 文本
entry1 = Entry(root, width=22, font=('GB2312', 20))
entry1.grid(row=1, column=0, sticky=W, padx=120, pady=10)
entry2 = Entry(root, width=22, font=('GB2312', 20), show="*")
entry2.grid(row=2, column=0, sticky=W, padx=120, pady=10)

# 按钮
button1 = Button(root, text="注册", command=add_user)
button1.grid(row=3, column=0, sticky=W, padx=120, ipadx=50, ipady=10)
button1 = Button(root, text="登录", command=login_user)
button1.grid(row=3, column=0, padx=300, ipadx=50, ipady=10)

# 主事件循环
root.mainloop()
