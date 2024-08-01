import streamlit as st
import sqlite3
import pandas as pd

# Database connection details
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

    if choice == "Home":
        st.subheader("Welcome to the Gym Management System")

    elif choice == "View Data":
        st.subheader("View Data")
        table = st.selectbox("Select Table", ["staff", "members", "class_schedules", 
                                              "training_programs", "booking"])

        query = f"SELECT * FROM {table};"
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Add Member":
        st.subheader("Add New Member")

        # Simulate user login to get the current user's ID and role
        current_user_id = st.text_input("Enter Your ID")
        current_user_role = None

        if st.button("Check Role"):
            with conn.cursor() as cursor:
                query = "SELECT position FROM staff WHERE staffID = ?;"
                cursor.execute(query, (current_user_id,))
                result = cursor.fetchone()
                if result:
                    current_user_role = result[0]
                    st.write(f"Valid ID with role of: {current_user_role}, you can add a member!")
                else:
                    st.error("User not found.")
        
        if current_user_role == 'Receptionist':
            # Display member addition form
            memberID = st.text_input("Member ID")
            programID = st.text_input("Program ID")
            last_name = st.text_input("Last Name")
            first_name = st.text_input("First Name")
            mtype_price = st.number_input("Membership Price", min_value=0.00)
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            contact_information = st.text_input("Contact Information")
            membership_type = st.text_input("Membership Type")

            if st.button("Add Member"):
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO members (memberID, programID, last_name, first_name, mtype_price, start_date, end_date, contact_information, membership_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """
                    try:
                        cursor.execute(query, (memberID, programID, last_name, first_name, mtype_price, start_date, end_date, contact_information, membership_type))
                        conn.commit()
                        st.success("Member added successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.error("Only receptionists can add new members.")

    elif choice == "Update Member":
        st.subheader("Update Member Details")

        memberID = st.text_input("Member ID to Update")

        if memberID:
            query = f"SELECT * FROM members WHERE memberID = '{memberID}';"
            df = pd.read_sql_query(query, conn)
            st.write(df)

            if not df.empty:
                new_last_name = st.text_input("New Last Name", value=df.loc[0, 'last_name'])
                new_first_name = st.text_input("New First Name", value=df.loc[0, 'first_name'])
                new_mtype_price = st.number_input("New Membership Price", min_value=0.00, value=df.loc[0, 'mtype_price'])
                new_start_date = st.date_input("New Start Date", value=pd.to_datetime(df.loc[0, 'start_date']).date())
                new_end_date = st.date_input("New End Date", value=pd.to_datetime(df.loc[0, 'end_date']).date())
                new_contact_information = st.text_input("New Contact Information", value=df.loc[0, 'contact_information'])
                new_membership_type = st.text_input("New Membership Type", value=df.loc[0, 'membership_type'])

                if st.button("Update Member"):
                    with conn.cursor() as cursor:
                        query = """
                        UPDATE members
                        SET last_name = ?, first_name = ?, mtype_price = ?, start_date = ?, end_date = ?, contact_information = ?, membership_type = ?
                        WHERE memberID = ?;
                        """
                        try:
                            cursor.execute(query, (new_last_name, new_first_name, new_mtype_price, new_start_date, new_end_date, new_contact_information, new_membership_type, memberID))
                            conn.commit()
                            st.success("Member updated successfully!")
                        except Exception as e:
                            st.error(f"Error: {e}")

    elif choice == "View Popular Class":
        st.subheader("Most Popular Class")

        query = """
        SELECT 
            cs.classID,
            cs.class_name,
            COUNT(ca.memberID) as total_members,
            tp.program_name,
            s.workers_name as tutor
        FROM 
            class_schedules cs
        JOIN 
            training_programs tp on cs.programID = tp.programID
        LEFT JOIN 
            class_attendance ca on cs.classID = ca.classID
        LEFT JOIN 
            staff s on cs.staffID = s.staffID
        WHERE 
            cs.classID = (
                SELECT 
                    classID
                FROM 
                    class_attendance
                GROUP BY 
                    classID
                ORDER BY 
                    COUNT(memberID) DESC
                LIMIT 1
            )
        GROUP BY 
            cs.classID, cs.class_name, tp.program_name, s.workers_name;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "View Receptionist Added Members":
        st.subheader("Receptionist Added Members")

        query = """
        SELECT 
            memberID,
            programID,
            last_name,
            first_name,
            mtype_price,
            start_date,
            end_date,
            contact_information,
            membership_type
        FROM members;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Bookings and Program Details":
        st.subheader("Bookings and Program Details")

        query = """
        SELECT
            booking.booking_time,
            members.memberID,
            CONCAT(members.first_name, ' ', members.last_name) as Full_name,
            staff.staffID as tutorID,
            staff.workers_name as tutor_name,
            class_schedules.class_name,
            training_programs.program_name
        FROM booking
        JOIN members on booking.memberID = members.memberID
        JOIN class_schedules on booking.staffID = class_schedules.staffID
        JOIN staff on class_schedules.staffID = staff.staffID
        JOIN training_programs on class_schedules.programID = training_programs.programID;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Training Programs Analysis":
        st.subheader("Training Programs Analysis")

        query = """
        SELECT 
            training_programs.program_name,
            COUNT(booking.bookingID) AS Total_bookings,
            GROUP_CONCAT(CONCAT(members.first_name,
                        ' ',
                        members.last_name,
                        ' (',
                        booking.booking_time,
                        ')')
            ORDER BY members.first_name , members.last_name
            SEPARATOR ', ') AS members,
            GROUP_CONCAT(staff.workers_name ORDER BY staff.workers_name SEPARATOR ', ') AS trainers
        FROM booking
        JOIN members ON booking.memberID = members.memberID
        JOIN staff ON booking.staffID = staff.staffID
        JOIN class_schedules ON staff.staffID = class_schedules.staffID
        JOIN training_programs ON class_schedules.programID = training_programs.programID
        GROUP BY training_programs.program_name;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Equipment Damage Analysis":
        st.subheader("Equipment Damage Analysis")

        query = """
        SELECT 
            equipment.equipment_name,
            COUNT(damage.damageID) AS Total_Damages,
            SUM(damage.repair_cost) AS Total_Cost,
            CASE 
                WHEN damage.damage_reported_by = 'member' THEN 'Reported by Member'
                ELSE 'Reported by Staff'
            END AS Reported_By
        FROM damage
        JOIN equipment ON damage.equipmentID = equipment.equipmentID
        GROUP BY equipment.equipment_name, damage.damage_reported_by;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Member Payment and Damage Balances":
        st.subheader("Member Payment and Damage Balances")

        query = """
        SELECT 
            m.memberID,
            m.first_name,
            m.last_name,
            p.amount as Payment,
            d.repair_cost as Damage
        FROM 
            members m
        JOIN 
            payment p on m.memberID = p.memberID
        LEFT JOIN 
            damage d on m.memberID = d.memberID;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    conn.close()

if __name__ == "__main__":
    main()
