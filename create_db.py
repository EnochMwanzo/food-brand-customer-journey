import sqlite3
import random

con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

with open('doughnuts-brand-databse.sql') as f:
        cur.executescript(f.read())