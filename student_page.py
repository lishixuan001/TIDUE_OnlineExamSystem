import tkinter as tk
import os
import pickle
import pandas as pd
import tkinter.messagebox


class StudentPage(object):

    def __init__(self, basedir, username):

        self.basedir = basedir
        self.username = username
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        # Label Pack
        label = tk.Label(self.window, font=('Arial', 24), width=30, text="您好 {}".format(username))
        label.pack(fill=None, pady=20)

        # Button Pack
        start_button = tk.Button(self.window, bg="green", text='开始考试', width=30, height=5, command=self.go_test)
        start_button.pack(pady=20)

        # Label Pack
        label = tk.Label(self.window, font=('Arial', 18), width=30, text="考试期间不可退出!")
        label.pack(fill=None, pady=20)

        back_button = tk.Button(self.window, bg="gray", text='返回登陆页', width=10, height=2, command=self.go_login)
        back_button.pack(pady=20)

        # Window Run   
        self.window.mainloop()

    def go_test(self):
        from test_page import TestPage 
        self.window.destroy()
        TestPage(basedir=self.basedir, username=self.username)

    def go_login(self):
        from login_page import LoginPage
        self.window.destroy()
        LoginPage(basedir=self.basedir)