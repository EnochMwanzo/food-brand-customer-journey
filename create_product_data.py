import sqlite3
import random


con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

products = [
    ['Plain Doughnuts', 'Doughnuts with nothing added to them', 'https://unsplash.com/photos/FmMlzpBbJcg/download?ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY4NzUzMTYwfA&force=true&w=640'],
    ['Chocolate Doughnuts', 'Doughnuts with chocolate icing and sprinkles','https://unsplash.com/photos/X1Xe7tYCaZc/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjZ8fGRvdWdobnV0fGVufDB8Mnx8fDE3Njg2MDQzNTR8MA&force=true&w=640'],
    ['Vaiety', 'A diverse set of doughnuts', 'https://unsplash.com/photos/9pf74eJrb74/download?force=true&w=640'],
    ['Strawberry Doughnuts', 'Doughnuts wth strawberry icing', 'https://unsplash.com/photos/PFzy4N0_R3M/download?force=true&w=640'],
    ['Glazed Doughnuts', 'Doughnuts coated in a sugary glaze', 'https://unsplash.com/photos/NH2S3zVPMaE/download?force=true&w=640']
]

for i in range(5):
    cur.execute(
        "INSERT INTO products (product_name, product_description, product_image_link, stock, price) VALUES (?,?,?,?,?)", [products[i][0] , products[i][1], products[i][2],random.randint(0,10), random.randint(15,29)+0.99]
    )
    con.commit()

