from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv
from main import convert_to_json

load_dotenv()
app = Flask(__name__)
con = supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

cur = con.cursor()

@app.route("/api/v1/customers", methods=["GET", "POST", "PATCH", "DELETE"])
def customers():
    if request.method == "GET":
        if "id" in request.args.get():
            customers = convert_to_json(cur.execute(
                "SELECT * FROM customers WHERE id = ?", [id]
            ))
            return customers
        else:
            customers = convert_to_json(cur.execute(
            "SELECT * FROM customers"
        ))
        return customers
    elif request.method == "POST":
        customer_data = request.json.get()
        cur.execute(
            "INSERT INTO customers (username) VALUES (?)", [customer_data['username']]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM customers WHERE id=(SELECT MAX(id) FROM customers)"
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE customers SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM customers WHERE id=(SELECT MAX(id) FROM customers)"
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM customers WHERE id=?", [request.args('id')]
        )
        # if a customer is delated, their conversions and triggers should also be deleted, because they have customer_id as foreign key.
        # but it may by necessary to keep customer data so that the data and history makes sense. will have to think more about this
        con.commit()
        return 'Deleted'

@app.route("/api/v1/products", methods=["GET", "POST", "PATCH", "DELETE"])
def products():
    if request.method == "GET":
        if "id" in request.args.get():
            products = convert_to_json(cur.execute(
                "SELECT * FROM products WHERE id = ?", [request.args.get("id")]
            ))
            return products
        else:
            products = convert_to_json(cur.execute(
            "SELECT * FROM products"
        ))
        return products
    elif request.method == "POST":
        product_data = request.json.get()
        cur.execute(
            "INSERT INTO products (product_name, product_description, product_image_link, stock, price) VALUES (?)", [product_data['product_name'], product_data['product_description'], product_data['product_image_link'], product_data['stock'], product_data['price']]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM products WHERE id=(SELECT MAX(id) FROM customers)"
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE products SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT ? FROM products WHERE id=?", [response.args('id')]
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM products WHERE id=?", [request.args('id')]
        )
        con.commit()
        return 'Deleted'

