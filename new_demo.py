import streamlit as st
import mysql.connector
import datetime
import re

def get_connection():
     return mysql.connector.connect(
        host=st.secrets["sql12.freesqldatabase.com"],      # e.g. "sql12.freesqldatabase.com"
        user=st.secrets["sql12805592"],      # your DB username
        password=st.secrets["i1dgYYx6ac"],  # your DB password
        database=st.secrets["sql12805592"],  # your DB name
        port=st.secrets["3306"]  
    )

st.set_page_config(page_title="All Submitted Data", layout="wide")
st.title("Registration Form")

# --- Form ---
with st.form("contact_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        fname = st.text_input("First Name")
        mname = st.text_input("Middle Name")
        lname = st.text_input("Last Name")

    with col2:
        gender = st.radio("Gender", ["Male", "Female"])
        hobby = st.multiselect("Hobbies", ["Reading", "Sports", "Travelling"])
        city = st.selectbox("City", ["Rajkot", "Ahemdabad", "Surat", "Vadodara"])

    address = st.text_area("Address")
    email = st.text_input("Email")
    
    # --- Mobile number input ---
    raw_mnumber = st.text_input("Mobile Number")
    # Keep only digits
    mnumber = ''.join(filter(str.isdigit, raw_mnumber))
    # Limit to max 10 digits
    if len(mnumber) > 10:
        mnumber = mnumber[:10]

    birthdate = st.date_input(
        "Birthdate",
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date(3000, 12, 31),
        value=datetime.date(2000, 1, 1)
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    # --- Email validation ---
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email.strip():
        st.warning("⚠️ Please enter your Email before submitting.")
    elif not re.match(email_pattern, email):
        st.warning("⚠️ Please enter a valid Email address.")
    elif not mnumber:
        st.warning("⚠️ Please enter your Mobile Number before submitting.")
    elif len(mnumber) != 10:
        st.warning("⚠️ Mobile number must be exactly 10 digits long. No more, no less.")
    else:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO demo_form
                (first_name, middle_name, last_name, gender, hobby, address, email, mobile, city, birthdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fname, mname, lname, gender,
                ", ".join(hobby), address, email,
                mnumber, city, str(birthdate)
            ))
            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Data inserted successfully!")
            st.switch_page("pages/show_data.py")

        except mysql.connector.Error as err:

            st.error(f"❌ Database error: {err}")

