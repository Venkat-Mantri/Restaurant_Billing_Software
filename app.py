import streamlit as st
import pandas as pd
import sqlite3
import os
import traceback
from datetime import datetime
from pdf_bill import create_pdf_bill
from setup_db import create_or_migrate

st.set_page_config(page_title="Restaurant Billing System", page_icon="🍽️", layout="centered")

# Ensure DB and schema are ready
create_or_migrate()

# Paths
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")
MENU_PATH = os.path.join(BASE_DIR, "menu.csv")
PDF_PATH = os.path.join(BASE_DIR, "bill.pdf")

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login", use_container_width=True)
    if login_btn:
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.success("Logged in successfully")
        else:
            st.error("Invalid credentials")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_page()
    st.stop()

# ---------- LOAD MENU ----------
if not os.path.exists(MENU_PATH):
    st.error("menu.csv not found in project folder. Create menu.csv with columns item_name,price,GST")
    st.stop()

menu = pd.read_csv(MENU_PATH)
required_cols = {"item_name", "price", "GST"}
if not required_cols.issubset(set(menu.columns)):
    st.error(f"menu.csv must contain columns: {required_cols}")
    st.stop()

# ---------- UI ----------
st.title("🍽️ Restaurant Billing System")

# Sidebar clock
st.sidebar.markdown("### ⏱ Current Time")
st.sidebar.info(datetime.now().strftime("%I:%M:%S %p"))

# Order type & table
order_type = st.radio("Select Order Type:", ["Dine-in", "Takeaway"])
table_no = st.selectbox("Select Table Number", list(range(1, 11))) if order_type == "Dine-in" else "N/A"

# Menu selection
st.subheader("📜 Menu")
selected_items = st.multiselect("Choose Items", menu["item_name"].tolist())

# Quantities
quantities = {}
if selected_items:
    st.subheader("🔢 Quantities")
    for item in selected_items:
        quantities[item] = st.number_input(f"Quantity for {item}", min_value=1, value=1, key=f"qty_{item}")

# Payment method
payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

# Single generate button (no duplicates)
generate = st.button("Generate Bill", use_container_width=True)

# ---------- BILL LOGIC ----------
if generate:
    if not selected_items:
        st.warning("Please select at least one item.")
        st.stop()

    # Prepare calculations
    menu_indexed = menu.set_index("item_name")
    try:
        subtotal = sum(menu_indexed.loc[item, "price"] * quantities[item] for item in selected_items)
        gst = sum(menu_indexed.loc[item, "price"] * quantities[item] * menu_indexed.loc[item, "GST"] / 100 for item in selected_items)
        total = subtotal + gst
    except Exception as e:
        st.error("Error calculating totals. Check menu.csv values (price and GST must be numeric).")
        st.text(traceback.format_exc())
        st.stop()

    # Show results
    st.success("🧾 Bill Generated Successfully!")
    st.write("### 🧾 Bill Summary")
    st.write(f"**Order Type:** {order_type}")
    if order_type == "Dine-in":
        st.write(f"**Table No.:** {table_no}")
    st.write(f"**Subtotal:** ₹{subtotal:.2f}")
    st.write(f"**GST:** ₹{gst:.2f}")
    st.write(f"**Total:** ₹{total:.2f}")

    # Insert into DB safely
    order_id = None
    try:
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
    except Exception as e:
        st.error("Failed to save order to database. App will still generate the PDF.")
        st.text(traceback.format_exc())

    # Create PDF (works even if DB insert failed)
    try:
        create_pdf_bill(order_id or "N/A", quantities, subtotal, gst, total, payment_method)
    except Exception as e:
        st.error("Failed to create PDF bill.")
        st.text(traceback.format_exc())
        st.stop()

    # Provide download (ensure file exists)
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button("⬇️ Download Bill PDF", f, file_name=f"Bill_Order_{order_id or 'NA'}.pdf")
    else:
        st.error("PDF file not found after creation.")

# OPTIONAL: simple order history viewer (read-only)
with st.expander("Order History (latest 10)", expanded=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        df_orders = pd.read_sql_query("SELECT id, customer_type, items, subtotal, gst, total, payment_method, timestamp FROM orders ORDER BY id DESC LIMIT 10;", conn)
        conn.close()
        if df_orders.empty:
            st.info("No orders yet.")
        else:
            st.dataframe(df_orders)
    except Exception:
        st.error("Could not load order history.")
