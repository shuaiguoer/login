import os
import random
import base64
import pymysql
from tkinter import *
from icon import img1, img2
from PIL import Image, ImageTk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


try:
    # 连接数据库
    db = pymysql.connect('97.64.26.219', 'user', '123.com', 'login')
    # 声明游标
    cur = db.cursor()
except pymysql.Error as e:
    messagebox.showerror(title="网络连接失败", message="网络连接失败\n" + str(e))


# #########################注册界面#########################
def add_user():
    xxxx = random.randint(1000, 9999)

    # 发送邮件
    def mail():
        try:
            my_sender = 'ls12345666@qq.com'     # 发件人邮箱账号
            my_pass = 'dsyzyeeftoyzcddb'        # 发件人邮箱密码(当时申请smtp给的口令)
            my_user = entry_new_mail.get()      # 收件人邮箱账号，我这边发送给自己
            msg = MIMEText(str(xxxx), 'plain', 'utf-8')
            msg['From'] = formataddr(["Shuai", my_sender])      # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = formataddr(["收件人昵称", my_user])
            msg['Subject'] = "欢迎注册!!!"                      # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)       # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)                    # 括号中对应的是发件人邮箱账号、邮箱密码
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            server.quit()  # 关闭连接
        except smtplib.SMTPRecipientsRefused:
            messagebox.showwarning(title="警告信息", message="验证码发送失败!\n请检查您的邮箱是否填写正确！")
        except smtplib.SMTPServerDisconnected:
            messagebox.showwarning(title="警告信息", message="验证码发送失败!\n网络问题，请更换网络后重试")

    # 注册
    def prove_user():
        # 查询数据
        name = []
        emaile = []
        query = "SELECT * FROM user_info"
        cur.execute(query)
        results = cur.fetchall()
        for i in results:
            name.append(i[1])
            emaile.append(i[3])
        if entry_new_user.get() in name:
            messagebox.showwarning(title='警告信息', message="此用户名已存在")
        elif entry_new_user.get() == '':
            messagebox.showwarning(title="警告信息", message="用户名不能为空")
        elif entry_new_pwd.get() == '':
            messagebox.showwarning(title="警告信息", message="密码不能为空，且不能低于6位")
        elif len(entry_new_pwd.get()) < 6:
            messagebox.showwarning(title="警告信息", message="密码不能低于6位数")
        elif entry_new_pwd.get() != entry_new_pwd2.get():
            messagebox.showwarning(title="警告信息", message="两次输入密码不一致")
        elif entry_new_mail.get() == '':
            messagebox.showwarning(title="警告信息", message="绑定的邮箱不能为空")
        elif entry_new_mail.get() in emaile:
            messagebox.showwarning(title="警告信息", message="此邮箱已绑定其他账号")
        elif entry_new_pin.get() == '':
            messagebox.showwarning(title="警告信息", message="请输入验证码")
        elif entry_new_pin.get() != str(xxxx):
            messagebox.showwarning(title="警告信息", message="验证码输入错误")
        else:
            # 插入数据
            insert_SQL = 'INSERT INTO user_info (name, password, email) VALUE (%s,%s,%s)'
            value = (entry_new_user.get(), entry_new_pwd.get(), entry_new_mail.get())
            cur.execute(insert_SQL, value)
            db.commit()
            messagebox.showinfo(title='提示信息', message="注册成功！")
            sign_up.destroy()

    # 基本属性
    sign_up = Toplevel(root)
    sign_up.title("注册账号")
    sign_up.geometry('360x200+300+150')
    # 标签
    label_new_user = Label(sign_up, text="用户名：", font=('GB2312', 12))
    label_new_user.grid(row=0, column=0, padx=5, pady=8)
    label_new_pwd = Label(sign_up, text="密  码：", font=('GB2312', 12))
    label_new_pwd.grid(row=1, column=0, padx=5, pady=8)
    label_new_pwd2 = Label(sign_up, text="确认密码：", font=('GB2312', 12))
    label_new_pwd2.grid(row=2, column=0, padx=5, pady=8)
    label_new_mail = Label(sign_up, text="绑定邮箱：", font=('GB2312', 12))
    label_new_mail.grid(row=3, column=0, padx=5, pady=8)
    label_new_pin = Label(sign_up, text="验证码：", font=('GB2312', 12))
    label_new_pin.grid(row=4, column=0, padx=5, pady=8)
    # 文本
    entry_new_user = Entry(sign_up, width=22, font=('GB2312', 16))
    entry_new_user.grid(row=0, column=1, sticky=W)
    entry_new_pwd = Entry(sign_up, width=22, show="*", font=('GB2312', 16))
    entry_new_pwd.grid(row=1, column=1, sticky=W)
    entry_new_pwd2 = Entry(sign_up, width=22, show="*", font=('GB2312', 16))
    entry_new_pwd2.grid(row=2, column=1, sticky=W)
    entry_new_mail = Entry(sign_up, width=22, font=('GB2312', 16))
    entry_new_mail.grid(row=3, column=1, sticky=W)
    entry_new_pin = Entry(sign_up, width=6, font=('GB2312', 16))
    entry_new_pin.grid(row=4, column=1, sticky=W)
    # 按钮
    button_new_mail = Button(sign_up, text="发送验证码", command=mail)
    button_new_mail.grid(row=4, column=1, pady=5)
    button_new_user = Button(sign_up, text="注册", command=prove_user)
    button_new_user.grid(row=4, column=1, ipadx=20, ipady=5, pady=5, sticky=E)


