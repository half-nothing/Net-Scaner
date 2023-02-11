from tkinter import Label, Checkbutton, Entry, Text
from tkinter import END, DISABLED, NORMAL
from tkinter import BooleanVar
from module.tk_module.column_2 import ping_or_icmp_check_button


def limit():
    if web_poc_value.get():
        poc_limit_entry.configure(state=DISABLED)
    else:
        poc_limit_entry.configure(state=NORMAL)


def set_cookie():
    if cookie_value.get():
        cookie_info_text.configure(state=NORMAL)
    else:
        cookie_info_text.configure(state=DISABLED)


def jump_survival():
    if survival_value.get():
        ping_or_icmp_check_button.deselect()
        ping_or_icmp_check_button.configure(state=DISABLED)
    else:
        ping_or_icmp_check_button.configure(state=NORMAL)


password_value = BooleanVar()
web_poc_value = BooleanVar()
survival_value = BooleanVar()
cookie_value = BooleanVar()
Label(text="cookie:").place(x=15, y=280)
Label(text="发包速率:").place(x=15, y=200)
Checkbutton(text="跳过sql、ftp、ssh等的密码爆破", variable=password_value, onvalue=True, offvalue=False).place(x=15, y=157)
Checkbutton(text="跳过web poc扫描", variable=web_poc_value, onvalue=True, offvalue=False, command=limit).place(x=15, y=177)
poc_limit_entry = Entry()
poc_limit_entry.insert(END, "20")
poc_limit_entry.place(x=20, y=220, width=200)
Checkbutton(text="跳过存活探测", variable=survival_value, onvalue=True, offvalue=False, command=jump_survival).place(x=15, y=240)
Checkbutton(text="设置cookie", variable=cookie_value, onvalue=True, offvalue=False, command=set_cookie).place(x=15, y=260)
cookie_info_text = Text(state=DISABLED)
cookie_info_text.place(x=20, y=300, width=200, height=50)
