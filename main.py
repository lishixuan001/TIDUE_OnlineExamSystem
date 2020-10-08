#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tkinter as tk
import os
import pandas as pd
import pickle


"""
Main Program
"""

class Main(object):

    def __init__(self):
        self.basedir = os.getcwd()
        self.database_dir = os.path.join(self.basedir, "database")
        if os.path.exists(self.database_dir):
            if len(sys.argv) > 1 and "clean" in sys.argv[1]:
                import shutil
                shutil.rmtree(self.database_dir)
                self.init_users_database()
        else:
            self.init_users_database()
        self.go_login()

    def init_users_database(self):
        os.makedirs(self.database_dir)
        with open(os.path.join(self.database_dir, "users.pickle"), 'wb') as users_data_file:
            users_df = pd.DataFrame(data=[["admin", "admin", True, None]], columns=["Username", "Password", "is_admin", "Grade"])
            pickle.dump(users_df, users_data_file)

    def go_login(self):
        from login_page import LoginPage
        LoginPage(basedir=self.basedir)


if __name__ == "__main__":
    Main()



# Init TKInter Window

# The index page is the user login page

# If it's admin user, then jump to admin user page

# If it's student user, then jump to student user page
