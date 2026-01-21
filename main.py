from flask import Flask, request, render_template
import sqlite3

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
con = sqlite3.connect("doughnuts-brand.db", check_same_thread=False)
cur = con.cursor()

def email(template, customer_data):
    customer = customer_data
    sender_email = "TheDoughnutsBrand@example.com"
    receiver_email = customer['username'] + ''.join("@example.com")
    password='abc'
    message = MIMEMultipart("alternative")
    message["Subject"] = "Message from TDB"
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(template, "html")

    message.attach(part)

    with smtplib.SMTP("localhost", 25) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def convert_to_json(result):
    columns = [description[0] for description in result.description]
    for row in result.fetchall():
        result = dict(zip(columns, row))
    return result

@app.route("/signup", methods=["POST"])
def signup():
    customer_id = (request.json.get('customer_id'))
    cur.execute(
        "UPDATE conversions SET signup = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT signup FROM conversions WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    template = render_template("signup.html", customer=customer_data)
    email(template, customer_data)
    return f'{result}\n'

@app.route("/view_product_page", methods=["POST"])
def view_product_page():
    customer_id = request.json.get('customer_id')
    product_id = request.json.get('product_id')
    cur.execute(
        "UPDATE conversions SET view_product_page = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT view_product_page FROM conversions WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [product_id]
    ))
    template = render_template("view-product-page.html", customer=customer_data, product=product_data)
    email(template, customer_data)
    return result


@app.route("/abandoned-cart", methods=["POST"])
def abandoned_cart():
    customer_id = request.json.get('customer_id')
    product_id = request.json.get('product_id')
    cur.execute(
        "UPDATE triggers SET abandon_cart = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT abandon_cart FROM triggers WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [product_id]
    ))
    template = render_template("abandoned-cart.html", customer=customer_data, product=product_data)
    email(template, customer_data)
    return result


@app.route("/make-purchase", methods=["POST"])
def make_purchase():
    customer_id = request.json.get('customer_id')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    cur.execute(
        "UPDATE conversions SET purchase = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [product_id]
    ))
    cur.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, total) VALUES(?, ?, ?, ?)", [customer_id, product_id, quantity, product_data['price']*quantity]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT purchase = 'TRUE' FROM conversions WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    template = render_template("make_purchase.html", customer=customer_data, product=product_data, quantity=quantity)
    email(template, customer_data)
    return result

@app.route("/order-tracking", methods=["POST"])
def order_tracking():
    order_id = request.json.get('order_id')
    cur.execute(
        "UPDATE orders SET progress = 'in transit' WHERE id = ?", [order_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT progress FROM orders WHERE id = ?", [order_id]
    ))
    order_data = convert_to_json(cur.execute(
        "SELECT * FROM orders WHERE id = ?", [order_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [order_data['customer_id']]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [order_data['product_id']]
    ))
    template = render_template("order-tracking.html", customer=customer_data, product=product_data, order=result)
    email(template, customer_data)
    return result

@app.route("/delivered", methods=["POST"])
def delivered():
    order_id = request.json.get('order_id')
    cur.execute(
        "UPDATE orders SET progress = 'delivered' WHERE id = ?", [order_id]
    )
    order_data = convert_to_json(cur.execute(
        "SELECT * FROM orders WHERE id = ?", [order_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [order_data['customer_id']]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [order_data['product_id']]
    ))
    template = render_template("delivered.html", customer=customer_data, product=product_data, order=order_data)
    email(template, customer_data)
    return order_data
   
@app.route("/leave-review", methods=["POST"])
def leave_review():
    order_id = request.json.get('order_id')
    rating = request.json.get('rating')
    review = request.json.get('review')
    review_ids = cur.execute(
        "SELECT order_id FROM reviews"
    ).fetchall()
    if order_id not in review_ids:
        cur.execute(
            "INSERT INTO reviews (order_id, rating, review) VALUES (?,?,?)", [order_id, rating, review]
        )
        con.commit()
    else:
        cur.execute(
            "UPDATE review SET rating = ?, review = ?", [rating, review]
        )
        con.commit()
    return 'OK\n'

@app.route("/review", methods=["POST"])
def review():
    order_id = request.json.get('order_id')
    order_data = convert_to_json(cur.execute(
        "SELECT * FROM orders WHERE id = ?", [order_id]
    ))
    cur.execute(
        "UPDATE conversions SET review = 'TRUE' WHERE customer_id = ?", [order_data['customer_id']]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT review FROM conversions WHERE customer_id = ?", [order_data['customer_id']]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [order_data['customer_id']]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [order_data['product_id']]
    ))
    rating = convert_to_json(cur.execute(
        "SELECT rating FROM reviews WHERE order_id = ?", [order_id]
    ))
    recommendation1 = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id IS NOT ? ORDER BY RANDOM() LIMIT 1", [order_data['product_id']]
    ))
    recommendation2 = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id IS NOT ? ORDER BY RANDOM() LIMIT 1", [order_data['product_id']]
    ))
    recommendations = [recommendation1, recommendation2]
    template = render_template("review.html", customer=customer_data, product=product_data, rating=rating, recommendations=recommendations)
    email(template, customer_data)
    return result

