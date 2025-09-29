from app.crud import (
    get_customers, add_customer, update_customer, delete_customer,
    get_products, add_product, update_product, delete_product
)

# Test MySQL
print("=== MySQL Customers (Before) ===")
for c in get_customers(5):
    print(c)

# Test Add (will prompt)
add_customer("Test User", "testuser@example.com", "Pune", 29, "9999999999", "Silver")

# Test Update (will prompt)
update_customer(1, name="Alice Updated", city="Mumbai")

# Test Delete (will prompt)
delete_customer(2)

print("=== MySQL Customers (After) ===")
for c in get_customers(5):
    print(c)

# Test PostgreSQL 
print("\n=== PostgreSQL Products (Before) ===")
for p in get_products(5):
    print(p)

# Test Add (will prompt)
add_product("Test Product", 1000, 10, "Category", 0)

# Test Update (will prompt)
update_product(1, price=99999, stock=5)

# Test Delete (will prompt)
delete_product(2)

print("=== PostgreSQL Products (After) ===")
for p in get_products(5):
    print(p)