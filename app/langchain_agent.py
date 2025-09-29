#importing all required libraries
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from app.crud import (
    get_customers, get_customer_by_id, get_customers_by_name,
    add_customer, update_customer, delete_customer,
    get_products, get_product_by_id, get_products_by_name,
    add_product, update_product, delete_product
)
import json
import ast


# Helper to safely parse parameters
def parse_params(params):
    """
    Convert input to dictionary.
    Accepts:
    - Python dict
    - JSON string
    - Stringified dict (with single quotes)
    """
    if isinstance(params, dict):
        return params
    if isinstance(params, str):
        try:
            return json.loads(params)  # normal JSON string
        except json.JSONDecodeError:
            try:
                # convert single-quote dict string to dict safely
                return ast.literal_eval(params)
            except Exception:
                raise ValueError("Invalid string passed to agent; cannot parse as dict.")
    raise ValueError("Unsupported parameter type passed to agent.")

# Define Tools
tools = [
    # Customers - Read operations
    Tool(
        name="Get Customers",
        func=lambda query: str(get_customers(limit=int(query))),
        description="Get top N customers. Input: number of customers."
    ),
    Tool(
        name="Get Customer By ID",
        func=lambda customer_id: str(get_customer_by_id(int(customer_id))),
        description="Retrieve a customer by ID. Input: customer ID."
    ),
    Tool(
        name="Get Customers By Name",
        func=lambda name: str(get_customers_by_name(name)),
        description="Retrieve customers by name. Input: customer name (partial allowed)."
    ),

    # Customers - C/U/D operations (human-in-loop)
    Tool(
        name="Add Customer",
        func=lambda params: add_customer(**parse_params(params)),
        description="Queue a new customer for approval. Input: dict with name, email, city, age, phone, membership."
    ),
    Tool(
        name="Update Customer",
        func=lambda params: update_customer(
            customer_id=parse_params(params)["id"],
            **{k: v for k, v in parse_params(params).items() if k != "id"}
        ),
        description="Queue an update for a customer. Input: dict with id and fields to update."
    ),
    Tool(
        name="Delete Customer",
        func=lambda customer_id: delete_customer(int(customer_id)),
        description="Queue deletion of a customer. Input: customer ID."
    ),

    # Products - Read operations
    Tool(
        name="Get Products",
        func=lambda query: str(get_products(limit=int(query))),
        description="Get top N products. Input: number of products."
    ),
    Tool(
        name="Get Product By ID",
        func=lambda product_id: str(get_product_by_id(int(product_id))),
        description="Retrieve a product by ID. Input: product ID."
    ),
    Tool(
        name="Get Products By Name",
        func=lambda name: str(get_products_by_name(name)),
        description="Retrieve products by name. Input: product name (partial allowed)."
    ),

    # Products - C/U/D operations (human-in-loop)
    Tool(
        name="Add Product",
        func=lambda params: add_product(**parse_params(params)),
        description="Queue a new product for approval. Input: dict with name, price, stock, category, discount."
    ),
    Tool(
        name="Update Product",
        func=lambda params: update_product(
            product_id=parse_params(params)["id"],
            **{k: v for k, v in parse_params(params).items() if k != "id"}
        ),
        description="Queue an update for a product. Input: dict with id and fields to update."
    ),
    Tool(
        name="Delete Product",
        func=lambda product_id: delete_product(int(product_id)),
        description="Queue deletion of a product. Input: product ID."
    ),
]

# Initialize Chat Model
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# Initialize Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Agent Interface
def ask_agent(user_input: str):
    """
    Send natural language input to LangChain agent.
    Handles all CRUD operations for customers and products.
    Returns structured string output.
    """
    return agent.run(user_input)