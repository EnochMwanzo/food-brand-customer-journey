import sqlite3

con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

def convert_to_json(result):
    columns = [description[0] for description in result.description]
    for row in result.fetchall():
        result = dict(zip(columns, row))
    return result
r = convert_to_json(cur.execute("SELECT(SELECT COUNT(*) FROM conversions WHERE subscribe = TRUE)* 1.0/(SELECT COUNT(*) FROM conversions) AS conversion_rate"))
print(r)
con.commit()
con.close()