# #########################修改界面#########################
def forget_pwd():
    xxxx = random.randint(1000, 9999)

    # 发送邮件
    def mail():
        try:
            my_sender = 'ls12345666@qq.com'     # 发件人邮箱账号
            my_pass = 'dsyzyeeftoyzcddb'        # 发件人邮箱密码(当时申请smtp给的口令)
            my_user = entry_set_mail.get()      # 收件人邮箱账号，我这边发送给自己
            msg = MIMEText(str(xxxx), 'plain', 'utf-8')
            msg['From'] = formataddr(["Shuai", my_sender])      # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = formataddr(["收件人昵称", my_user])
            msg['Subject'] = "密码找回!!!"                      # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)       # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)                    # 括号中对应的是发件人邮箱账号、邮箱密码
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            server.quit()  # 关闭连接
        except smtplib.SMTPRecipientsRefused:
            messagebox.showwarning(title="警告信息", message="验证码发送失败!\n请检查您的邮箱是否填写正确！")
        except smtplib.SMTPServerDisconnected:
            messagebox.showwarning(title="警告信息", message="验证码发送失败!\n网络问题，请更换网络后重试")

    def reset_pwd():
        # 查询当前邮箱的密码
        pwd_sql = "SELECT password FROM user_info WHERE email =%s"
        value = entry_set_mail.get()
        cur.execute(pwd_sql, value)
        pwd = cur.fetchone()
        # 查询数据
        email = []
        query = "SELECT * FROM user_info"
        cur.execute(query)
        results = cur.fetchall()
        # 遍历邮箱
        for i in results:
            email.append(i[3])
        if entry_set_mail.get() == '':
            messagebox.showwarning(title="警告信息", message="未填写邮箱")
        elif entry_set_mail.get() not in email:
            messagebox.showwarning(title="警告信息", message="此邮箱未绑定任何账号")
        elif entry_set_pwd.get() == '':
            messagebox.showwarning(title="警告信息", message="密码不能为空，且不能低于6位")
        elif len(entry_set_pwd.get()) < 6:
            messagebox.showwarning(title="警告信息", message="密码不能低于6位数")
        elif entry_set_pwd.get() != entry_set_pwd2.get():
            messagebox.showwarning(title="警告信息", message="两次输入的密码不一致")
        elif entry_set_pwd.get() == pwd[0]:
            messagebox.showwarning(title="警告信息", message="新密码不能与原密码相同")
        elif entry_set_pin.get() == '':
            messagebox.showwarning(title="警告信息", message="请输入验证码")
        elif entry_set_pin.get() != str(xxxx):
            messagebox.showwarning(title="警告信息", message="验证码错误")
        else:
            # 修改数据
            up = "UPDATE user_info SET password=%s WHERE email =%s"
            value = (entry_set_pwd.get(), entry_set_mail.get())
            cur.execute(up, value)
            db.commit()
            messagebox.showinfo(title="通知信息", message="密码已修改成功")
            reset.destroy()
    # 基本属性
    reset = Toplevel(root)
    reset.title("忘记密码")
    reset.geometry("365x180+300+150")
    # 标签
    label_set_user = Label(reset, text="邮      箱：", font=('GB2312', 12))
    label_set_user.grid(row=0, column=0, ipadx=20, ipady=5, pady=5)
    label_set_pwd = Label(reset, text="新  密  码：", font=('GB2312', 12))
    label_set_pwd.grid(row=1, column=0, ipadx=20, ipady=5, pady=5)
    label_set_pwd2 = Label(reset, text="确认新密码：", font=('GB2312', 12))
    label_set_pwd2.grid(row=2, column=0, ipadx=20, ipady=5, pady=5)
    label_set_pin = Label(reset, text="验  证  码：", font=('GB2312', 12))
    label_set_pin.grid(row=3, column=0, ipadx=20, ipady=5, pady=5)
    # 文本
    entry_set_mail = Entry(reset, width=18, font=('GB2312', 16))
    entry_set_mail.grid(row=0, column=1, sticky=W)
    entry_set_pwd = Entry(reset, width=18, font=('GB2312', 16), show="*")
    entry_set_pwd.grid(row=1, column=1, sticky=W)
    entry_set_pwd2 = Entry(reset, width=18, font=('GB2312', 16), show="*")
    entry_set_pwd2.grid(row=2, column=1, sticky=W)
    entry_set_pin = Entry(reset, width=6, font=('GB2312', 16))
    entry_set_pin.grid(row=3, column=1, sticky=W)
    # 按钮
    button_set_mail = Button(reset, text="发送验证码", command=mail)
    button_set_mail.grid(row=3, column=1, sticky=W, padx=75)
    button_set_affirm = Button(reset, text="确定", command=reset_pwd)
    button_set_affirm.grid(row=3, column=1, sticky=W, padx=150, ipadx=10)


