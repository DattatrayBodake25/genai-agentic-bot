from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus  # NEW

# Load .env file
load_dotenv()

# Encode passwords safely
mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD"))
postgres_password = quote_plus(os.getenv("POSTGRES_PASSWORD"))

# MySQL connection
mysql_engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{mysql_password}"
    f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

# PostgreSQL connection
postgres_engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{postgres_password}"
    f"@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
)

# Metadata objects
mysql_meta = MetaData()
postgres_meta = MetaData()














# #importing all required libraries
# from sqlalchemy import create_engine, MetaData
# from dotenv import load_dotenv
# import os

# # Load .env file
# load_dotenv()

# # MySQL connection
# mysql_engine = create_engine(
#     f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
#     f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
# )

# # PostgreSQL connection
# postgres_engine = create_engine(
#     f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
#     f"@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
# )

# # Metadata objects
# mysql_meta = MetaData()
# postgres_meta = MetaData()