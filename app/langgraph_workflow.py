#importing all required libraries
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
from app.crud import (
    get_customers, get_customer_by_id, get_customers_by_name,
    add_customer, update_customer, delete_customer,
    get_products, get_product_by_id, get_products_by_name,
    add_product, update_product, delete_product
)
import json
import re

class GraphState(TypedDict):
    message: str
    needs_confirmation: bool
    result: Any
    action: Dict[str, Any]

# Helper to detect CRUD commands and extract params
def parse_command(message: str) -> Dict[str, Any]:
    message_lower = message.lower()
    command = {}
    # Simple parsing rules; could be replaced by LLM parsing
    if 'customer' in message_lower:
        command['table'] = 'customer'
    elif 'product' in message_lower:
        command['table'] = 'product'
    else:
        command['table'] = None

    if any(word in message_lower for word in ['add', 'create']):
        command['action_type'] = 'add'
        # Extract params from curly braces {...}
        match = re.search(r'\{(.*)\}', message)
        if match:
            try:
                command['params'] = json.loads(match.group(0).replace("'", '"'))
            except:
                command['params'] = {}
        else:
            command['params'] = {}
    elif any(word in message_lower for word in ['update']):
        command['action_type'] = 'update'
        match = re.search(r'\{(.*)\}', message)
        if match:
            try:
                command['params'] = json.loads(match.group(0).replace("'", '"'))
            except:
                command['params'] = {}
        else:
            command['params'] = {}
    elif any(word in message_lower for word in ['delete', 'remove']):
        command['action_type'] = 'delete'
        match = re.search(r'\{(.*)\}', message)
        if match:
            try:
                command['params'] = json.loads(match.group(0).replace("'", '"'))
            except:
                command['params'] = {}
        else:
            command['params'] = {}
    else:
        command['action_type'] = 'read'
        command['params'] = {}

    return command

def create_advanced_workflow():
    workflow = StateGraph(GraphState)

    # Nodes
    def user_input(state: GraphState):
        return {"message": state.get("message", ""), "needs_confirmation": True, "result": None, "action": {}}

    def llm_processing(state: GraphState):
        message = state.get("message", "")
        action = parse_command(message)
        needs_confirmation = action['action_type'] in ['add', 'update', 'delete']
        return {"message": message, "needs_confirmation": needs_confirmation, "result": None, "action": action}

    def human_confirmation(state: GraphState):
        from app.human_loop import queue_human_confirmation, approve_action
        action = state['action']
        queued = queue_human_confirmation(action['action_type'], action.get('params', {}))
        state['result'] = queued
        # Here you can simulate auto-approval or wait for actual human approval
        # For demo, we approve immediately
        approved = approve_action(0)
        # Execute actual action after approval
        return execute_action({**state, 'action': action})

    def execute_action(state: GraphState):
        action = state['action']
        params = action.get('params', {})
        table = action.get('table')
        action_type = action.get('action_type')

        # Handle customers
        if table == 'customer':
            if action_type == 'read':
                state['result'] = get_customers() if not params else get_customer_by_id(params.get('id', 1))
            elif action_type == 'add':
                from app.crud import add_customer_actual
                add_customer_actual(**params)
                state['result'] = f"Customer {params.get('name')} added successfully!"
            elif action_type == 'update':
                from app.crud import update_customer_actual
                update_customer_actual(params['id'], **{k: v for k, v in params.items() if k != 'id'})
                state['result'] = f"Customer ID {params.get('id')} updated successfully!"
            elif action_type == 'delete':
                from app.crud import delete_customer_actual
                delete_customer_actual(params['id'])
                state['result'] = f"Customer ID {params.get('id')} deleted successfully!"
        # Handle products
        elif table == 'product':
            if action_type == 'read':
                state['result'] = get_products() if not params else get_product_by_id(params.get('id', 1))
            elif action_type == 'add':
                from app.crud import add_product_actual
                add_product_actual(**params)
                state['result'] = f"Product {params.get('name')} added successfully!"
            elif action_type == 'update':
                from app.crud import update_product_actual
                update_product_actual(params['id'], **{k: v for k, v in params.items() if k != 'id'})
                state['result'] = f"Product ID {params.get('id')} updated successfully!"
            elif action_type == 'delete':
                from app.crud import delete_product_actual
                delete_product_actual(params['id'])
                state['result'] = f"Product ID {params.get('id')} deleted successfully!"
        else:
            state['result'] = f"Unrecognized command: {state['message']}"
        return state

    def direct_output(state: GraphState):
        return state

    # Add nodes
    workflow.add_node("user", user_input)
    workflow.add_node("llm", llm_processing)
    workflow.add_node("human", human_confirmation)
    workflow.add_node("execute", execute_action)
    workflow.add_node("output", direct_output)

    # Entry point
    workflow.set_entry_point("user")
    workflow.add_edge("user", "llm")

    # Conditional routing
    def route_after_llm(state: GraphState):
        if state.get("needs_confirmation", False):
            return "human"
        return "execute"

    workflow.add_conditional_edges("llm", route_after_llm, {"human": "human", "execute": "execute"})
    workflow.add_edge("execute", "output")
    workflow.add_edge("output", END)
    workflow.add_edge("human", "output")

    return workflow.compile()

# Usage
if __name__ == "__main__":
    graph = create_advanced_workflow()

    # Read operation
    result = graph.invoke({"message": "Get customer list"})
    print("Read operation result:", result)

    # Write operation
    result = graph.invoke({"message": "Add new customer: {\"name\": \"Sahil Kumar\", \"email\": \"sahilkumar@example.com\", \"city\": \"Kolhapur\", \"age\": 30, \"phone\": 9991239999, \"membership\": \"Silver\"}"})
    print("Write operation result:", result)