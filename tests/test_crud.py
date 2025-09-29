from app.crud import get_customers, get_products

# Test MySQL
print("MySQL Customers:")
for customer in get_customers(5):
    print(customer)

# Test PostgreSQL
print("\nPostgreSQL Products:")
for product in get_products(5):
    print(product)