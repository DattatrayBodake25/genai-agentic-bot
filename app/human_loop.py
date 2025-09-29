from typing import List, Dict

# Store pending C/U/D actions here
pending_actions: List[Dict] = []

def queue_human_confirmation(action_type: str, data: dict) -> Dict:
    """
    Add a CRUD action to the pending queue instead of blocking for input.
    Returns the action dictionary.
    """
    action = {
        "type": action_type,    # for example add_customer, update_product
        "data": data,           # payload of the action
        "status": "pending"     # pending / approved / rejected
    }
    pending_actions.append(action)
    return action

def list_pending_actions() -> List[Dict]:
    """
    Return the list of all pending actions.
    """
    return pending_actions

def approve_action(index: int) -> Dict:
    """
    Approve a pending action and remove it from the queue.
    Returns the approved action.
    """
    if index < 0 or index >= len(pending_actions):
        raise IndexError("Invalid action index")
    action = pending_actions.pop(index)
    action["status"] = "approved"
    return action

def reject_action(index: int) -> Dict:
    """
    Reject a pending action and remove it from the queue.
    Returns the rejected action.
    """
    if index < 0 or index >= len(pending_actions):
        raise IndexError("Invalid action index")
    action = pending_actions.pop(index)
    action["status"] = "rejected"
    return action