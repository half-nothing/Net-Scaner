from subprocess import Popen, PIPE
from tkinter import Tk, Button, Text, Menu, Label, Scrollbar, Radiobutton
from tkinter import HORIZONTAL, VERTICAL, END, IntVar, Y, BooleanVar, ACTIVE, DISABLED
from tkinter import messagebox
from tkinter.simpledialog import askstring
from re import match as rematch
from tkinter.ttk import Separator, Combobox
from os.path import exists
from socket import getaddrinfo

isIp: bool = True
host: str = ""
subnetMask: int = 0
# 初始化类窗体类
windows = Tk()


def queryIp():
    global isIp, host
    if isIp:
        messagebox.showinfo("Info", "已经是ip地址，无需查询")
    else:
        if DNSport.get() == 0:
            messagebox.showerror("Error", "未指定DNS查询端口")
        else:
            host = getaddrinfo(host, DNSport.get())[0][4][0]
            label1.config(text=host)
            isIp = True


def showHost():
    global isIp, host, subnetMask
    data = askstring('请输入', '请输入有效的ip地址或域名')
    if data is None:
        return
    if rematch("^\\b((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\b", data):
        subnetMask = SubnetMask.get()
        if subnetMask != 0:
            host = data + f"/{subnetMask}"
            label1.config(text=host)
        else:
            host = data
            label1.config(text=host)
    elif rematch("^\\b((?!-)[A-Za-z\\d-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}\\b$", data):
        isIp = False
        label1.config(text=data)
        host = data
    else:
        messagebox.showerror("错误", "请输入有效的ip地址或域名")
        showHost()


def logger(message: str):
    logOutput.insert(END, message + "\n")
    logOutput.see(END)


def confirmExit():
    res = messagebox.askokcancel("确认退出", "确认退出？")
    if res:
        windows.destroy()
    else:
        return


def startScan():
    global host
    if not exists("fscan64.exe"):
        messagebox.showerror("Error!", "无法找到fscan64.exe文件，请前往作者github下载\n"
                                       "https://github.com/shadow1ng/fscan/releases")
        return
    # if agent.get():
    #     match agentType.get():
    if isIp:
        logger("----------------------------------------------------------------------")
        logger(Popen([".\\fscan64.exe", "-h", host], stdout=PIPE).communicate()[0].decode())
        logger("----------------------------------------------------------------------")
    else:
        logger("----------------------------------------------------------------------")
        logger(Popen([".\\fscan64.exe", "-u", host], stdout=PIPE).communicate()[0].decode())
        logger("----------------------------------------------------------------------")

def EnableAgent():
    agentType1.configure(state=ACTIVE)
    agentType2.configure(state=ACTIVE)

def DisableAgent():
    agentType1.configure(state=DISABLED)
    agentType2.configure(state=DISABLED)


# 定义第一组单选返回值
DNSport = IntVar()
Radiobutton(windows, text="80", variable=DNSport, value=80).place(x=265, y=20)
Radiobutton(windows, text="443", variable=DNSport, value=443).place(x=265, y=40)

# 复选框
SubnetMask = IntVar()
Combobox(windows, textvariable=SubnetMask,
         values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                   26, 27, 28, 29, 30, 31, 32]).place(x=320, y=30)
Label(windows, text="子网掩码:").place(x=320, y=5, width=60)

# 是否启用代理
Label(windows, text="是否启用代理:").place(x=15, y=77)
agent = BooleanVar()
Radiobutton(windows, text="启用", command=EnableAgent, variable=agent, value=True).place(x=100, y=75)
Radiobutton(windows, text="不启用", command=DisableAgent, variable=agent, value=False).place(x=160, y=75)

# 代理类型
Label(windows, text="代理类型:").place(x=15, y=97)
agentType = IntVar()
agentType1 = Radiobutton(windows, text="proxy", state=DISABLED, variable=agentType, value=1)
agentType1.place(x=100, y=95)
agentType2 = Radiobutton(windows, text="socks5", state=DISABLED, variable=agentType, value=2)
agentType2.place(x=160, y=95)

# 代理地址


# 窗口标题
windows.title("Net Scaner")

# 窗口大小
windows.geometry("1024x720")

# 标签
Label(windows, text="端口:").place(x=255, y=5, width=60, height=20)
Label(windows, text="IP地址:").place(x=15, y=5, width=40, height=20)
label1 = Label(windows)
label1.place(x=60, y=5, width=200, height=20)

# 输入地址
inputBox = Button(windows, command=showHost, text="输入地址")
inputBox.place(x=15, y=30, width=70)

# 获取ip
query = Button(windows, command=queryIp, text="获取ip")
query.place(x=90, y=30, width=70)

# 开始扫描
scan = Button(windows, command=startScan, text="开始扫描")
scan.place(x=165, y=30, width=70)

# 分割线
line1 = Separator(windows, orient=HORIZONTAL)
line1.place(x=0, y=70, width=490)

line2 = Separator(windows, orient=VERTICAL)
line2.place(x=490, y=0, height=70)

line3 = Separator(windows, orient=HORIZONTAL)
line3.place(x=0, y=360, relwidth=1)

# 定义消息输出
logOutput = Text(windows)
logOutput.place(x=0, y=361, relheight=0.5, width=1007)

# 滚动条
scroll = Scrollbar(windows)
scroll.pack(fill=Y)
scroll.place(x=1007, y=361, relheight=0.5)

scroll.config(command=logOutput.yview)
logOutput.config(yscrollcommand=scroll.set)

# 原作者连接显示
github = Label(windows, text="本软件只是对别人软件的可视化封装，具体软件的GitHub: https://github.com/shadow1ng/fscan")
github.place(x=0, y=700, relwidth=1, height=20)

# 菜单
MainMenu = Menu(windows)
FileMenu = Menu(MainMenu)
MainMenu.add_cascade(label="文件", menu=FileMenu)
FileMenu.add_command(label="退出", command=confirmExit)

# 退出确认
windows.protocol("WM_DELETE_WINDOW", confirmExit)

# 运行窗口
windows.config(menu=MainMenu)
windows.mainloop()
