from tkinter import Tk, Label, BOTTOM, X
from tkinter import HORIZONTAL
from tkinter.ttk import Separator

windows = Tk()

# 窗口标题
windows.title("Net Scaner")

# 窗口大小
windows.geometry("1024x720")

# 分割线
line1 = Separator(windows, orient=HORIZONTAL)
line1.place(x=0, y=70, relwidth=1)

# 原作者连接显示
github = Label(windows, text="本软件只是对别人软件的可视化封装，具体软件的GitHub=>https://github.com/shadow1ng/fscan")
github.pack(fill=X, side=BOTTOM)
