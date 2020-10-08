import tkinter as tk
import tkinter.messagebox
import os
import pickle
import pandas as pd

class UsersPage(object):

    def __init__(self, basedir):
        self.basedir = basedir
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('Online Exam System')
        self.window.geometry('800x500')

        # Listbox Pack
        self.load_users_database()
        self.listbox = tk.Listbox()
        self.listbox.pack(pady=10)
        self.update_listbox()

        # Add New
        self.userinfo_entry = tk.Entry(self.window, show=None, width=20, font=('Arial', 14))
        self.userinfo_entry.pack(fill=None, pady=10)
        add_button = tk.Button(self.window, text='添加人员', width=20, height=3, command=self.add_new)
        add_button.pack()

        # Delete Selected
        delete_button = tk.Button(self.window, text='删除人员', width=20, height=3, command=self.delete_selected)
        delete_button.pack()

        # Remove Grade
        retest_button = tk.Button(self.window, text='清除成绩', width=20, height=3, command=self.remove_grade)
        retest_button.pack()

        # Back Pack
        back_button = tk.Button(self.window, bg="gray", text='返回上一页', width=10, height=2, command=self.go_admin)
        back_button.pack(pady=20)

        # Window Run
        self.window.mainloop()

    def load_users_database(self):
        with open(os.path.join(self.database_dir, "users.pickle"), 'rb') as users_data_file:
            self.users_df = pickle.load(users_data_file)

    def add_new(self):
        userinfo = self.userinfo_entry.get().split(";")
        if len(userinfo) == 3 and len(userinfo[0]) > 0 and len(userinfo[1]) > 0 and (userinfo[2].isnumeric() or userinfo[2] == "-"):
            username, password, grade = userinfo
            if (self.users_df.Username == username).any():
                tk.messagebox.showwarning('Error', "用户名已经存在!")
                return
            grade = int(grade) if grade.isnumeric() else None
            new_dataline = pd.DataFrame(data=[[username, password, False, grade]], columns=self.users_df.columns.tolist())
            self.users_df = pd.concat([self.users_df, new_dataline])
            self.update_users_database()
            self.update_listbox()
            self.userinfo_entry.delete(0, tk.END)
        else:
            tk.messagebox.showwarning('Error', "请按照'用户名;密码;成绩'的格式输入, 如果成绩为空请用‘-’代替")

    def update_users_database(self):
        with open(os.path.join(self.database_dir, "users.pickle"), 'wb') as users_data_file:
            pickle.dump(self.users_df, users_data_file)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, row in self.users_df.iterrows():
            grade = "-" if row["Grade"] is None else row["Grade"]
            self.listbox.insert(tk.END, ";".join([row["Username"], row["Password"], str(grade)]))

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection: # no item selected
            return
        selected = self.listbox.get(selection)
        userinfo = selected.split(";")
        assert len(userinfo) == 3 and len(userinfo[0]) > 0 and len(userinfo[1]) > 0
        username, password, grade = userinfo
        query = self.users_df[(self.users_df[['Username','Password']].values == [username, password]).all(axis=1)]
        assert not query.empty
        if query["is_admin"][0]:
            tk.messagebox.showwarning('Error', "管理员用户不可删除!")
        else:
            self.users_df = self.users_df[self.users_df.Username != username]
            self.update_users_database()
            self.update_listbox()

    def remove_grade(self):
        selection = self.listbox.curselection()
        if not selection: # no item selected
            return
        selected = self.listbox.get(selection)
        userinfo = selected.split(";")
        assert len(userinfo) == 3 and len(userinfo[0]) > 0 and len(userinfo[1]) > 0
        username, password, grade = userinfo
        self.users_df.loc[self.users_df['Username'] == username, 'Grade'] = None
        self.update_users_database()
        self.update_listbox()

    def go_admin(self):
        from admin_page import AdminPage
        self.window.destroy()
        AdminPage(basedir=self.basedir)
