from module.tk_module.windows_root import windows
from module.config import regular_expression
from module.logger import logger
from re import match as rematch
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.ttk import Combobox
from tkinter import Label, Radiobutton, Button, messagebox, Entry, Text
from tkinter import IntVar, BooleanVar
from tkinter import NORMAL, DISABLED
from tkinter import END
from os import getcwd
from os.path import join, exists
from socket import getaddrinfo
from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen, PIPE, STDOUT

from module.tk_module.agent_module import agent_type_value, agent_address, enable_agent_value
from module.tk_module.column_1 import password_value, web_poc_value, survival_value, cookie_value
from module.tk_module.column_1 import poc_limit_entry, cookie_info_text
from module.tk_module.column_2 import ping_value, command_value, timeout_value, set_port_value, add_port_value
from module.tk_module.column_2 import ssh_command_entry, timeout_entry, set_port_entry, added_port_entry
from module.tk_module.column_3 import skip_port_value, set_thread_num_value
from module.tk_module.column_3 import skip_port_entry, set_thread_num_entry

pool = ThreadPoolExecutor(max_workers=10)
result: dict = {}


def judge_ip_and_url(host: str) -> int:
    if rematch(regular_expression.ip_address, host) is not None:
        return 1
    elif rematch(regular_expression.domain_name, host) is not None:
        return 0
    else:
        return -1


def run_command(cmd: list, callback=None) -> None:
    callback("----------------------------------------------------------------------\n")
    callback("扫描中...\n")
    screen_data = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    for info in iter(screen_data.stdout.readline, b''):
        print(info) if callback is None else callback(info)
        if Popen.poll(screen_data) == 0:
            screen_data.stdout.close()
            break
    callback("扫描完成\n")
    callback("----------------------------------------------------------------------")


def start_scan() -> None:
    """
    开始扫描回调函数
    """
    if not exists("fscan64.exe"):
        messagebox.showerror("错误", "无法找到「fscan64.exe」文件，请前往作者github下载\n"
                                     "https://github.com/shadow1ng/fscan/releases")
        return
    cmd = [".\\fscan64.exe", "-h", result["host"]]
    if enable_agent_value.get():
        match agent_type_value.get():
            case 1:
                cmd.append("-proxy")
            case 2:
                cmd.append("-socks5")
        cmd.append(agent_address.get())
    if password_value.get():
        cmd.append("-nobr")
    if web_poc_value.get():
        cmd.append("-nopoc")
    else:
        cmd.append("-num")
        cmd.append(poc_limit_entry.get())
    if survival_value.get():
        cmd.append("-np")
    if cookie_value.get() and cookie_info_text.get(1.0, END + "-1c") != "":
        cmd.append("-cookie")
        cmd.append(cookie_info_text.get(1.0, END + "-1c"))
    if ping_value.get():
        cmd.append("-ping")
    if command_value.get() and ssh_command_entry.get() != "":
        cmd.append("-c")
        cmd.append(ssh_command_entry.get())
    if timeout_value.get():
        cmd.append("-debug")
        cmd.append(timeout_entry.get())
    if set_port_value.get():
        cmd.append("-p")
        cmd.append(set_port_entry.get())
    if not set_port_value.get() and add_port_value.get():
        cmd.append("-pa")
        cmd.append(added_port_entry.get())
    if skip_port_value.get():
        cmd.append("-pn")
        cmd.append(skip_port_entry.get())
    if set_thread_num_value.get():
        cmd.append("-t")
        cmd.append(set_thread_num_entry.get())
    print(str(cmd))
    pool.submit(run_command, cmd, logger)


def query_ip():
    """
    “查询ip”按钮回调函数\n
    """
    if dns_query_port_value.get() == 0:
        messagebox.showerror("错误", "未指定DNS查询端口")
    else:
        try:
            result["host"] = getaddrinfo(result["host"], dns_query_port_value.get())[0][4][0]
        except Exception as err:
            messagebox.showerror("Error", str(err))
        else:
            start_scan_button.configure(state=NORMAL)
            module_output_entry.configure(state=NORMAL)
            module_output_entry.delete(0, END)
            module_output_entry.insert(END, result["host"])
            module_output_entry.configure(state=DISABLED)
            query_ip_button.configure(state=DISABLED)


