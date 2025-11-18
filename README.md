🍽️ Restaurant Billing Software

A clean, professional Restaurant Billing System built using Streamlit, SQLite, and Python.
Generates PDF bills, stores order history, calculates GST, and provides a simple login system.

This project is designed to be internship-ready, resume-ready, and demo-ready.

📌 Features
✅ User Interface (Streamlit)

Clean, simple, and responsive UI

Login screen (admin access)

Menu selection

Quantity input

Billing summary

Live time display

✅ Billing System

Subtotal calculation

GST calculation per item

Final amount

Payment method selection

✅ PDF Bill Generation

Professional invoice-style PDF

Item-wise billing table

GST & totals

Supports restaurant logo

Auto-generated order ID

Downloadable immediately

✅ Database (SQLite)

Stores order history

Auto-creates database & tables

Safe SQL inserts

✅ Menu Management

Loads items from menu.csv

Customizable items, GST, prices

📂 Project Structure
Restaurant_Billing_Software/
│
├── app.py
├── setup_db.py
├── pdf_bill.py
├── menu.csv
├── restaurant.db   (auto created)
├── bill.pdf        (auto generated)
├── README.md
└── logo.png        (optional)

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/Venkat-Mantri/Restaurant_Billing_Software.git
cd Restaurant_Billing_Software

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate   # macOS/Linux

3. Install Requirements
pip install streamlit pandas reportlab

4. Setup Database
python setup_db.py


This creates restaurant.db with required tables.

5. Run the Application
streamlit run app.py


Then open the local URL (default: http://localhost:8501
).

🔐 Login Credentials
username: admin
password: 1234

🧾 PDF Bill Format

The generated PDF includes:

Restaurant name & address

Logo (if logo.png exists)

Order ID & timestamp

Item list with:

Item name

Quantity

Price

GST

Total per item

Subtotal, GST, and final total

Payment method

Thank-you footer

📊 menu.csv Format
item_name,price,GST
Tea,20,5
Coffee,30,5
Burger,120,18
Pizza,220,18
French Fries,80,12
Pasta,150,12
Sandwich,100,5
Thums Up,40,18
Water Bottle,20,0
Ice Cream,70,18


You can modify or add new items anytime.

✨ Customization Options

You can easily change:

Restaurant name

Address

Logo

Menu items

GST rules

PDF design

Just edit pdf_bill.py or menu.csv.

🛠️ Tech Stack

Python 3

Streamlit (Frontend UI)

SQLite3 (Database)

ReportLab (PDF generation)

Pandas (Menu handling)
