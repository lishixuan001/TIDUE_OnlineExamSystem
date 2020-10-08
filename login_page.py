import tkinter as tk
import tkinter.messagebox
import os
import pickle
import pandas


class LoginPage(object):

    def __init__(self, basedir):

        self.basedir = basedir
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        # Label Pack
        label = tk.Label(self.window, font=('Arial', 24), width=30, text="登陆")
        label.pack(fill=None, pady=30)

        # Entry Pack
        username_label = tk.Label(self.window, anchor='w', font=('Arial', 14), width=20, text="用户名")
        username_label.pack(fill=None, pady=0)
        self.username_entry = tk.Entry(self.window, show=None, width=20, font=('Arial', 14))
        self.username_entry.pack(fill=None, pady=10)
        password_label = tk.Label(self.window, anchor='w', font=('Arial', 14), width=20, text="密码")
        password_label.pack(fill=None, pady=0)
        self.password_entry = tk.Entry(self.window, show='*', width=20, font=('Arial', 14))
        self.password_entry.pack(fill=None, pady=10)

        # Load Database
        self.load_users_database()

        # Button Pack
        submit_button = tk.Button(self.window, text='确定', width=15, height=2, command=self.login_action)
        submit_button.pack()

        # Window Run
        self.window.mainloop()

    def load_users_database(self):
        with open(os.path.join(self.database_dir, "users.pickle"), 'rb') as users_data_file:
            self.users_df = pickle.load(users_data_file)

    def login_action(self):
        username_entry = self.username_entry.get()
        password_entry = self.password_entry.get()
        query = self.users_df[(self.users_df[['Username','Password']].values == [username_entry, password_entry]).all(axis=1)]
        if query.empty:
            tk.messagebox.showwarning('Error', "用户信息错误")
        else:
            if query["is_admin"][0]:
                self.go_admin()
            else:
                # If legal for test, test; If not, show Label
                if query["Grade"][0] is None:
                    self.go_student(username=username_entry)
                else:
                    tk.messagebox.showwarning('Error', "您已经参加过考试!")

    def go_admin(self):
        from admin_page import AdminPage
        self.window.destroy()
        AdminPage(basedir=self.basedir)

    def go_student(self, username):
        from student_page import StudentPage
        self.window.destroy()
        StudentPage(basedir=self.basedir, username=username)





























