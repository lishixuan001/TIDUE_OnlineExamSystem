import tkinter as tk
import os
import pickle
import pandas as pd
import datetime
import tkinter.messagebox
import random


class TestPage(object):

    def __init__(self, basedir, username):

        self.basedir = basedir
        self.username = username
        self.database_dir = os.path.join(self.basedir, "database")

        # Window Init
        self.window = tk.Tk()
        self.window.title('在线考试系统')
        self.window.geometry('800x500')

        # Time Property
        self.start = datetime.datetime.now()
        self.limit = datetime.timedelta(0, 1800, 0) # 0 day, x secs

        label_text = tk.Label(self.window, font=('Arial', 24), width=30, text="剩余时间: ")
        label_text.pack()
        self.label_time = tk.Label(self.window, text="")
        self.label_time.pack()
        self.update_time()

        # Questions
        if not os.path.exists(os.path.join(self.database_dir, "exams.pickle")):
            tk.messagebox.showwarning('Error', "No Exams Yet")
        else:
            self.score = 0
            with open(os.path.join(self.database_dir, "exams.pickle"), 'rb') as exams_data_file:
                self.exams_df = pickle.load(exams_data_file)
            self.exams_count = len(self.exams_df.index)
            self.cur_index = 0 # Current Question's Index

            # Choice Pack
            self.question = tk.Label(self.window, font=('Arial', 18), width=30, text="")
            self.question.pack(pady=20)
            self.v = tk.IntVar()
            self.choice1 = tk.Radiobutton(self.window, text='', variable=self.v, value=1)
            self.choice1.pack(pady=5)
            self.choice2 = tk.Radiobutton(self.window, text='', variable=self.v, value=2)
            self.choice2.pack(pady=5)
            self.choice3 = tk.Radiobutton(self.window, text='', variable=self.v, value=3)
            self.choice3.pack(pady=5)

            # Button Pack
            self.button = tk.Button(self.window, bg="gray", text='', width=10, height=2, command=self.update_question)
            self.button.pack(pady=5)

            self.update_question()

        # Window Run   
        self.window.mainloop()

    def update_time(self):
        now = datetime.datetime.now()
        if (now - self.start) >= self.limit:
            self.label_time.configure(text="时间已到!")
            from grade_page import GradePage 
            self.window.destroy()
            GradePage(basedir=self.basedir, username=self.username, grade=self.score)
        else:
            countdown = self.limit - (now - self.start)
            self.label_time.configure(text=str(countdown).split(".")[0])
            self.window.after(1000, self.update_time)

    def update_question(self):

        # Collect Answer
        if self.cur_index != 0:
            if self.v.get() == 0:
                tk.messagebox.showwarning('Error', "请做出答案选择!")
            else:
                question = self.question["text"]
                query = self.exams_df[(self.exams_df[['Question']].values == question).all(axis=1)]
                answer = query["Options"][0].split(";")[0]
                feedback = self.__dict__["choice{}".format(self.v.get())]["text"]
                if feedback == answer:
                    self.score += 1

        # Update Button
        if self.cur_index == self.exams_count - 1:
            self.button.configure(text="提交")
        elif self.cur_index == self.exams_count:
            # Jump To Grade
            from grade_page import GradePage 
            self.window.destroy()
            GradePage(basedir=self.basedir, username=self.username, grade=self.score)
        else:
            self.button.configure(text="下一题")

        # Update Question
        print(self.exams_count)
        print(self.cur_index)

        query = self.exams_df.iloc[self.cur_index]
        question = query["Question"]
        options = query["Options"].split(";")

        # Shuffle Options
        indices = list(range(3))
        random.shuffle(indices)

        self.question.configure(text=question)
        for i in range(3):
            self.__dict__["choice{}".format(i+1)].configure(text=options[indices[i]])
        self.v.set(0)

        # Update Current Index
        self.cur_index += 1


if __name__ == "__main__":
    TestPage("./", "test1")














