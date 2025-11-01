import streamlit as st
import mysql.connector
import re

# ---------------- Database Connection ----------------
def get_connection():
     return mysql.connector.connect(
         host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        port=st.secrets["DB_PORT"]
)

# ---------------- Fetch Record ----------------
def fetch_record(row_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM demo_form WHERE id=%s", (row_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record

# ---------------- Update Record ----------------
def update_record(row_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE demo_form
        SET first_name=%s, middle_name=%s, last_name=%s, gender=%s, 
            hobby=%s, address=%s, email=%s, mobile=%s, city=%s, birthdate=%s
        WHERE id=%s
    """
    values = (
        data["first_name"], data["middle_name"], data["last_name"], data["gender"],
        data["hobby"], data["address"], data["email"], data["mobile"],
        data["city"], data["birthdate"], row_id
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- Validation Functions ----------------
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def is_valid_mobile(mobile):
    return re.match(r'^\d{10}$', mobile) is not None

# ---------------- Duplicate Check ----------------
def is_duplicate_email(email, current_id):
    if not email.strip():
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM demo_form WHERE email=%s AND id != %s", (email, current_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def is_duplicate_mobile(mobile, current_id):
    if not mobile.strip():
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM demo_form WHERE mobile=%s AND id != %s", (mobile, current_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# ---------------- Streamlit Page ----------------
st.title("Update Record")

if "update_id" not in st.session_state:
    st.warning("No record selected for update.")
    st.stop()

row_id = st.session_state["update_id"]
record = fetch_record(row_id)

if not record:
    st.error("Record not found in database.")
    st.stop()

with st.form("update_form"):
    first_name = st.text_input("First Name", value=record["first_name"])
    middle_name = st.text_input("Middle Name", value=record["middle_name"])
    last_name = st.text_input("Last Name", value=record["last_name"])
    gender = st.selectbox("Gender", ["Male", "Female"], index=(0 if record["gender"] == "Male" else 1))
    hobby = st.text_input("Hobby", value=record["hobby"])
    address = st.text_area("Address", value=record["address"])
    
    # Email validation & duplicate check
    email = st.text_input("Email", value=record["email"])
    email_warning = ""
    if email and not is_valid_email(email):
        email_warning = "⚠️ Invalid email format!"
    elif email != record["email"] and is_duplicate_email(email, row_id):
        email_warning = "⚠️ Email is already registered!"
    if email_warning:
        st.warning(email_warning)
    
    # Mobile validation & duplicate check
    mobile = st.text_input("Mobile", value=record["mobile"])
    mobile_warning = ""
    if mobile and not is_valid_mobile(mobile):
        mobile_warning = "⚠️ Mobile number must be 10 digits!"
    elif mobile != record["mobile"] and is_duplicate_mobile(mobile, row_id):
        mobile_warning = "⚠️ Mobile number is already registered!"
    if mobile_warning:
        st.warning(mobile_warning)

    city = st.text_input("City", value=record["city"])
    birthdate = st.date_input("Birthdate", value=record["birthdate"])

    submitted = st.form_submit_button("Update Record")

    # Prevent submission if validation fails
    if submitted:
        if email_warning or mobile_warning:
            st.error("❌ Cannot update. Please fix the warnings above.")
        else:
            updated_data = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "gender": gender,
                "hobby": hobby,
                "address": address,
                "email": email,
                "mobile": mobile,
                "city": city,
                "birthdate": birthdate
            }
            update_record(row_id, updated_data)
            st.success("Record updated successfully! ✅")
            st.session_state.pop("update_id", None)
            st.switch_page("pages/show_data.py")



