DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS conversions;
DROP TABLE IF EXISTS triggers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reviews;


CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    number_of_purchases INTEGER DEFAULT 0,
    subscriber BOOLEAN DEFAULT 'FALSE',
    days_since_signup INTEGER DEFAULT 0,
    days_since_subscribing INTEGER DEFAULT 0
);

CREATE TABLE conversions (
    customer_id INTEGER,
    signup BOOLEAN DEFAULT 'FALSE',
    view_product_page BOOLEAN DEFAULT 'FALSE',
    item_in_cart BOOLEAN DEFAULT 'FALSE',
    purchase BOOLEAN DEFAULT 'FALSE',
    review BOOLEAN DEFAULT 'FALSE',
    subscribe BOOLEAN DEFAULT 'FALSE',
    restart_subscription BOOLEAN DEFAULT 'FALSE',
    referral BOOLEAN DEFAULT 'FALSE',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE triggers (
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