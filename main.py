from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen, PIPE
from tkinter import Tk, Button, Text, Menu, Label, Radiobutton, Checkbutton, Entry
from tkinter import HORIZONTAL, END, IntVar, X, BooleanVar, ACTIVE, DISABLED, NORMAL, RIGHT, BOTTOM
from tkinter import messagebox
from tkinter.simpledialog import askstring
from re import match as rematch
from tkinter.ttk import Separator, Combobox
from os.path import exists, join
from socket import getaddrinfo
from typing import Union
from tkinter.filedialog import askopenfilename
from module.ReadLanguage import language
from os import getcwd
from asyncio.tasks import sleep
from asyncio.runners import run

isIp: bool = True
host: str = ""
subnetMask: int = 0
savePath: str = None
log = "----------------------------------------------------------------------\n{result}\n----------------------------------------------------------------------"

# 初始化类窗体类
windows = Tk()


def queryIp():
    global isIp, host
    if isIp:
        messagebox.showinfo("Info", language.alreadyIpaddress)
    else:
        if DNSport.get() == 0:
            messagebox.showerror("Error", language.noPort)
        else:
            host = getaddrinfo(host, DNSport.get())[0][4][0]
            module1OutputText.configure(state=NORMAL)
            module1OutputText.delete(1.0, END)
            module1OutputText.insert(END, host)
            isIp = True
            module1OutputText.configure(state=DISABLED)
            queryIpButton.configure(state=DISABLED)


def showHost():
    global isIp, host, subnetMask
    module1OutputText.configure(state=NORMAL)
    data = askstring('Please enter', language.effectIpOrUrls)
    if data is None:
        return
    if rematch("^\\b((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\b$", data):
        subnetMask = SubnetMask.get()
        if subnetMask != 0:
            host = data + f"/{subnetMask}"
            module1OutputText.delete(1.0, END)
            module1OutputText.insert(END, host)
        else:
            host = data
            module1OutputText.delete(1.0, END)
            module1OutputText.insert(END, host)
    elif rematch("^\\b((?!-)[A-Za-z\\d-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}\\b$", data):
        isIp = False
        module1OutputText.delete(1.0, END)
        module1OutputText.insert(END, data)
        host = data
        queryIpButton.configure(state=NORMAL)
    else:
        messagebox.showerror("Error", language.effectIpOrUrls)
        showHost()
    module1OutputText.configure(state=DISABLED)
    module1OutputLabel.configure(text=language.ipAddress)
    startScanButton.configure(state=NORMAL)


def logger(message: str):
    logOutput.insert(END, message + "\n")
    logOutput.see(END)


def confirmExit():
    res = messagebox.askokcancel("Confirm", language.confirmQuit)
    if res:
        windows.destroy()
    else:
        return

def RunCommand(command: list, pool: ThreadPoolExecutor):
    logger(log.format(result=Popen(command, stdout=PIPE).communicate()[0].decode()))
    logger(language.finishing)
    pool.shutdown()

def startScan():
    global host
    pool = ThreadPoolExecutor(max_workers=2)
    if not exists("fscan64.exe"):
        messagebox.showerror("Error!", f"{language.cantFindFile.format(filename='fscan64.exe')}\n"
                                       "https://github.com/shadow1ng/fscan/releases")
        return
    # if agent.get():
    #     match agentType.get():

    if isIp:
        logger(language.scanning)
        pool.submit(RunCommand, [".\\fscan64.exe", "-h", host], pool)
    else:
        logger(language.scanning)
        pool.submit(RunCommand, [".\\fscan64.exe", "-u", host], pool)


def EnableAgent():
    agentTypeProxy.configure(state=ACTIVE)
    agentTypeSocks5.configure(state=ACTIVE)
    match agentType.get():
        case 1:
            agentAddress.configure(state=DISABLED)
        case 2:
            agentAddress.configure(state=NORMAL)


def DisableAgent():
    agentTypeProxy.configure(state=DISABLED)
    agentTypeSocks5.configure(state=DISABLED)
    agentAddress.configure(state=DISABLED)


def ProxyAddress():
    agentAddress.configure(state=NORMAL)
    agentAddress.delete(1.0, END)
    address = CheckProxy(askstring(language.getAgentAddressTitle, language.getAgentAddressInfo.format(type="Http")),
                         "Http")
    if address is None:
        agentAddress.insert(END, "http://127.0.0.1:8080")
    else:
        agentAddress.insert(END, address)
    agentAddress.configure(state=DISABLED)