def input_address() -> None:
    """
    “输入地址”按钮的回调函数\n
    """
    module_output_entry.configure(state=NORMAL)  # 使显示框变成能被编辑的状态
    data = askstring('请输入地址', "请输入有效的ip地址或域名\nPS:域名需要点击'查询ip'按钮")  # 取得输入的数据
    if data is None:  # 如果用户没有输入数据
        module_output_entry.configure(state=DISABLED)  # 设置为不可输入
        return
    match judge_ip_and_url(data):  # 判断是域名还是ip
        case 1:  # 1代表是ip
            subnet_mask = subnet_mask_value.get()  # 读取设置的子网掩码
            result["subnet_mask"] = subnet_mask  # 写入全局
            if subnet_mask != 0:  # 如果不是0
                module_output_entry.delete(0, END)  # 删除原来的内容
                module_output_entry.insert(END, data + f"/{subnet_mask}")  # 连接字符串并输出
            else:
                module_output_entry.delete(0, END)
                module_output_entry.insert(END, data)
            result["host"] = data
            query_ip_button.configure(state=DISABLED)  # 将查询ip的按钮设置为不可点击
            start_scan_button.configure(state=NORMAL)  # 设置开始扫描按钮可点击
            module_output_entry.configure(state=DISABLED)  # 设置为不可输入
        case 0:  # 0代表域名
            module_output_entry.delete(0, END)
            module_output_entry.insert(END, data)
            query_ip_button.configure(state=NORMAL)  # 将查询ip的按钮设置为可点击
            start_scan_button.configure(state=DISABLED)  # 设置开始扫描按钮可点击
            module_output_entry.configure(state=DISABLED)  # 设置为不可输入
            result["host"] = data
        case -1:  # -1代表输入的值非法
            messagebox.showerror("错误", "请输入有效的ip地址或域名")  # 抛出错误
            input_address()  # 重复调用等待下一次输入


def subnet():
    """
    绑定的监听函数\n
    """
    if "host" not in result.keys() or result['host'] == "":
        return
    result['subnet'] = subnet_mask_value.get()
    module_output_entry.configure(state=NORMAL)
    module_output_entry.delete(0, END)
    module_output_entry.insert(END,
                               f"{result['host']}" if result['subnet'] == 0 else f"{result['host']}/{result['subnet']}")
    module_output_entry.configure(state=DISABLED)


def read_from_file():
    """
    “从文件”按钮回调函数\n
    """
    data = askopenfilename(title="选择一个txt文件，里面包含要扫描的IP地址或域名",
                           filetypes=[('TXT', '*.txt'), ('All Files', '*')], initialdir='.\\')  # 选择文件并获取文件路径(绝对路径)
    if data == "":
        return
    result["host"] = data
    module_output_label.configure(text="文件:")
    module_output_entry.configure(state=NORMAL)  # 使文本框可以输入
    module_output_entry.delete(0, END)  # 清空内容
    module_output_entry.insert(END, result["host"])  # 写入内容
    module_output_entry.configure(state=DISABLED)  # 关闭文本框
    query_ip_button.configure(state=DISABLED)  # 关闭查询按钮
    start_scan_button.configure(state=NORMAL)  # 打开扫描按钮


def choice_save_file():
    save_path = askopenfilename(title="选择一个文件", filetypes=[('TXT', '*.txt'), ('All Files', '*')],
                                initialdir='.\\')
    if save_path == "":
        save_path = join(getcwd(), "result.txt")
    output_file_path.configure(state=NORMAL)
    output_file_path.delete(1.0, END)
    output_file_path.insert(END, save_path)
    output_file_path.see(END)
    output_file_path.configure(state=DISABLED)


def del_save_file():
    output_file_path.configure(state=NORMAL)
    output_file_path.delete(1.0, END)
    output_file_path.configure(state=DISABLED)


# 静态资源
Label(windows, text="端口:", ).place(x=630, y=0, width=60, height=20)
Label(windows, text="子网掩码:").place(x=680, y=0, width=100)
Label(windows, text="保存结果到文件：").place(x=820, y=0, width=120)
# 单选复选取值定义
dns_query_port_value = IntVar()
subnet_mask_value = IntVar()
save_file_value = BooleanVar()
# 默认值设置
dns_query_port_value.set(80)
save_file_value.set(False)
# 单选复选定义
Radiobutton(windows, text="80", variable=dns_query_port_value, value=80).place(x=645, y=20)
Radiobutton(windows, text="443", variable=dns_query_port_value, value=443).place(x=645, y=40)
Radiobutton(windows, text="保存", variable=save_file_value, command=choice_save_file, value=True).place(x=820, y=20)
Radiobutton(windows, text="不保存", variable=save_file_value, command=del_save_file, value=False).place(x=820, y=40)
# 按钮定义
# 输入地址，输入的同时判断是否合法
input_button = Button(windows, command=input_address, text="输入地址")
input_button.place(x=15, y=30, width=140)
# 从文件读取内容
read_from_file_button = Button(windows, command=read_from_file, text="从文件导入")
read_from_file_button.place(x=175, y=30, width=140)
# 获取ip
query_ip_button = Button(windows, command=query_ip, text="获取ip", state=DISABLED)
query_ip_button.place(x=335, y=30, width=140)
# 开始扫描
start_scan_button = Button(windows, command=start_scan, text="开始扫描", state=DISABLED)
start_scan_button.place(x=495, y=30, width=140)
# 复选框
subnet_combobox = Combobox(windows, textvariable=subnet_mask_value, state="readonly")
subnet_combobox.place(x=705, y=30, width=100)
subnet_combobox["value"] = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    31,
    32)
subnet_combobox.current(0)
subnet_combobox.bind('<<ComboboxSelected>>', lambda event: subnet())
# 信息输出
module_output_entry = Entry(windows, state=DISABLED)
module_output_entry.place(x=100, y=5, width=535, height=20)
module_output_label = Label(windows, text="IP地址:")
module_output_label.place(x=15, y=5, width=80, height=20)
output_file_path = Text(windows, state=DISABLED)
output_file_path.place(x=890, y=22, height=40, width=120)
