# food-brand-customer-journey
This is similar to my membership group customer journey project, but I wanted to do an ecommerce brand to practce creating emails for different industries. I chose to make up a donuts themed brand and used images from Unsplash.

### What is the goal of the journey
The brand wants customer to purchase donuts, make referrals, and subscribe to receive donuts on a regular basis. In order to chieve this, we can creae a very straightforward flow where the customer:

- signs up to receive emails
- views products on the brand's website
- adds products to cart and makes a purchase
- is updated on their order status and delivery
- leave a positive review
- become loyal and subscribe or refer others

There are stages in this flow where tings could go wrong, like the customer:

- adds product to their cart but doesn't purchase
- leaves a negative review
- cancels subscription

  We can track all of this in a database:

```sql
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
```
### What can the brand do
Then when the customer performs one of these actions, the brand can send a message with a call to action to the next point in the journey. For example if the user leaves a low rating, they will get an emal reminding them they can get a refund, but if they leave a positive rating, they are recommeded other donuts to buy. Some snippets of the backend logic and the email code:

```py
order_id = request.json.get('order_id')
order_data = convert_to_json(cur.execute(
    "SELECT * FROM orders WHERE id = ?", [order_id]
))
cur.execute(
    "UPDATE conversions SET review = 'TRUE' WHERE customer_id = ?", [order_data['customer_id']]
)
con.commit()
...
recommendation1 = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id IS NOT ? ORDER BY RANDOM() LIMIT 1", [order_data['product_id']]
    ))
recommendation2 = convert_to_json(cur.execute(
        "SELECT * FROM products WHERE id IS NOT ? ORDER BY RANDOM() LIMIT 1", [order_data['product_id']]
    ))
```

```html
{% if rating['rating'] >= 3 %}
<p style="margin: 1em 0;">It looks like you really enjoyed {{product['product_name']}}. Here are some other products you may also like:</p>
{% for i in recommendations %}
<figure>
  <img class="has-border" src="{{i['product_image_link']}}" alt="{{i['product_description']}}" style="width: 60%; max-height: 250px; object-fit: fill; display:block; margin: 0 auto; border: 3px solid #451212">
  <figcaption>{{i['product_description']}}</figcaption>
</figure>
<p style="margin: 1em 0;">There are {{i['stock']}} left in stock, so get it for {{i['price']}} when your ready.</p>
{% endfor %}
...
<a class="cta" href="#" style="background-color:#451212; color: moccasin; text-decoration: none; display:inline-block; border-radius:16px; padding: .5em 2em;">
  View Recommended Products
</a>
{% elif rating['rating'] < 3 %}
<p style="margin: 1em 0;">It looks like you didn't enjoy your {{product['product_name']}}. Remember that you can get a <a href="#" style="text-decoration: none; color: darkgreen;">refund</a> if you are unhappy with your purchase.</p>
{% endif %}
```

All the emails are in examples.md and the examples directory.

### metrics

The doughnut brand would want to keep track of number of purchases made, subscribe rate, or segment customers by their lifetime value. These can also be tracked in a database and queried for analysis.

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
...
    number_of_purchases INTEGER DEFAULT 0,
    subscriber BOOLEAN DEFAULT 'FALSE',
    days_since_signup INTEGER DEFAULT 0,
    days_since_subscribing INTEGER DEFAULT 0
);
```

```py
number_of_purchases = convert_to_json(cur.execute(
        "SELECT COUNT(*) as number_of_purchase FROM orders GROUP BY customer_id"
    ))
    cur.execute(
        "INSERT INTO customers (number_of_purchases) VALUES(?)", [number_of_purchases]
    )
    con.commit()
```
