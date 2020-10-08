import tkinter as tk
import os
import pickle
import pandas as pd
import tkinter.messagebox


class AdminPage(object):

    def __init__(self, basedir):
        self.basedir = basedir
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        # Label Pack
        label = tk.Label(self.window, font=('Arial', 24), width=30, text="管理员")
        label.pack(fill=None, pady=30)

        # Button Pack
        users_button = tk.Button(self.window, bg="pink", text='查看人员信息', width=25, height=6, command=self.go_users)
        users_button.pack(fill=None, pady=10)
        exams_button = tk.Button(self.window, bg="yellow", text='查看试题内容', width=25, height=6, command=self.go_exams)
        exams_button.pack(fill=None, pady=10)
        back_button = tk.Button(self.window, bg="gray", text='返回登陆页', width=10, height=2, command=self.go_login)
        back_button.pack(pady=20)

        # Window Run
        self.window.mainloop()

    def go_users(self):
        from users_page import UsersPage
        self.window.destroy()
        UsersPage(basedir=self.basedir)

    def go_exams(self):
        from exams_page import ExamsPage
        self.window.destroy()
        ExamsPage(basedir=self.basedir)

    def go_login(self):
        from login_page import LoginPage
        self.window.destroy()
        LoginPage(basedir=self.basedir)
