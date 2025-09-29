#importing all required libraries
import streamlit as st
import requests
import pandas as pd


API_URL = "http://agent_api:8000"

st.set_page_config(page_title="Mini Agentic Bot", page_icon="🤖", layout="wide")
st.title("🤖 Mini Agentic Bot")
st.write("Interact with **Customers (MySQL)**, **Products (PostgreSQL)**, or ask the **Agent** using natural language.")

page = st.sidebar.radio("Navigate", ["📊 Customers", "📦 Products", "🤖 Agent"])


# Customers
if page == "📊 Customers":
    st.header("📊 Customers (MySQL)")
    limit = st.slider("Number of customers to fetch", 1, 20, 5, key="cust_limit")
    if st.button("Fetch Customers", key="fetch_cust"):
        resp = requests.get(f"{API_URL}/customers?limit={limit}&confirmed=true")
        if resp.ok:
            df = pd.DataFrame(resp.json())
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Error fetching customers")


# Products
elif page == "📦 Products":
    st.header("📦 Products (PostgreSQL)")
    limit = st.slider("Number of products to fetch", 1, 20, 5, key="prod_limit")
    if st.button("Fetch Products", key="fetch_prod"):
        resp = requests.get(f"{API_URL}/products?limit={limit}&confirmed=true")
        if resp.ok:
            df = pd.DataFrame(resp.json())
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Error fetching products")


# Agent
elif page == "🤖 Agent":
    st.header("🤖 Chat with the Agent")
    user_input = st.text_area("Enter your command", placeholder="e.g., Show top 10 customers")
    if st.button("Ask Bot", key="ask_bot"):
        if user_input.strip():
            resp = requests.post(f"{API_URL}/ask", json={"question": user_input})
            if resp.ok:
                answer = resp.json()["response"]
                st.text(answer)
            else:
                st.error("Error from agent")


    # Human-in-Loop Pending Actions
    st.subheader("📝 Pending Actions for Approval")
    pending_resp = requests.get(f"{API_URL}/pending_actions")
    if pending_resp.ok:
        actions = pending_resp.json()
        if actions:
            for idx, action in enumerate(actions):
                st.markdown(f"**[{idx}] {action['type']}** - {action['data']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve {idx}", key=f"approve_{idx}"):
                        approve_resp = requests.post(f"{API_URL}/pending_actions/approve/{idx}")
                        if approve_resp.ok:
                            st.success(approve_resp.json()["response"])
                with col2:
                    if st.button(f"Reject {idx}", key=f"reject_{idx}"):
                        reject_resp = requests.post(f"{API_URL}/pending_actions/reject/{idx}")
                        if reject_resp.ok:
                            st.error(reject_resp.json()["response"])
        else:
            st.info("No pending actions.")