# 登录
def login_user():
    name = []
    pwd = []
    query = "SELECT * FROM user_info"
    cur.execute(query)
    results = cur.fetchall()
    # 遍历所有的用户名和密码，并加入到列表中
    for i in results:
        name.append(i[1])
        pwd.append(i[2])
    # 判断用户是否存在
    if entry_user_name.get() not in name:
        messagebox.showerror(title="警告信息", message='该用户不存在')
        if messagebox.askokcancel(title='通知信息', message="是否注册为新用户？"):
            add_user()
    # 判断输入的用户名和密码是否正确
    elif entry_user_name.get() in name and entry_user_pwd.get() == pwd[name.index(entry_user_name.get())]:
        messagebox.showinfo(title="欢迎登录", message='登录成功：' + entry_user_name.get())
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
root.title('login')
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
label_name = Label(root, text="用户名：", fg='red', font=('GB2312', 16))
label_name.grid(row=1, column=0, sticky=W, padx=10)
label_pwd = Label(root, text="密  码：", fg='red', font=('GB2312', 16))
label_pwd.grid(row=2, column=0, sticky=W, padx=10)

# 文本
entry_user_name = Entry(root, width=22, font=('GB2312', 20))
entry_user_name.grid(row=1, column=0, sticky=W, padx=120, pady=10)
entry_user_pwd = Entry(root, width=22, font=('GB2312', 20), show="*")
entry_user_pwd.grid(row=2, column=0, sticky=W, padx=120, pady=10)

# 按钮
button_add_user = Button(root, text="注    册", command=add_user)
button_add_user.grid(row=3, column=0, sticky=W, padx=120, ipadx=20, ipady=10)
button_login_user = Button(root, text="登录", command=login_user)
button_login_user.grid(row=3, column=0, sticky=E, padx=300, ipadx=50, ipady=10)
button_forget_pwd = Button(root, text="忘记密码", command=forget_pwd)
button_forget_pwd.grid(row=3, column=0, sticky=W, padx=10, ipadx=20, ipady=10)

# 主事件循环
root.mainloop()
