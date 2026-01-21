import sqlite3

con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

def convert_to_json(result):
    columns = [description[0] for description in result.description]
    for row in result.fetchall():
        result = dict(zip(columns, row))
    return result
order_data = convert_to_json(cur.execute(
        "SELECT * FROM orders WHERE id = ?", [1]
    ))
print(order_data['product_id'])
con.commit()

