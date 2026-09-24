import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Chouhan Autos & Station Management",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TECHBRIDGE / LIGHT ORANGE WARM THEME (CUSTOM CSS)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary-orange: #ff5722;
        --primary-orange-hover: #f4511e;
        --text-dark: #1e1e24;
        --text-muted: #555555;
        --bg-gradient-start: #ffffff;
        --bg-gradient-end: #ffebee;
        --card-bg: #ffffff;
        --border-color: #ffd2cc;
    }

    html, body, .stApp {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%) !important;
        color: var(--text-dark) !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh;
    }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Deploy button chupane ke liye */
    .stAppDeployButton {
        display: none !important;
    }

    .block-container { padding-top: 1.5rem !important; }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
    }

    hr { border-color: var(--border-color) !important; }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div {
        color: var(--text-dark) !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex !important;
        align-items: center;
        width: 100%;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        border-radius: 10px !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
        cursor: pointer;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background-color: var(--primary-orange) !important;
        border-color: var(--primary-orange) !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span,
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* LABELS */
    label, .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stDateInput label, .stRadio label {
        color: var(--primary-orange) !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }

    /* INPUT FIELDS */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] input, 
    div[data-baseweb="base-input"] input,
    input.st-ae, input[type="text"], input[type="number"] {
        background-color: #ffffff !important;
        color: var(--text-dark) !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* SELECTBOX */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-dark) !important;
    }

    div[data-baseweb="select"] span {
        color: var(--text-dark) !important;
    }

    /* BUTTONS */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: var(--text-dark) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.1rem !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--primary-orange) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.3rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
    }

    div[data-testid="stNumberInput"] button {
        background-color: #ffebee !important;
        border: 1px solid var(--border-color) !important;
        color: var(--primary-orange) !important;
        border-radius: 6px !important;
    }

    /* DOWNLOAD BUTTON HOVER FIX */
    .stDownloadButton > button {
        background-color: #ffffff !important;
        color: var(--text-dark) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stDownloadButton > button:hover {
        background-color: #fff5f3 !important;
        border-color: var(--primary-orange) !important;
        color: var(--primary-orange) !important;
    }

    .stDownloadButton > button:hover svg {
        fill: var(--primary-orange) !important;
        color: var(--primary-orange) !important;
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-left: 4px solid var(--primary-orange) !important;
        padding: 16px 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 13px !important;
        text-transform: uppercase;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-dark) !important;
    }

    .station-banner {
        background: #ffffff;
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 22px 20px 18px 20px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.05);
    }
    .station-banner h1 {
        margin: 0 0 4px 0 !important;
        color: var(--primary-orange) !important;
        font-size: 2rem !important;
    }
    .station-banner p {
        margin: 0 !important;
        color: var(--text-muted) !important;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE SETUP
# ============================================================
def init_db():
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fuel_sales_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT,
            shift TEXT,
            operator_name TEXT,
            nozzle_name TEXT,
            starting_reading REAL,
            ending_reading REAL,
            qty_sold REAL,
            rate REAL,
            total_amount REAL,
            cash_received REAL,
            online_received REAL,
            credit_amount REAL,
            expenses REAL,
            net_cash REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tank_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tank_capacity REAL,
            current_stock REAL,
            warning_limit REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS station_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT
        )
    ''')

    c.execute("SELECT COUNT(*) FROM tank_stock")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO tank_stock (tank_capacity, current_stock, warning_limit) VALUES (10000.0, 7500.0, 2000.0)")

    c.execute("SELECT COUNT(*) FROM station_config")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO station_config (station_name) VALUES ('CHOUHAN AUTOS & STATION')")

    conn.commit()
    conn.close()

init_db()

# ============================================================
# HELPER FUNCTIONS (Updated with Date Range Support)
# ============================================================
def save_entry(date_str, shift, operator, nozzle, start, end, qty, rate, total, cash, online, credit, exp, net):
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO fuel_sales_v2
        (entry_date, shift, operator_name, nozzle_name, starting_reading, ending_reading, qty_sold, rate, total_amount, cash_received, online_received, credit_amount, expenses, net_cash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date_str, shift, operator, nozzle, start, end, qty, rate, total, cash, online, credit, exp, net))

    c.execute("UPDATE tank_stock SET current_stock = current_stock - ? WHERE id = 1", (qty,))
    conn.commit()
    conn.close()

def delete_entry(record_id):
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute("DELETE FROM fuel_sales_v2 WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def get_tank_stock():
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute("SELECT tank_capacity, current_stock, warning_limit FROM tank_stock WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row if row else (10000.0, 7500.0, 2000.0)

def update_tank_stock(capacity, current, warning):
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute("UPDATE tank_stock SET tank_capacity = ?, current_stock = ?, warning_limit = ? WHERE id = 1", (capacity, current, warning))
    conn.commit()
    conn.close()

def get_station_name():
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute("SELECT station_name FROM station_config WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else "CHOUHAN AUTOS & STATION"

def update_station_name(new_name):
    conn = sqlite3.connect("sales_database.db")
    c = conn.cursor()
    c.execute("UPDATE station_config SET station_name = ? WHERE id = 1", (new_name,))
    conn.commit()
    conn.close()

def load_data(start_date=None, end_date=None):
    conn = sqlite3.connect("sales_database.db")
    query = '''
        SELECT
            id AS 'ID',
            entry_date AS 'Date',
            shift AS 'Shift',
            operator_name AS 'Operator',
            nozzle_name AS 'Nozzle',
            starting_reading AS 'Start Read',
            ending_reading AS 'End Read',
            qty_sold AS 'Qty Sold',
            rate AS 'Rate',
            total_amount AS 'Total Sale',
            cash_received AS 'Cash',
            online_received AS 'Online',
            credit_amount AS 'Udhaar',
            expenses AS 'Expenses',
            net_cash AS 'Net Cash'
        FROM fuel_sales_v2
    '''
    if start_date and end_date:
        query += f" WHERE entry_date BETWEEN '{start_date}' AND '{end_date}'"

    query += " ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def safe_calculate(expression: str):
    cleaned = expression.strip()
    if not cleaned:
        raise ValueError("Expression khaali hai.")
    if not re.fullmatch(r"[0-9\.\+\-\\/\%\(\)\s]", cleaned):
        raise ValueError("Sirf numbers aur + - * / % ( ) allowed hain.")
    return eval(cleaned, {"_builtins_": {}}, {})

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🔐 Portal Access")
user_mode = st.sidebar.radio("Select System Role:", ["Operator Mode (Staff)", "Admin Mode (Owner)"])

is_admin = False
if user_mode == "Admin Mode (Owner)":
    admin_pass = st.sidebar.text_input("Enter Admin Password:", type="password")
    if admin_pass == "admin123":
        is_admin = True
        st.sidebar.success("🔑 Admin Panel Unlocked!")
    elif admin_pass:
        st.sidebar.warning("🔒 Incorrect password.")
    else:
        st.sidebar.info("🔒 Enter password for Owner tools.")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Main Navigation")
calc_type = st.sidebar.radio(
    "Go To Module:",
    [
        "⛽ Daily Shift & Nozzle Entry",
        "🧾 Shift Receipt & Print Slip",
        "🛢️ Tank Stock Inventory",
        "📊 Sales Visual Analytics",
        "📦 Profit & Margin Calculator",
        "🏷️ Discount Calculator",
        "🔢 Smart Math Calculator"
    ],
    label_visibility="collapsed"
)

current_station_name = get_station_name()

if is_admin:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Branding Settings")
    custom_name = st.sidebar.text_input("Edit Station Name:", value=current_station_name)
    if st.sidebar.button("💾 Update Station Title"):
        update_station_name(custom_name)
        st.sidebar.success("Name updated successfully!")
        st.rerun()

# ============================================================
# MAIN CONTENT HEADER
# ============================================================
st.markdown(f"""
<div class="station-banner">
    <h1>⛽ {current_station_name.upper()}</h1>
    <p>Professional Shift Management & Smart Analytics Portal</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MODULES ROUTING
# ============================================================
if calc_type == "⛽ Daily Shift & Nozzle Entry":
    st.header("📝 Daily Shift & Meter Reading Logger")
    
    cap, curr_stock, warn = get_tank_stock()
    stock_percent = (curr_stock / cap * 100) if cap > 0 else 0
    
    if curr_stock <= warn:
        st.error(f"⚠️ *LOW STOCK ALERT!* Tank Stock: {curr_stock:,.2f} Units ({stock_percent:.1f}% Remaining).")
    else:
        st.info(f"🛢️ *Live Tank Level:* {curr_stock:,.2f} / {cap:,.2f} Units ({stock_percent:.1f}% Full)")

    st.markdown("---")

    st.subheader("1️⃣ Shift Setup")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        selected_date = st.date_input("Date:", datetime.now())
    with c2:
        shift = st.selectbox("Shift:", ["Day Shift", "Night Shift"])
    with c3:
        operator_name = st.text_input("Operator Name:", value="Ali Raza")
    with c4:
        nozzle_name = st.selectbox("Select Nozzle:", ["Nozzle 1", "Nozzle 2", "Nozzle 3", "Nozzle 4"])

    st.markdown("---")
    
    st.subheader("2️⃣ Meter Readings")
    m1, m2, m3 = st.columns(3)
    with m1:
        start_reading = st.number_input("Starting Reading:", min_value=0.0, value=1000.0, step=1.0)
    with m2:
        end_reading = st.number_input("Ending Reading:", min_value=0.0, value=1250.0, step=1.0)
    with m3:
        rate = st.number_input("Rate Per Unit (Rs):", min_value=0.0, value=300.0, step=1.0)

    if end_reading < start_reading:
        st.error("⚠️ Ending reading starting reading se kam nahi ho sakti!")
    else:
        qty_sold = end_reading - start_reading
        total_amount = qty_sold * rate

        st.success(f"📊 *Calculated Volume:* {qty_sold:.2f} Units | *Calculated Revenue:* Rs {total_amount:,.2f}")

        st.markdown("---")
        
        st.subheader("3️⃣ Cash Reconciliation & Expenses")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            cash_received = st.number_input("Cash Received (Rs):", min_value=0.0, value=float(total_amount))
        with f2:
            online_received = st.number_input("Online Payment (Rs):", min_value=0.0, value=0.0)
        with f3:
            credit_amount = st.number_input("Udhaar / Credit (Rs):", min_value=0.0, value=0.0)
        with f4:
            expenses = st.number_input("Shift Expenses (Rs):", min_value=0.0, value=0.0)

        net_cash_in_hand = cash_received - expenses

        st.markdown("### 💵 Financial Summary")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Sale", f"Rs {total_amount:,.2f}")
        k2.metric("Total Collected", f"Rs {(cash_received + online_received + credit_amount):,.2f}")
        k3.metric("Expenses", f"Rs {expenses:,.2f}")
        k4.metric("Net Cash Drawer", f"Rs {net_cash_in_hand:,.2f}")

        if st.button("💾 Save Shift Record", type="primary"):
            save_entry(
                selected_date.strftime("%Y-%m-%d"),
                shift,
                operator_name,
                nozzle_name,
                start_reading,
                end_reading,
                qty_sold,
                rate,
                total_amount,
                cash_received,
                online_received,
                credit_amount,
                expenses,
                net_cash_in_hand
            )
            st.success("✅ Entry Saved & Tank Stock Auto-Updated!")
            st.rerun()

    st.markdown("---")
    st.subheader("📜 Master Ledger History & Date Filter")
    
    # Date Range Filter Added Here
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        f_start = st.date_input("From Date:", datetime.now())
    with filter_col2:
        f_end = st.date_input("To Date:", datetime.now())

    df_history = load_data(f_start.strftime("%Y-%m-%d"), f_end.strftime("%Y-%m-%d"))
    
    if not df_history.empty:
        st.dataframe(df_history, use_container_width=True)
        
        if is_admin:
            st.markdown("---")
            del_c1, del_c2 = st.columns([2, 1])
            with del_c1:
                delete_id = st.number_input("Delete Record ID:", min_value=1, step=1)
            with del_c2:
                st.write("")
                st.write("")
                if st.button("❌ Delete Record"):
                    delete_entry(delete_id)
                    st.error(f"Record #{delete_id} Deleted!")
                    st.rerun()

        st.markdown("---")
        csv_data = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered History (CSV)",
            data=csv_data,
            file_name=f"Station_Sales_{datetime.now().strftime('%Y_%m_%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Mukhtarafa tareeq (Selected dates) mein koi record maujood nahi hai.")

elif calc_type == "🧾 Shift Receipt & Print Slip":
    st.header("🧾 Official Shift Receipt Slip")
    df_receipts = load_data()
    if not df_receipts.empty:
        selected_id = st.selectbox("Select Record ID for Receipt:", df_receipts["ID"].tolist())
        record = df_receipts[df_receipts["ID"] == selected_id].iloc[0]

        receipt_box = f"Official Shift Receipt - ID: {selected_id}"
                          
