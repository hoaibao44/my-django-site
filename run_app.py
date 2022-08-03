from django.core.management import execute_from_command_line

import os
import django
import sqlite3
import pandas as pd


def runInteractive():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_learning.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()
    # from django.contrib.auth.models import User


def run_server():
    execute_from_command_line(['runserver'])


class sqlData():
    def __init__(self, sqlFileName):
        self.sqlFileName = sqlFileName
        self.database = self.databaseConnect()

    def getAlltable_List(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cursor.fetchall()

    def databaseConnect(self):
        con = sqlite3.connect(self.sqlFileName)
        return con

    def sql2df(self, tableName):
        df = pd.read_sql_query(
            "SELECT * FROM {}".format(tableName), self.database)
        return df

    def createTable(self, tableName):

        cur = self.database.cursor()

        cur.execute(
            'CREATE TABLE {}(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)'.format(tableName))
        self.database.commit()

    def addData2Table(self, tableName, dataList):
        # dataList = [['name','],[],[]]
        pass

    def closeDatabase(self):
        self.database.close()


if __name__ == '__main__':
    runInteractive()
