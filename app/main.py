#importing all required libraries
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from app.crud import (
    get_customers, get_customer_by_id, get_customers_by_name,
    add_customer, update_customer, delete_customer,
    get_products, get_product_by_id, get_products_by_name,
    add_product, update_product, delete_product,
    add_customer_actual, update_customer_actual, delete_customer_actual,
    add_product_actual, update_product_actual, delete_product_actual
)
from app.langchain_agent import ask_agent
from app.human_loop import list_pending_actions, approve_action, reject_action


app = FastAPI(title="Mini Agentic Bot API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Pydantic Models
class Customer(BaseModel):
    name: str
    email: str
    city: str
    age: int
    phone: str
    membership: str

class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    city: Optional[str]
    age: Optional[int]
    phone: Optional[str]
    membership: Optional[str]

class Product(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    discount: float

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category: Optional[str]
    discount: Optional[float]

class AskRequest(BaseModel):
    question: str


# Customer Endpoints
@app.get("/customers")
def read_customers(limit: int = 10, name: Optional[str] = None, customer_id: Optional[int] = None):
    if customer_id:
        return get_customer_by_id(customer_id)
    if name:
        return get_customers_by_name(name)
    return get_customers(limit)

@app.post("/customers")
def create_customer(customer: Customer, confirmed: bool = Query(False)):
    action = add_customer(**customer.dict())
    if confirmed:
        add_customer_actual(**customer.dict())
        return {"response": f"Customer '{customer.name}' added successfully!"}
    return {"response": f"Customer '{customer.name}' queued for confirmation.", "action": action}

@app.put("/customers/{customer_id}")
def modify_customer(customer_id: int, customer: CustomerUpdate, confirmed: bool = Query(False)):
    data = customer.dict(exclude_unset=True)
    action = update_customer(customer_id, **data)
    if confirmed:
        update_customer_actual(customer_id, **data)
        return {"response": f"Customer ID {customer_id} updated successfully!"}
    return {"response": f"Update for Customer ID {customer_id} queued for confirmation.", "action": action}

@app.delete("/customers/{customer_id}")
def remove_customer(customer_id: int, confirmed: bool = Query(False)):
    action = delete_customer(customer_id)
    if confirmed:
        delete_customer_actual(customer_id)
        return {"response": f"Customer ID {customer_id} deleted successfully!"}
    return {"response": f"Delete for Customer ID {customer_id} queued for confirmation.", "action": action}


# Product Endpoints 
@app.get("/products")
def read_products(limit: int = 10, name: Optional[str] = None, product_id: Optional[int] = None):
    if product_id:
        return get_product_by_id(product_id)
    if name:
        return get_products_by_name(name)
    return get_products(limit)

@app.post("/products")
def create_product(product: Product, confirmed: bool = Query(False)):
    action = add_product(**product.dict())
    if confirmed:
        add_product_actual(**product.dict())
        return {"response": f"Product '{product.name}' added successfully!"}
    return {"response": f"Product '{product.name}' queued for confirmation.", "action": action}

@app.put("/products/{product_id}")
def modify_product(product_id: int, product: ProductUpdate, confirmed: bool = Query(False)):
    data = product.dict(exclude_unset=True)
    action = update_product(product_id, **data)
    if confirmed:
        update_product_actual(product_id, **data)
        return {"response": f"Product ID {product_id} updated successfully!"}
    return {"response": f"Update for Product ID {product_id} queued for confirmation.", "action": action}

@app.delete("/products/{product_id}")
def remove_product(product_id: int, confirmed: bool = Query(False)):
    action = delete_product(product_id)
    if confirmed:
        delete_product_actual(product_id)
        return {"response": f"Product ID {product_id} deleted successfully!"}
    return {"response": f"Delete for Product ID {product_id} queued for confirmation.", "action": action}


# Agent Endpoint
@app.post("/ask")
def ask_bot(request: AskRequest):
    try:
        result = ask_agent(request.question)
        if isinstance(result, dict) and "action_type" in result:
            response_text = f"Action queued: {result['action_type']} for verification."
        elif isinstance(result, list):
            response_text = "\n".join([str(r) for r in result])
        else:
            response_text = str(result)
        return {"response": response_text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


# Pending Actions Endpoints
@app.get("/pending_actions")
def get_pending_actions():
    """List all pending actions."""
    return list_pending_actions()

@app.post("/pending_actions/approve/{index}")
def approve_pending_action(index: int):
    """Approve a pending action by index."""
    try:
        action = approve_action(index)
        # Execute the action immediately
        from app.crud import (
            add_customer_actual, update_customer_actual, delete_customer_actual,
            add_product_actual, update_product_actual, delete_product_actual
        )
        data = action["data"]
        if action["type"] == "add_customer":
            add_customer_actual(**data)
        elif action["type"] == "update_customer":
            update_customer_actual(data["id"], **{k:v for k,v in data.items() if k!="id"})
        elif action["type"] == "delete_customer":
            delete_customer_actual(data["id"])
        elif action["type"] == "add_product":
            add_product_actual(**data)
        elif action["type"] == "update_product":
            update_product_actual(data["id"], **{k:v for k,v in data.items() if k!="id"})
        elif action["type"] == "delete_product":
            delete_product_actual(data["id"])
        return {"response": f"Action '{action['type']}' approved and executed.", "action": action}
    except IndexError:
        return {"response": f"Invalid action index: {index}"}

@app.post("/pending_actions/reject/{index}")
def reject_pending_action(index: int):
    """Reject a pending action by index."""
    try:
        action = reject_action(index)
        return {"response": f"Action '{action['type']}' rejected.", "action": action}
    except IndexError:
        return {"response": f"Invalid action index: {index}"}