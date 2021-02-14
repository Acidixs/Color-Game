import mysql.connector
import os
from dotenv import load_dotenv
import random

class Database:
    def __init__(self):
        load_dotenv()
        self.mydb = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), password=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))


    def add_score(self, score):
        cursor = self.mydb.cursor()
        conn = self.mydb
        sql= """INSERT INTO stats (score) VALUES (%s)"""
        cursor.execute(sql, (score,))
        conn.commit()
        cursor.close()

    def get_score(self):
        cursor = self.mydb.cursor()
        conn = self.mydb
        sql = """SELECT stats.score FROM stats"""
        cursor.execute(sql)
        info = cursor.fetchall()
        # converts list of tuples to one list by using list comprehension
        l = [item for t in info for item in t]
        print("from db scores", l)
        cursor.close()
        return l

    def get_round(self):
        cursor = self.mydb.cursor()
        conn = self.mydb
        sql = """SELECT stats.round FROM stats"""
        cursor.execute(sql)
        info = cursor.fetchall()
        # converts list of tuples to one list by using list comprehension
        l = [item for t in info for item in t]
        print("from db rounds", l)
        cursor.close()
        return l

