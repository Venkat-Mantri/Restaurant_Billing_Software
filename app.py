import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
from pdf_bill import create_pdf_bill

st.set_page_config(page_title="Restaurant Billing System", page_icon="🍽️", layout="centered")

# ---------- DATABASE PATH ----------
DB_PATH = os.path.join(os.path.dirname(__file__), "restaurant.db")

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_btn = st.button("Login", use_container_width=True)

    if login_btn:
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# ---------- SESSION CHECK ----------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_page()
    st.stop()

# ---------- MAIN UI ----------
st.title("🍽️ Restaurant Billing System")

# Load Menu
menu = pd.read_csv("menu.csv")

# Sidebar clock
st.sidebar.markdown("### ⏱ Live Time")
st.sidebar.info(datetime.now().strftime("%I:%M:%S %p"))

# Order Type
order_type = st.radio("Select Order Type:", ["Dine-in", "Takeaway"])

if order_type == "Dine-in":
    table_no = st.selectbox("Select Table Number", list(range(1, 11)))
else:
    table_no = "N/A"

# Menu Items
st.subheader("📜 Menu Selection")
selected_items = st.multiselect("Choose your items", menu["item_name"].tolist())

# Quantities
quantities = {}
if selected_items:
    st.subheader("🍽️ Item Quantities")
    for item in selected_items:
        quantities[item] = st.number_input(f"Quantity for {item}", min_value=1, value=1)

# Payment Method
payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

# ---------- MAIN ACTION BUTTON ----------
generate = st.button("Generate Bill", use_container_width=True)

# ---------- BILL GENERATION ----------
if generate:
    if not selected_items:
        st.warning("Please select at least one item.")
        st.stop()

    # Billing calculations
    selected_df = menu[menu["item_name"].isin(selected_items)]
    selected_df = selected_df.set_index("item_name")

    subtotal = sum(selected_df.loc[item, "price"] * quantities[item] for item in selected_items)
    gst = sum(
        selected_df.loc[item, "price"] * quantities[item] * selected_df.loc[item, "GST"] / 100
        for item in selected_items
    )
    total = subtotal + gst

    st.success("Bill Generated Successfully!")
    st.write("### 🧾 Bill Summary")
    st.write(f"**Subtotal:** ₹{subtotal:.2f}")
    st.write(f"**GST:** ₹{gst:.2f}")
    st.write(f"**Total Amount:** ₹{total:.2f}")

    # ---------- DB INSERT ----------
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (customer_type, items, subtotal, gst, total, payment_method, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order_type,
        str(quantities),
        subtotal,
        gst,
        total,
        payment_method,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    order_id = cursor.lastrowid
    conn.close()

    # ---------- PDF GENERATION ----------
    create_pdf_bill(order_id, quantities, subtotal, gst, total, payment_method)

    with open("bill.pdf", "rb") as file:
        st.download_button("⬇️ Download Bill PDF", file, file_name=f"Bill_Order_{order_id}.pdf")
