import tkinter as tk
import os
import pickle
import pandas as pd
import tkinter.messagebox


class GradePage(object):

    def __init__(self, basedir, username, grade):

        self.basedir = basedir
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        self.load_users_database()
        self.users_df.loc[self.users_df['Username'] == username, 'Grade'] = int(grade)
        self.update_users_database()

        # Label Pack
        label = tk.Label(self.window, font=('Arial', 30), width=30, text="您的得分是: [{}]".format(grade))
        label.pack(fill=None, pady=30)

        # Button Pack
        back_button = tk.Button(self.window, bg="gray", text='返回登陆页', width=10, height=2, command=self.go_login)
        back_button.pack(pady=20)

        # Window Run
        self.window.mainloop()

    def load_users_database(self):
        with open(os.path.join(self.database_dir, "users.pickle"), 'rb') as users_data_file:
            self.users_df = pickle.load(users_data_file)

    def update_users_database(self):
        with open(os.path.join(self.database_dir, "users.pickle"), 'wb') as users_data_file:
            pickle.dump(self.users_df, users_data_file)

    def go_login(self):
        from login_page import LoginPage
        self.window.destroy()
        LoginPage(basedir=self.basedir)
