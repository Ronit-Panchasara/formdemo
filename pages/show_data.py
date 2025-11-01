import streamlit as st
import mysql.connector
import pandas as pd

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="All Submitted Data", layout="wide")

# ---------------------------
# Database connection
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

# ---------------------------
# Fetch data
# ---------------------------
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM demo_form")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# ---------------------------
# Delete row
# ---------------------------
def delete_row(row_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM demo_form WHERE id=%s", (row_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# Main App
# ---------------------------
st.title("🗂️ All Submitted Data")

rows = fetch_data()

if rows:
    df = pd.DataFrame(rows)

    # Show data table
    st.dataframe(df, use_container_width=True)

    st.write("### Actions")

    # Add action buttons for each row
    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([8, 1, 1])

        col1.write(f"**ID:** {row['id']} | **Name:** {row.get('first_name', '')} {row.get('last_name', '')}")

        # Update Button
        if col2.button("✏️ Update", key=f"update_{row['id']}"):
            # Redirect to another page (e.g., edit_form.py) with query parameter
            st.session_state["update_id"] = row["id"]
            st.switch_page("pages/update_data.py")  

        # Delete Button
        if col3.button("🗑️ Delete", key=f"delete_{row['id']}"):
            delete_row(row["id"])
            st.success(f"🗑️ Record with ID {row['id']} deleted successfully!")
            st.rerun()

else:
    st.warning("No records found in the database.")
