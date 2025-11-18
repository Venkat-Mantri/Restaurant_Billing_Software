import streamlit as st
import pandas as pd
import sqlite3
import os
import traceback
from datetime import datetime

# Import helper functions (ensure setup_db.py and pdf_bill.py exist in the same folder)
from setup_db import create_or_migrate
from pdf_bill import create_pdf_bill

# ---------- CONFIG ----------
st.set_page_config(page_title="Restaurant Billing System", page_icon="🍽️", layout="centered")



BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "restaurant.db")
MENU_PATH = os.path.join(BASE_DIR, "menu.csv")
PDF_PATH = os.path.join(BASE_DIR, "bill.pdf")


# Ensure DB/schema exist (idempotent)
create_or_migrate()

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Admin Login")
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

try:
    menu = pd.read_csv(MENU_PATH)
except Exception as e:
    st.error("Failed to read menu.csv. Ensure it's a valid CSV.")
    st.text(traceback.format_exc())
    st.stop()

required_cols = {"item_name", "price", "GST"}
if not required_cols.issubset(set(menu.columns)):
    st.error(f"menu.csv must contain columns: {required_cols}")
    st.stop()

# Ensure numeric types
menu['price'] = pd.to_numeric(menu['price'], errors='coerce')
menu['GST'] = pd.to_numeric(menu['GST'], errors='coerce')
if menu['price'].isnull().any() or menu['GST'].isnull().any():
    st.error("menu.csv contains non-numeric values in price or GST. Fix them.")
    st.stop()

# ---------- UI ----------
st.title("🍽️ Restaurant Billing System")

# Sidebar: live clock and basic info
st.sidebar.markdown("### ⏱ Current Time")
st.sidebar.info(datetime.now().strftime("%I:%M:%S %p"))
st.sidebar.markdown("Admin: `admin` / `1234`")

# Order type & table selection
order_type = st.radio("Select Order Type:", ["Dine-in", "Takeaway"])
table_no = st.selectbox("Select Table Number", list(range(1, 11))) if order_type == "Dine-in" else "N/A"

# Menu selection
st.subheader("📜 Menu")
selected_items = st.multiselect("Choose items", menu["item_name"].tolist())

# Quantities
quantities = {}
if selected_items:
    st.subheader("🔢 Quantities")
    for item in selected_items:
        # unique key per item ensures stable widgets
        quantities[item] = st.number_input(f"Quantity for {item}", min_value=1, value=1, key=f"qty_{item}")

# Payment method
payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

# Single generate button (no duplicates)
generate = st.button("Generate Bill", use_container_width=True)

# ---------- BILL GENERATION LOGIC ----------
if generate:
    if not selected_items:
        st.warning("Please select at least one item first.")
        st.stop()

    menu_indexed = menu.set_index("item_name")

    # Calculate totals
    try:
        subtotal = sum(menu_indexed.loc[item, "price"] * quantities[item] for item in selected_items)
        gst = sum(menu_indexed.loc[item, "price"] * quantities[item] * menu_indexed.loc[item, "GST"] / 100 for item in selected_items)
        total = subtotal + gst
    except Exception:
        st.error("Error calculating totals. Check menu.csv and quantities.")
        st.text(traceback.format_exc())
        st.stop()

    # Display summary
    st.success("🧾 Bill Generated Successfully!")
    st.write("### 🧾 Bill Summary")
    st.write(f"**Order Type:** {order_type}")
    if order_type == "Dine-in":
        st.write(f"**Table No.:** {table_no}")
    st.write(f"**Subtotal:** ₹{subtotal:.2f}")
    st.write(f"**GST:** ₹{gst:.2f}")
    st.write(f"**Total:** ₹{total:.2f}")

    # Save order to DB (safe)
    order_id = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
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
        order_id = cur.lastrowid
        conn.close()
    except Exception:
        st.error("Failed to save order to database. The app will still attempt to generate a PDF.")
        st.text(traceback.format_exc())

    # Create PDF using absolute path inside pdf_bill
    try:
        create_pdf_bill(order_id or "N/A", quantities, subtotal, gst, total, payment_method)
    except Exception:
        st.error("PDF generation failed.")
        st.text(traceback.format_exc())
        st.stop()

    # Provide download if exists
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            st.download_button("⬇️ Download Bill PDF", f, file_name=f"Bill_Order_{order_id or 'NA'}.pdf")
    else:
        st.error("PDF file not found after creation.")






