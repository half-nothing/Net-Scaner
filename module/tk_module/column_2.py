from tkinter import Label, Checkbutton, Entry
from tkinter import END, DISABLED, NORMAL
from tkinter import BooleanVar
from tkinter.simpledialog import askstring


def command_():
    if command_value.get():
        ssh_command_entry.configure(state=NORMAL)
    else:
        ssh_command_entry.configure(state=DISABLED)


def time_():
    if timeout_value.get():
        timeout_entry.configure(state=NORMAL)
    else:
        timeout_entry.configure(state=DISABLED)


def set_port():
    if set_port_value.get():
        set_port_entry.configure(state=NORMAL)
        data = askstring("输入扫描端口", "格式：\n22 | 1-65565 | 22,21,80,443")
        if data is None or data == "":
            select_port_check_button.deselect()
            set_port_entry.configure(state=DISABLED)
        else:
            set_port_entry.delete(0, END)
            set_port_entry.insert(END, data)
            set_port_entry.configure(state=DISABLED)


def add_port():
    if add_port_value.get():
        added_port_entry.configure(state=NORMAL)
        data = askstring("输入扫描端口", "格式：\n22 | 1-65565 | 22,21,80,443")
        if data is None or data == "":
            add_port_check_button.deselect()
            added_port_entry.configure(state=DISABLED)
        else:
            added_port_entry.delete(0, END)
            added_port_entry.insert(END, data)
            added_port_entry.configure(state=DISABLED)


def ping():
    return


command_value = BooleanVar()
ping_value = BooleanVar()
timeout_value = BooleanVar()
domain_value = BooleanVar()
set_port_value = BooleanVar()
add_port_value = BooleanVar()

Label(text="要执行的ssh命令:").place(x=250, y=117)
Label(text="超时时间:").place(x=250, y=177)
Label(text="扫描端口:").place(x=250, y=242)
Label(text="扫描端口:").place(x=250, y=305)
Checkbutton(text="扫描完毕执行ssh命令", variable=command_value, onvalue=True, offvalue=False, command=command_).place(x=250, y=95)
ping_or_icmp_check_button = Checkbutton(text="使用ping代替icmp", variable=ping_value, onvalue=True, offvalue=False, command=ping)
ping_or_icmp_check_button.place(x=250, y=75)
ssh_command_entry = Entry(state=DISABLED)
ssh_command_entry.place(x=255, y=137, width=200)
Checkbutton(text="设定超时时间", variable=timeout_value, onvalue=True, offvalue=False, command=time_).place(x=250, y=155)
timeout_entry = Entry()
timeout_entry.insert(END, "60")
timeout_entry.configure(state=DISABLED)
timeout_entry.place(x=255, y=197, width=200)
select_port_check_button = Checkbutton(text="设置扫描端口", variable=set_port_value, onvalue=True, offvalue=False, command=set_port)
select_port_check_button.place(x=250, y=220)
set_port_entry = Entry(state=DISABLED)
set_port_entry.place(x=255, y=262, width=200)
add_port_check_button = Checkbutton(text="添加扫描端口", variable=add_port_value, onvalue=True, offvalue=False, command=add_port)
add_port_check_button.place(x=250, y=282)
added_port_entry = Entry(state=DISABLED)
added_port_entry.place(x=255, y=325, width=200)