@app.route("/refund", methods=["POST"])
def refund():
    order_id = request.json.get('order_id')
    order_data = convert_to_json(cur.execute(
        "SELECT * FROM orders WHERE id = ?", [order_id]
    ))
    cur.execute(
        "UPDATE triggers SET refund = 'TRUE' WHERE customer_id = ?", [order_data['customer_id']]
    )
    result = convert_to_json(cur.execute(
        "SELECT refund FROM triggers WHERE customer_id = ?", [order_data['customer_id']]
    ))
    con.commit()
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [order_data['customer_id']]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [order_data['product_id']]
    ))
    template = render_template("refund.html", customer=customer_data, product=product_data)
    email(template, customer_data)
    return result
    
@app.route("/subscribe", methods=["POST"])
def subscribe():
    customer_id = request.json.get('customer_id')
    choice1_id = request.json.get('choice1')
    choice2_id = request.json.get('choice2')
    cur.execute(
        "UPDATE conversions SET subscribe = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    cur.execute(
        "UPDATE customers SET subscriber = 'TRUE' WHERE id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT subscriber, subscribe FROM customers JOIN conversions on id=customer_id WHERE id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT username FROM customers WHERE id = ?", [customer_id]
    ))
    product_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [choice1_id]
    ))
    product2_data = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id = ?", [choice2_id]
    ))
    template = render_template("subscribe.html", customer=customer_data, product=product_data, product2=product2_data)
    email(template, customer_data)
    return result

@app.route("/referral", methods=["POST"])
def referral():
    customer_id = request.json.get('customer_id')
    cur.execute(
        "UPDATE conversions SET referral = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT referral FROM conversions WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    template = render_template("referral.html", customer=customer_data)
    email(template, customer_data)
    return result

@app.route("/cancel", methods=["POST"])
def cancel():
    customer_id = request.json.get('customer_id')
    cur.execute(
        "UPDATE triggers SET cancel = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    cur.execute(
        "UPDATE customers SET subscriber = 'FALSE' WHERE id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT cancel, subscriber FROM triggers JOIN customers on customer_id=id WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    template = render_template("cancel.html", customer=customer_data)
    email(template, customer_data)
    return result

@app.route("/renew", methods=["POST"])
def renew():
    customer_id = request.json.get('customer_id')
    cur.execute(
        "UPDATE conversions SET restart_subscription = 'TRUE' WHERE customer_id = ?", [customer_id]
    )
    con.commit()
    cur.execute(
        "UPDATE customers SET subscriber = 'TRUE' WHERE id = ?", [customer_id]
    )
    con.commit()
    result = convert_to_json(cur.execute(
        "SELECT restart_subscription, subscriber FROM conversions JOIN customers ON customer_id=id WHERE customer_id = ?", [customer_id]
    ))
    customer_data = convert_to_json(cur.execute(
        "SELECT * FROM customers WHERE id = ?", [customer_id]
    ))
    template = render_template("renew.html", customer=customer_data)
    email(template, customer_data)
    return result

@app.route("/metrics", methods=["POST"])
def metrics():
    number_of_purchases = convert_to_json(cur.execute(
        "SELECT COUNT(*) as number_of_purchase FROM orders GROUP BY customer_id"
    ))
    cur.execute(
        "INSERT INTO customers (number_of_purchases) VALUES(?)", [number_of_purchases]
    )
    con.commit()

if __name__ == "__main__":
    app.run(debug=True, port='5001')
