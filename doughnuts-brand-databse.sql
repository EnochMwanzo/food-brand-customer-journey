DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS customer_conversions;
DROP TABLE IF EXISTS customer_triggers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS employee_conversions;
DROP TABLE IF EXISTS employee_triggers;
DROP TABLE IF EXISTS financials;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS creator_conversions;
DROP TABLE IF EXISTS creator_triggers;



CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    number_of_purchases INTEGER DEFAULT 0,
    subscriber BOOLEAN DEFAULT 'FALSE',
    creator BOOLEAN DEFAULT 'FALSE',
    cohort TEXT DEFAULT 'engaged prospect'
        CHECK(cohort IN('engaged prospect', 'lapsed prospect' 'one purchase', 'two purchases', 'VIP', 'churned' ) DEFAULT 'engaged prospect'
    days_since_signup INTEGER DEFAULT 0,
    days_since_subscribing INTEGER DEFAULT 0,
    days_since_last_purchase INTEGER DEFAULT 0
);

CREATE TABLE customer_conversions (
    customer_id INTEGER,
    signup BOOLEAN DEFAULT 'FALSE',
    view_product_page BOOLEAN DEFAULT 'FALSE',
    item_in_cart BOOLEAN DEFAULT 'FALSE',
    purchase BOOLEAN DEFAULT 'FALSE',
    review BOOLEAN DEFAULT 'FALSE',
    subscribe BOOLEAN DEFAULT 'FALSE',
    restart_subscription BOOLEAN DEFAULT 'FALSE',
    referral BOOLEAN DEFAULT 'FALSE',
    post_on_social_media BOOLEAN DEFAULT 'FALSE',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE customer_triggers (
    customer_id INTEGER,
    abandon_cart BOOLEAN DEFAULT 'FALSE',
    refund BOOLEAN DEFAULT 'FALSE',
    cancel BOOLEAN DEFAULT 'FALSE',
    FOREIGN KEY (customer_id) REFERENCES customers(id)

);

CREATE TABLE reviews (
    order_id INTEGER,
    rating INTEGER,
    review TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_description TEXT,
    product_image_link TEXT,
    stock INTEGER DEFAULT 0,
    price FLOAT DEFAULT 1.00
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    total FLOAT,
    progress TEXT DEFAULT 'received',
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE creators (
    id INTEGER PRIMARY KEY,
    creator_name TEXT,
    link TEXT
);

CREATE TABLE creator_conversions (
    creator_id INTEGER PRIMARY KEY,
    receives_product BOOLEAN,
    FOREIGN KEY (creator_id) REFERENCES creators(id)
);

CREATE TABLE creator_triggers (
    creator_id INTEGER PRIMARY KEY,
    lapsed BOOLEAN DEFAULT "FALSE",
    FOREIGN KEY (creator_id) REFERENCES creators(id)
);

CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_id INTEGER,
    subject TEXT,
    body TEXT,
    assigned_employee_id INTEGER,
    progress TEXT
        CHECK (progress IN ('not started', 'in progress', 'done')),
    days_until_close INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    username TEXT,
    job_title TEXT,
    department TEXT,
    days_since_starting INTEGER DEFAULT 0,
    phone INTEGER,
    company_email TEXT,
    salary FLOAT
);

CREATE TABLE employee_conversions (
    employee_id INTEGER PRIMARY KEY,
    onboarded BOOLEAN DEFAULT "FALSE",
    finished_training BOOLEAN DEFAULT "FALSE",
    promoted DEFAULT "FALSE",
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE employee_triggers (
    employee_id INTEGER PRIMARY KEY,
    violation_count
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

/*
financials

for a post rewuest, like a transaction being added, it should be routed to one of these tables
for get, should it be like "get all income/expenses + join together tables"? or should all these tables just be joined?
*/
CREATE TABLE cash_flow_statements (
    time_period TEXT,
    operating_cash_flow FLOAT,
    total_sales FLOAT,
    cash_spent_on_assets FLOAT,
    operating_expenses FLOAT
);

CREATE TABLE income_statements (
    time_period TEXT,
    total_sales FLOAT,
    cost_of_goods_sold FLOAT,
    profit FLOAT,
    promotion_expenses FLOAT,
    selling_general_administratice_expenses FLOAT,
    depreciation_and_amoritization FLOAT
);

CREATE TABLE balance_sheets (
    time_period TEXT,
    cash FLOAT,
    accounts_receivable FLOAT,
    prepaid_expenses FLOAT,
    inventory FLOAT,
    property_and_equipment FLOAT,
    goodwill FLOAT,
    accounts_payable FLOAT,
    accrued_expenses FLOAT,
    unearned_revenue FLOAT,
    long_term_debt FLOAT
);
