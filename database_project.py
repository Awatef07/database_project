import sqlite3
from datetime import datetime
import random


conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
)
""")

conn.commit()



# ---
 products = [
    ("T-Shirt", "Clothing", 25.5),
    ("Jeans", "Clothing", 50.0),
    ("Sneakers", "Footwear", 80.0),
    ("Jacket", "Clothing", 120.0),
    ("Watch", "Accessories", 200.0)
]

cur.executemany("INSERT INTO Products (name, category, price) VALUES (?, ?, ?)", products)

 customers = [
    ("Awatif", "awatif@example.com", "0501234567"),
    ("Ali", "ali@example.com", "0507654321"),
    ("Sara", "sara@example.com", "0509876543"),
    ("Khalid", "khalid@example.com", "0501122334"),
    ("Laila", "laila@example.com", "0504433221")
]

cur.executemany("INSERT INTO Customers (name, email, phone) VALUES (?, ?, ?)", customers)

# إدخال طلبات عشوائية
order_dates = ["2025-11-20", "2025-11-21", "2025-11-22", "2025-11-23", "2025-11-24"]
for _ in range(15):
    customer_id = random.randint(1, len(customers))
    product_id = random.randint(1, len(products))
    quantity = random.randint(1, 5)
    order_date = random.choice(order_dates)
    cur.execute("INSERT INTO Orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
                (customer_id, product_id, quantity, order_date))

conn.commit()


# استعلامات 
print("=== All Orders ===")
cur.execute("""
SELECT o.order_id, c.name AS customer, p.name AS product, o.quantity, o.order_date
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Products p ON o.product_id = p.product_id
""")
for row in cur.fetchall():
    print(row)

print("\n=== Total Quantity Sold per Product ===")
cur.execute("""
SELECT p.name, SUM(o.quantity) AS total_sold
FROM Orders o
JOIN Products p ON o.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold DESC
""")
for row in cur.fetchall():
    print(row)

print("\n=== Total Spending per Customer ===")
cur.execute("""
SELECT c.name, SUM(o.quantity * p.price) AS total_spent
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Products p ON o.product_id = p.product_id
GROUP BY c.name
ORDER BY total_spent DESC
""")
for row in cur.fetchall():
    print(row)

conn.close()
