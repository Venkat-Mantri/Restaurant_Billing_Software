# Restaurant_Billing_Software
 README.md

A complete Restaurant Billing System built with *Python, **Streamlit, **SQLite, and **ReportLab*. Supports Dine-in and Takeaway orders, GST calculations, PDF bill generation, and admin login.

---

##  Features

-  Admin Login
-  Dine-in / Takeaway Option
-  Menu with Price + GST (loaded from CSV)
-  Auto PDF Bill Generation
-  Payment Method Selection (Cash/Card/UPI)
-  Live Clock in Sidebar
-  Order History saved in SQLite database

---

##  Folder Structure

restaurant_billing/ ├── app.py                     # Main Streamlit application ├── db/ │   ├── setup_db.py           # Script to initialize the database │   └── restaurant.db         # SQLite database file (created after first run) ├── data/ │   ├── menu.csv              # Menu data (item, category, price, GST) │   └── bill.pdf              # Generated bill saved as PDF ├── utils/ │   └── pdf_bill.py           # PDF bill generator using reportlab

---

##  Getting Started

### 1️⃣ Clone the Project
```bash
git clone https://github.com/your-username/restaurant_billing.git
cd restaurant_billing

2️⃣ Install Dependencies

pip install streamlit pandas reportlab

3️⃣ Initialize the Database

python db/setup_db.py

4️⃣ Run the Application

streamlit run app.py


---

# Login Credentials

Role	Username	Password

Admin	admin	1234



---

# Sample Menu (data/menu.csv)

item_name,category,price,GST
Idli,Breakfast,30,5
Dosa,Breakfast,50,5
Pulao,Lunch,100,12
Paneer Curry,Lunch,150,12
Ice Cream,Dessert,60,18


---

# Order Entry Example

1. Select order type: Dine-in or Takeaway


2. For Dine-in, select a table number


3. Choose food items and quantities


4. Select payment method


5. Click Generate Bill


6. Download PDF bill and record gets saved to database




---

# Technologies Used

Python

Streamlit

Pandas

SQLite

ReportLab (for PDF)

