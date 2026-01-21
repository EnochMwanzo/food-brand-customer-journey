import pandas as pd
import sqlite3

con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

pd.read_sql(
    "SELECT * FROM customers", con
).to_csv('./tables/customers.csv')
pd.read_sql(
    "SELECT * FROM products", con
).to_csv('./tables/products.csv')
pd.read_sql(
    "SELECT * FROM conversions", con
).to_csv('./tables/conversions.csv')
pd.read_sql(
    "SELECT * FROM triggers", con
).to_csv('./tables/triggers.csv')
pd.read_sql(
    "SELECT * FROM orders", con
).to_csv('./tables/orders.csv')
pd.read_sql(
    "SELECT * FROM reviews", con
).to_csv('./tables/reviews.csv')