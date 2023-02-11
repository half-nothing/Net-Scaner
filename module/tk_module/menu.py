from module.tk_module.windows_root import windows
from tkinter import Menu, messagebox


def confirm_exit():
    res = messagebox.askokcancel("确认", "确认退出？")
    if res:
        windows.destroy()
    else:
        return


main_menu = Menu(windows)
file_menu = Menu(main_menu, tearoff=False)
about_menu = Menu(main_menu, tearoff=False)
file_menu.add_command(label="退出", command=confirm_exit)
about_menu.add_command(label="设置")
about_menu.add_command(label="关于")
main_menu.add_cascade(label="文件", menu=file_menu)
main_menu.add_cascade(label="其他", menu=about_menu)

windows.protocol("WM_DELETE_WINDOW", confirm_exit)
