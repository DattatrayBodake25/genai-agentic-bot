#importing libraries
from sqlalchemy import text
from app.db_connections import mysql_engine, postgres_engine


def test_mysql():
    try:
        with mysql_engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM customers LIMIT 5"))
            for row in result:
                print("MySQL:", row)
        print("MySQL connection successful!")
    except Exception as e:
        print("MySQL connection failed:", e)


def test_postgres():
    try:
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM products LIMIT 5"))
            for row in result:
                print("PostgreSQL:", row)
        print("PostgreSQL connection successful!")
    except Exception as e:
        print("PostgreSQL connection failed:", e)


if __name__ == "__main__":
    test_mysql()
    test_postgres()