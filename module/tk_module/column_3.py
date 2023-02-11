from tkinter.simpledialog import askstring, askinteger
from tkinter import Checkbutton, Entry, Label
from tkinter import DISABLED, NORMAL
from tkinter import END
from tkinter import BooleanVar


def skip_port():
    if skip_port_value.get():
        skip_port_entry.configure(state=NORMAL)
        data = askstring("输入要跳过的端口", "格式：\n22 | 1-65565 | 22,21,80,443")
        if data is None or data == "":
            skip_port_check_button.deselect()
            skip_port_entry.configure(state=DISABLED)
        else:
            skip_port_entry.delete(0, END)
            skip_port_entry.insert(END, data)
            skip_port_entry.configure(state=DISABLED)


def thread_num():
    if set_thread_num_value.get():
        set_thread_num_entry.configure(state=NORMAL)
        data = askinteger("输入期望使用的线程数", "PS:此\"线程\"非彼\"线程\"\n默认值: 600")
        if data is None:
            set_thread_num_button.deselect()
            set_thread_num_entry.delete(0, END)
            set_thread_num_entry.insert(END, "600")
            set_thread_num_entry.configure(state=DISABLED)
        else:
            set_thread_num_entry.delete(0, END)
            set_thread_num_entry.insert(END, str(data))
            set_thread_num_entry.configure(state=DISABLED)


skip_port_value = BooleanVar()
skip_port_check_button = Checkbutton(text="设置排除端口", variable=skip_port_value, onvalue=True, offvalue=False, command=skip_port)
skip_port_check_button.place(x=480, y=75)
Label(text="扫描端口:").place(x=480, y=97)
skip_port_entry = Entry(state=DISABLED)
skip_port_entry.place(x=485, y=120, width=200)
set_thread_num_value = BooleanVar()
set_thread_num_button = Checkbutton(text="设置扫描线程数", variable=set_thread_num_value, onvalue=True, offvalue=False, command=thread_num)
set_thread_num_button.place(x=480, y=145)
Label(text="并发线程数:").place(x=480, y=167)
set_thread_num_entry = Entry(state=DISABLED)
set_thread_num_entry.place(x=485, y=190, width=200)
