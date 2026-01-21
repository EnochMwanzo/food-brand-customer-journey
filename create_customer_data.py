import sqlite3
import random

con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

for i in range(11):
    cur.execute(
        "INSERT INTO customers (username) VALUES (?)",
        [''.join(random.choices(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], k=6))]
    )
    con.commit()