def SocketAddress():
    agentAddress.configure(state=NORMAL)
    agentAddress.delete(1.0, END)
    address = CheckProxy(askstring(language.getAgentAddressTitle, language.getAgentAddressInfo.format(type="Socket")),
                         "Socket")
    if address is None:
        agentAddress.insert(END, "socks5://127.0.0.1:1080")
    else:
        agentAddress.insert(END, address)
    agentAddress.configure(state=DISABLED)


def CheckProxy(address: str, connectType: str) -> Union[str, None]:
    if address is None:
        return None
    if rematch(
            "^\\b(((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)|((?!-)[A-Za-z\\d-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}):(6553[0-5]|655[0-2]\\d|65[0-4]\\d{2}|6[0-4]\\d{3}|[1-5]\\d{4}|[1-9]\\d{1,3}|\\d)\\b$",
            address) is None:
        messagebox.showerror("Error", language.invalidAgentAddress)
        return CheckProxy(
            askstring(language.getAgentAddressTitle, language.getAgentAddressInfo.format(type=connectType)),
            connectType)
    else:
        if connectType == "Http":
            return f"http://{address}"
        elif connectType == "Socket":
            return f"socks5://{address}"


def Subnet():
    global host
    if SubnetMask.get() != 0:
        host = f"{host.split('/')[0]}/{SubnetMask.get()}"
        module1OutputText.configure(state=NORMAL)
        module1OutputText.delete(1.0, END)
        module1OutputText.insert(END, host)
        module1OutputText.configure(state=DISABLED)


def FromFile():
    global host, isIp
    host = askopenfilename(title=language.choiceTxt, filetypes=[('TXT', '*.txt'), ('All Files', '*')], initialdir='.\\')
    if messagebox.askyesno("Question", language.whetherUrl):
        isIp = False
    module1OutputLabel.configure(text=language.fileName)
    module1OutputText.configure(state=NORMAL)
    module1OutputText.delete(1.0, END)
    module1OutputText.insert(END, host)
    module1OutputText.see(END)
    module1OutputText.configure(state=DISABLED)
    queryIpButton.configure(state=DISABLED)
    startScanButton.configure(state=NORMAL)
    updateSubnetMaskButton.configure(state=DISABLED)


def ChoiceSaveFile():
    global savePath
    savePath = askopenfilename(title=language.choiceTxt, filetypes=[('TXT', '*.txt'), ('All Files', '*')],
                               initialdir='.\\')
    if savePath == "":
        savePath = join(getcwd(), "result.txt")
    outputFilePath.configure(state=NORMAL)
    outputFilePath.delete(1.0, END)
    outputFilePath.insert(END, savePath)
    outputFilePath.see(END)
    outputFilePath.configure(state=DISABLED)


def DelSaveFile():
    outputFilePath.configure(state=NORMAL)
    outputFilePath.delete(1.0, END)
    outputFilePath.configure(state=DISABLED)

def Limit():
    if webPoc.get():
        pocLimit.configure(state=DISABLED)
    else:
        pocLimit.configure(state=NORMAL)


# 第一模块
# 静态资源
Label(windows, text=language.port).place(x=630, y=0, width=60, height=20)
Label(windows, text=language.subnetMask).place(x=680, y=0, width=100)
Label(windows, text=language.saveResult).place(x=820, y=0, width=120)
# 单选复选取值定义
DNSport = IntVar()
SubnetMask = IntVar()
SaveFile = BooleanVar()
# 单选复选定义
Radiobutton(windows, text="80", variable=DNSport, value=80).place(x=645, y=20)
Radiobutton(windows, text="443", variable=DNSport, value=443).place(x=645, y=40)
Combobox(windows, textvariable=SubnetMask,
         values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                 26, 27, 28, 29, 30, 31, 32]).place(x=705, y=30, width=100)
