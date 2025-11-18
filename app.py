import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from pdf_bill import create_pdf_bill

# ---------- LOGIN ----------
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

# ---------- SESSION ----------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
    st.stop()

# ---------- UI ----------
st.title("🍽️ Restaurant Billing System")
menu = pd.read_csv("menu.csv")

# Live Clock
st.sidebar.markdown(f"*Current Time:* {datetime.now().strftime('%I:%M:%S %p')}")

# Order Type
order_type = st.radio("Select Order Type:", ["Dine-in", "Takeaway"])

# Table number if dine-in
if order_type == "Dine-in":
    table_number = st.selectbox("Select Table Number", list(range(1, 11)))
else:
    table_number = "N/A"

# Menu Selection
selected_items = st.multiselect("Choose Items", menu["item_name"].tolist())

item_details = menu[menu["item_name"].isin(selected_items)]
quantities = {}

for item in selected_items:
    quantities[item] = st.number_input(f"Enter quantity for {item}", min_value=1, value=1)

# Payment Method
payment_method = st.selectbox("Select Payment Method", ["Cash", "Card", "UPI"])

# ---------- BILLING ----------
if st.button("Generate Bill") and selected_items:
    subtotal = sum(item_details.set_index("item_name").loc[item, "price"] * qty for item, qty in quantities.items())
    gst = sum(item_details.set_index("item_name").loc[item, "price"] * qty * item_details.set_index("item_name").loc[item, "GST"] / 100 for item, qty in quantities.items())
    total = subtotal + gst

    st.success("🧾 Bill Generated Successfully!")

    st.write("### 🧾 Bill Summary")
    st.write(f"Subtotal: ₹{subtotal:.2f}")
    st.write(f"GST: ₹{gst:.2f}")
    st.write(f"Total: ₹{total:.2f}")

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (customer_type, items, total, gst, discount, payment_method, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_type, str(quantities), total, gst, 0, payment_method, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()

    create_pdf_bill(order_id, quantities, total, gst, payment_method)

    with open("bill.pdf", "rb") as file:
        st.download_button("Download PDF Bill", file, file_name=f"order_{order_id}_bill.pdf")

elif st.button("Generate Bill") and not selected_items:

    st.warning("Please select at least one item to generate a bill.")


