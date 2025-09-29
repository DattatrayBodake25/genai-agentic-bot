#importing all required libraries
from sqlalchemy import text
from app.db_connections import mysql_engine, postgres_engine
from app.human_loop import queue_human_confirmation

#MySQL CRUD (customers)
def get_customers(limit=10):
    """Return all customers, limited by count"""
    with mysql_engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM customers LIMIT {limit}"))
        return [dict(row._mapping) for row in result]

def get_customer_by_id(customer_id: int):
    """Retrieve a single customer by ID"""
    with mysql_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM customers WHERE id = :id"), {"id": customer_id})
        row = result.fetchone()
        return dict(row._mapping) if row else None

def get_customers_by_name(name: str):
    """Retrieve customers matching a name"""
    with mysql_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM customers WHERE name LIKE :name"), {"name": f"%{name}%"})
        return [dict(row._mapping) for row in result]

# Actual DB operations
def add_customer_actual(name, email, city, age, phone, membership):
    with mysql_engine.begin() as conn:
        query = text("""
            INSERT INTO customers (name, email, city, age, phone, membership)
            VALUES (:name, :email, :city, :age, :phone, :membership)
        """)
        conn.execute(query, {"name": name, "email": email, "city": city, "age": age, "phone": phone, "membership": membership})

def update_customer_actual(customer_id, **kwargs):
    if not kwargs:
        return
    set_clause = ", ".join([f"{k} = :{k}" for k in kwargs])
    with mysql_engine.begin() as conn:
        query = text(f"UPDATE customers SET {set_clause} WHERE id = :id")
        kwargs["id"] = customer_id
        conn.execute(query, kwargs)

def delete_customer_actual(customer_id):
    with mysql_engine.begin() as conn:
        query = text("DELETE FROM customers WHERE id = :id")
        conn.execute(query, {"id": customer_id})

# Queue operations for human-in-the-loop
def add_customer(name, email, city, age, phone, membership):
    return queue_human_confirmation("add_customer", {
        "name": name, "email": email, "city": city, "age": age, "phone": phone, "membership": membership
    })

def update_customer(customer_id, **kwargs):
    if not kwargs:
        return None
    return queue_human_confirmation("update_customer", {"id": customer_id, **kwargs})

def delete_customer(customer_id):
    return queue_human_confirmation("delete_customer", {"id": customer_id})


#PostgreSQL CRUD (products)
def get_products(limit=10):
    with postgres_engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM products LIMIT {limit}"))
        return [dict(row._mapping) for row in result]

def get_product_by_id(product_id: int):
    with postgres_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products WHERE id = :id"), {"id": product_id})
        row = result.fetchone()
        return dict(row._mapping) if row else None

def get_products_by_name(name: str):
    with postgres_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products WHERE name LIKE :name"), {"name": f"%{name}%"})
        return [dict(row._mapping) for row in result]

# Actual DB operations
def add_product_actual(name, price, stock, category, discount):
    with postgres_engine.begin() as conn:
        query = text("""
            INSERT INTO products (name, price, stock, category, discount)
            VALUES (:name, :price, :stock, :category, :discount)
        """)
        conn.execute(query, {"name": name, "price": price, "stock": stock, "category": category, "discount": discount})

def update_product_actual(product_id, **kwargs):
    if not kwargs:
        return
    set_clause = ", ".join([f"{k} = :{k}" for k in kwargs])
    with postgres_engine.begin() as conn:
        query = text(f"UPDATE products SET {set_clause} WHERE id = :id")
        kwargs["id"] = product_id
        conn.execute(query, kwargs)

def delete_product_actual(product_id):
    with postgres_engine.begin() as conn:
        query = text("DELETE FROM products WHERE id = :id")
        conn.execute(query, {"id": product_id})

# Queue operations for human-in-the-loop
def add_product(name, price, stock, category, discount):
    return queue_human_confirmation("add_product", {
        "name": name, "price": price, "stock": stock, "category": category, "discount": discount
    })

def update_product(product_id, **kwargs):
    if not kwargs:
        return None
    return queue_human_confirmation("update_product", {"id": product_id, **kwargs})

def delete_product(product_id):
    return queue_human_confirmation("delete_product", {"id": product_id})