import tkinter as tk
import os
import pickle
import tkinter.messagebox
import pandas as pd

class ExamsPage(object):

    def __init__(self, basedir):
        self.basedir = basedir
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        # Listbox Pack
        self.load_exams_database()
        self.listbox = tk.Listbox()
        self.listbox.pack(pady=10)
        self.update_listbox()

        # Button Pack
        unselect_button = tk.Button(self.window, text='取消选择', width=10, height=2, command=self.unselect)
        unselect_button.pack()

        # Entry Pack
        self.exam_entry = tk.Entry(self.window, show=None, width=20, font=('Arial', 14))
        self.exam_entry.pack(fill=None, pady=5)

        # Add Button
        add_update_button = tk.Button(self.window, text='添加/更新', width=10, height=2, command=self.add_update)
        add_update_button.pack()

        # Modify/Delete Button
        mod_del_button = tk.Button(self.window, text='删除/修改', width=10, height=2, command=self.mol_del)
        mod_del_button.pack()

        # Back Pack
        back_button = tk.Button(self.window, bg="gray", text='返回上一页', width=10, height=2, command=self.go_admin)
        back_button.pack(pady=20)

        # Window Run
        self.window.mainloop()

    def load_exams_database(self):
        if not os.path.exists(os.path.join(self.database_dir, "exams.pickle")):
            self.exams_df = None
        else:
            with open(os.path.join(self.database_dir, "exams.pickle"), 'rb') as exams_data_file:
                self.exams_df = pickle.load(exams_data_file)

    def unselect(self):
        self.exam_entry.delete(0, tk.END)
        self.listbox.selection_clear(0, tk.END)

    def add_update(self):
        exam_info = self.exam_entry.get().split("//")
        if len(exam_info) == 2 and len(exam_info[0]) > 0 and len(exam_info[1]) >= 3:
            options = exam_info[1].split(";")
            if len(options) == 3 and len(options[0]) > 0 and len(options[1]) > 0 and len(options[2]) > 0:
                answer, alter1, alter2 = options
                new_question = exam_info[0]
                if (self.exams_df.Question == new_question).any():
                    tk.messagebox.showwarning('Error', "该题目已存在")
                    return
                new_options = ";".join(options)
                new_dataline = pd.DataFrame(data=[[new_question, new_options]], columns=["Question", "Options"])
                if self.exams_df is None:
                    self.exams_df = new_dataline
                else:
                    self.exams_df = pd.concat([self.exams_df, new_dataline])
                self.update_exams_database()
                self.update_listbox()
                self.exam_entry.delete(0, tk.END)
            else:
                tk.messagebox.showwarning('Error', "请按照'题目//[正确选项; 错误选项1; 错误选项2]'的格式输入")
        else:
            tk.messagebox.showwarning('Error', "请按照'题目//[正确选项; 错误选项1; 错误选项2]'的格式输入")

    def mol_del(self):
        # Some item must be selected in listbox to start changing
        selection = self.listbox.curselection()
        if selection:
            # If some item is selected, delete it from listbox and copy the value to entry box for possible modification
            selected = self.listbox.get(selection)
            self.exam_entry.delete(0, tk.END)
            self.exam_entry.insert(0, selected)
            # Delete it from database
            question, options = selected.split("//")
            assert len(question) > 0
            query = self.exams_df[(self.exams_df[['Question','Options']].values == [question, options]).all(axis=1)]
            assert not query.empty
            self.exams_df = self.exams_df[self.exams_df.Question != question]
            self.update_exams_database()
            self.update_listbox()
        else:
            # If no item selected, simply clear the entry box
            self.exam_entry.delete(0, tk.END)


    def update_exams_database(self):
        with open(os.path.join(self.database_dir, "exams.pickle"), 'wb') as exams_data_file:
            pickle.dump(self.exams_df, exams_data_file)

    def update_listbox(self):
        if self.exams_df is not None:
            self.listbox.delete(0, tk.END)
            for idx, row in self.exams_df.iterrows():
                self.listbox.insert(tk.END, "//".join([row["Question"], row["Options"]]))

    def go_admin(self):
        from admin_page import AdminPage
        self.window.destroy()
        AdminPage(basedir=self.basedir)
