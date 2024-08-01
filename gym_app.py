import streamlit as st
import sqlite3
import pandas as pd

# Database path
DB_PATH = 'gym_database.db'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def main():
    st.title('Gym Management System')

    menu = [
        "Home",
        "View Data",
        "Add Member",
        "Update Member",
        "View Popular Class",
        "View Receptionist Added Members",
        "Bookings and Program Details",
        "Training Programs Analysis",
        "Equipment Damage Analysis",
        "Member Payment and Damage Balances"
    ]
    choice = st.sidebar.selectbox("Select Option", menu)

    conn = get_db_connection()

    try:
        if choice == "View Data":
            st.subheader("View Data")
            table = st.selectbox("Select Table", ["staff", "members", "class_schedules", 
                                                  "training_programs", "booking"])

            query = f"SELECT * FROM {table};"
            df = pd.read_sql_query(query, conn)
            st.write(df)

        elif choice == "Add Member":
            # Implementation for adding a member
            pass

        elif choice == "Update Member":
            # Implementation for updating a member
            pass

        elif choice == "View Popular Class":
            # Implementation for viewing popular class
            pass

        elif choice == "View Receptionist Added Members":
            # Implementation for viewing receptionist added members
            pass

        elif choice == "Bookings and Program Details":
            # Implementation for bookings and program details
            pass

        elif choice == "Training Programs Analysis":
            # Implementation for training programs analysis
            pass

        elif choice == "Equipment Damage Analysis":
            # Implementation for equipment damage analysis
            pass

        elif choice == "Member Payment and Damage Balances":
            # Implementation for member payment and damage balances
            pass

    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