Radiobutton(windows, text=language.save, variable=SaveFile, command=ChoiceSaveFile, value=True).place(x=820, y=20)
Radiobutton(windows, text=language.doNotSave, variable=SaveFile, command=DelSaveFile, value=False).place(x=820, y=40)
# 按钮定义
updateSubnetMaskButton = Button(windows, text=language.updateSubnetMask, command=Subnet)
inputButton = Button(windows, command=showHost, text=language.enterAddress)
fromfileButton = Button(windows, command=FromFile, text=language.fromFile)
queryIpButton = Button(windows, command=queryIp, text=language.getIpAddress, state=DISABLED)
startScanButton = Button(windows, command=startScan, text=language.startScan, state=DISABLED)
updateSubnetMaskButton.place(x=475, y=30, width=140)
inputButton.place(x=15, y=30, width=100)
fromfileButton.place(x=130, y=30, width=100)
queryIpButton.place(x=245, y=30, width=100)
startScanButton.place(x=360, y=30, width=100)
# 信息输出
module1OutputText = Text(windows, state=DISABLED)
module1OutputText.place(x=100, y=5, width=520, height=20)
module1OutputLabel = Label(windows, text=language.ipAddress)
module1OutputLabel.place(x=15, y=5, width=80, height=20)
outputFilePath = Text(windows, state=DISABLED)
outputFilePath.place(x=890, y=22, height=40, width=120)

# 第二模块
# 静态资源
Label(windows, text=language.enableAgent).place(x=15, y=77)
Label(windows, text=language.agentAddress).place(x=15, y=117)
Label(windows, text=language.agentType).place(x=15, y=97)
# 单选框取值定义
enableAgent = BooleanVar()
agentType = IntVar()
# 单选框定义
Radiobutton(windows, text=language.enable, command=EnableAgent, variable=enableAgent, value=True).place(x=100, y=75)
Radiobutton(windows, text=language.disable, command=DisableAgent, variable=enableAgent, value=False).place(x=170, y=75)
agentTypeProxy = Radiobutton(windows, text="proxy", command=ProxyAddress, state=DISABLED, variable=agentType, value=1)
agentTypeSocks5 = Radiobutton(windows, text="socks5", command=SocketAddress, state=DISABLED, variable=agentType,
                              value=2)
agentTypeProxy.place(x=100, y=95)
agentTypeSocks5.place(x=170, y=95)
# 第二模块输出
agentAddress = Text(windows, state=DISABLED)
agentAddress.place(x=20, y=137, height=20, width=205)


# 第三模块
# 静态资源
Label(text=language.limit).place(x=15, y=200)
Label(text=language.cookie).place(x=15, y=280)
# 复选框取值定义
password = BooleanVar()
webPoc = BooleanVar()
survival = BooleanVar()
cookie = BooleanVar()
Checkbutton(text=language.password, variable=password, onvalue=True, offvalue=False).place(x=15, y=157)
Checkbutton(text=language.webPoc, variable=webPoc, onvalue=True, offvalue=False, command=Limit).place(x=15, y=177)
pocLimit = Entry()
pocLimit.insert(END, 20)
pocLimit.place(x=20, y=220, width=205)
Checkbutton(text=language.survival, variable=survival, onvalue=True, offvalue=False).place(x=15, y=240)
Checkbutton(text=language.setCookie, variable=cookie, onvalue=True, offvalue=False).place(x=15, y=260)
cookie = Text(state=DISABLED)
cookie.place(x=20, y=300, width=205, height=50)

# 分割线
line1 = Separator(windows, orient=HORIZONTAL)
line1.place(x=0, y=70, relwidth=1)

# 定义消息输出
logOutput = Text(windows)
logOutput.place(x=0, rely=0.5, relheight=0.47, relwidth=1)

# 原作者连接显示
github = Label(windows, text=language.added.format(url="https://github.com/shadow1ng/fscan"))
github.pack(fill=X, side=BOTTOM)

# 菜单
MainMenu = Menu(windows)
FileMenu = Menu(MainMenu, tearoff=False)
AboutMenu = Menu(MainMenu, tearoff=False)
FileMenu.add_command(label=language.exit, command=confirmExit)
AboutMenu.add_command(label=language.other.setting)
AboutMenu.add_command(label=language.other.about)
MainMenu.add_cascade(label=language.file, menu=FileMenu)
MainMenu.add_cascade(label=language.other.title, menu=AboutMenu)

# 退出确认
windows.protocol("WM_DELETE_WINDOW", confirmExit)

# 窗口标题
windows.title("Net Scaner")

# 窗口大小
windows.geometry("1024x720")

# 运行窗口
windows.config(menu=MainMenu)
windows.mainloop()