@app.route("/api/v1/orders", methods=["GET", "POST", "PATCH", "DELETE"])
def orders():
    if request.method == "GET":
        if "id" in request.args.get():
            orders = convert_to_json(cur.execute(
                "SELECT * FROM orders WHERE id = ?", [request.args.get("id")]
            ))
            return orders
        else:
            orders = convert_to_json(cur.execute(
            "SELECT * FROM orders"
        ))
        return orders
    elif request.method == "POST":
        order_data = request.json.get()
        cur.execute(
            "INSERT INTO orders (customer_id, product_id, quantity, total) VALUES (?,?,?,?)", [order_data['customer_id'], order_data['product_id'], order_data['quantity'], order_data['total']]
        )
        con.commit()
        number_of_orders = convert_to_json(cur.execute(
            "SELECT number_of_orders FROM customers WHERE id = ?", [order_data['customer_id']]
        ))
        if number_of_orders['number_of_orders'] == 0:
            cur.execute(
                "UPDATE customers SET number_of_orders = number_of_orders + 1 WHERE id = ?", [order_data['customer_id']]
            )
        cur.execute(
            "UPDATE customers SET day_since_last_purchase = 0 WHERE id = ?", [order_data['customer_id']]
        )
        result = convert_to_json(cur.execute(
            "SELECT * FROM orders WHERE id=(SELECT MAX(id) FROM orders)"
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE orders SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM orders WHERE id=?", [response.args('id')]
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM orders WHERE id=?", [request.args('id')]
        )
        con.commit()
        return 'Deleted'

@app.route("/api/v1/reviews", methods=["GET", "POST", "PATCH", "DELETE"])
def reviews():
    if request.method == "GET":
        if "order_id" in request.args.get():
            reviews = convert_to_json(cur.execute(
                "SELECT * FROM orders WHERE id = ?", [request.args.get("order_id")]
            ))
            return reviews
        else:
            reviews = convert_to_json(cur.execute(
            "SELECT * FROM orders"
        ))
        return reviews
    elif request.method == "POST":
        review_data = request.json.get()
        cur.execute(
            "INSERT INTO reviews (order_id, rating, review) VALUES (?,?,?)", [review_data['order_id'], review_data['rating'], review_data['review']]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM reviews WHERE id=?", [response.args('order_id')]
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE reviews SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('order_id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM reviews WHERE id=?", [response.args('id')]
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM reviews WHERE id=?", [request.args('id')]
        )
        con.commit()
        return 'Deleted'

@app.route("/api/v1/conversions", methods=["PATCH"])
def conversions():
    cur.execute(
        "UPDATE conversions SET ?=? WHERE customer_id=?", [response.json.get('field'), response.json.get('value'), response.args('customer_id')]
    )
    result = convert_to_json(cur.execute(
        "SELECT * FROM conversions WHERE customer_id = ?", [response.args('customer_id')]
    ))
    return result

@app.route("/api/v1/triggers", methods=["PATCH"])
def triggers():
    cur.execute(
        "UPDATE triggers SET ?=? WHERE customer_id=?", [response.json.get('field'), response.json.get('value'), response.args('customer_id')]
    )
    result = convert_to_json(cur.execute(
        "SELECT * FROM triggers WHERE customer_id = ?", [response.args('customer_id')]
    ))
    return result

@app.route("/api/v1/support-tickets", methods=["GET", "POST","PATCH", "DELETE"])
def support_tickets():
    if request.method == "GET":
        if "ticket_id" in request.args.get():
            support_tickets = convert_to_json(cur.execute(
                "SELECT * FROM support_tickets WHERE id = ?", [request.args.get("order_id")]
            ))
            return support_tickets
        else:
            support_tickets = convert_to_json(cur.execute(
            "SELECT * FROM support_tickets"
        ))
        return support_tickets
    elif request.method == "POST":
        support_ticket_data = request.json.get()
        cur.execute(
            "INSERT INTO support_tickets (customer_id, order_id, subject, body, assigned_employee_id, progress) VALUES (?,?,?,?,?,?)", [support_ticket_data['customer_id'], support_ticket_data['order_id'], support_ticket_data['subject'], support_ticket_data['body'], support_ticket_data['assigned_employee_id'], support_ticket_data['progress']]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM support_tickets WHERE id=?", [response.args('ticket_id')]
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE support_tickets SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('order_id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM support_tickets WHERE id=?", [response.args('id')]
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM support_tickets WHERE id=?", [request.args('id')]
        )
        con.commit()
        return 'Deleted'

@app.route("/api/v1/employees", methods=["GET", "POST","PATCH", "DELETE"])
def employees():
    if request.method == "GET":
        if "employee_id" in request.args.get():
            employees = convert_to_json(cur.execute(
                "SELECT * FROM employees WHERE id = ?", [request.args.get("employee_id")]
            ))
            return employees
        else:
            employees = convert_to_json(cur.execute(
            "SELECT * FROM employees"
        ))
        return employees
    elif request.method == "POST":
        employee_data = request.json.get()
        cur.execute(
            "INSERT INTO employees (username, job_title, department, salary) VALUES (?,?,?,?)", [employee_data['username'], employee_data['job_title'], employee_data['department'], employee_data['salary']]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM support_tickets WHERE id=?", [response.args('ticket_id')]
        ))
        return result
    elif request.method == "PATCH":
        cur.execute(
            "UPDATE employees SET ?=? WHERE id=?", [response.json.get('field'), response.json.get('value'), response.args('order_id')]
        )
        con.commit()
        result = convert_to_json(cur.execute(
            "SELECT * FROM employees WHERE id=?", [response.args('id')]
        ))
        return result
    elif request.method == "DELETE":
        cur.execute(
            "DELETE FROM employees WHERE id=?", [request.args('id')]
        )
        con.commit()
        return 'Deleted'

@app.route("/api/v1/financials", methods=["GET", "POST","PATCH", "DELETE"])
def financials():
    if request.method == "GET":
        if "time_period" in request.args.get():
            financials = convert_to_json(cur.execute(
                "SELECT * FROM employees WHERE id = ?", [request.args.get("employee_id")]
            ))
            return employees
        else:
            employees = convert_to_json(cur.execute(
                "SELECT * FROM employees"
            ))
            return employees
