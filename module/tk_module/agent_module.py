from tkinter.simpledialog import askstring
from module.config import regular_expression
from tkinter import Label, Radiobutton, Entry, messagebox
from tkinter import BooleanVar, IntVar
from tkinter import DISABLED, ACTIVE, NORMAL, END
from typing import Union
from re import match as rematch


def check_proxy(address: str, connectType: str) -> Union[str, None]:
    if address is None:
        return None
    if rematch(regular_expression.agent_address, address) is None:
        messagebox.showerror("错误", "无效代理地址")
        return check_proxy(askstring("请输入代理地址", f"请输入有效的{connectType}代理地址\n格式为\"xxx.xxx.xxx.xxx:xxxx\""), connectType)
    else:
        if connectType == "Http":
            return f"http://{address}"
        elif connectType == "Socket":
            return f"socks5://{address}"


def enable_agent():
    agent_type_proxy.configure(state=ACTIVE)
    agent_type_socks5.configure(state=ACTIVE)
    match agent_type_value.get():
        case 1:
            agent_address.configure(state=DISABLED)
        case 2:
            agent_address.configure(state=NORMAL)


def disable_agent():
    agent_type_proxy.configure(state=DISABLED)
    agent_type_socks5.configure(state=DISABLED)
    agent_address.configure(state=DISABLED)


def proxy_address():
    agent_address.configure(state=NORMAL)
    agent_address.delete(0, END)
    address = check_proxy(askstring("请输入代理地址", f"请输入有效的Http代理地址\n格式为\"xxx.xxx.xxx.xxx:xxxx\""), "Http")
    if address is None:
        agent_address.insert(END, "http://127.0.0.1:10809")
    else:
        agent_address.insert(END, address)
    agent_address.configure(state=DISABLED)


def socket_address():
    agent_address.configure(state=NORMAL)
    agent_address.delete(0, END)
    address = check_proxy(askstring("请输入代理地址", f"请输入有效的Socket代理地址\n格式为\"xxx.xxx.xxx.xxx:xxxx\""), "Socket")
    if address is None:
        agent_address.insert(END, "socks5://127.0.0.1:10808")
    else:
        agent_address.insert(END, address)
    agent_address.configure(state=DISABLED)


# 静态资源
Label(text="是否启用代理:").place(x=15, y=77)
Label(text="代理地址:").place(x=15, y=117)
Label(text="代理类型:").place(x=15, y=97)
# 单选框取值定义
enable_agent_value = BooleanVar()
agent_type_value = IntVar()
# 单选框定义
Radiobutton(text="启用", command=enable_agent, variable=enable_agent_value, value=True).place(x=100, y=75)
Radiobutton(text="不启用", command=disable_agent, variable=enable_agent_value, value=False).place(x=170, y=75)
agent_type_proxy = Radiobutton(text="proxy", command=proxy_address, state=DISABLED, variable=agent_type_value, value=1)
agent_type_socks5 = Radiobutton(text="socks5", command=socket_address, state=DISABLED, variable=agent_type_value, value=2)
agent_type_proxy.place(x=100, y=95)
agent_type_socks5.place(x=170, y=95)
# 第二模块输出
agent_address = Entry(state=DISABLED)
agent_address.place(x=20, y=137, height=20, width=205)
