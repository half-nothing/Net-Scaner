from module.tk_module.windows_root import windows
from tkinter import Text
from tkinter import END


def logger(message: str | bytes):
    if isinstance(message, bytes):
        message = message.decode()
    output_log_text.insert(END, message)
    output_log_text.see(END)


# 定义消息输出
output_log_text = Text(windows)
output_log_text.place(x=0, rely=0.5, relheight=0.47, relwidth=1)
