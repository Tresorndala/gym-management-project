import streamlit as st
import mysql.connector
import pandas as pd

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Minushbest#0"
DB_NAME = "gym_database"

# Connect to the database
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        port='3307',
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
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
        table = st.selectbox("Select Table", ["staff", "inventory_table", "gym_equipment_table", 
                                              "class_schedules", "training_programs", "members", 
                                              "visitor_table", "attendance", "damage", "feedback", 
                                              "booking", "payment", "class_attendance"])

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
                query = "SELECT position FROM staff WHERE staffID = %s;"
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
                    CALL insert_member(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    try:
                        cursor.execute(query, (memberID, programID, last_name, first_name, mtype_price, start_date, end_date, contact_information, membership_type, current_user_id))
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
                        query = f"""
                        UPDATE members
                        SET last_name = %s, first_name = %s, mtype_price = %s, start_date = %s, end_date = %s, contact_information = %s, membership_type = %s
                        WHERE memberID = %s;
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
            GROUP_CONCAT(staff.workers_name
            ORDER BY staff.workers_name
            SEPARATOR ', ') AS tutors
        FROM booking
        JOIN members ON booking.memberID = members.memberID
        JOIN class_schedules ON booking.staffID = class_schedules.staffID
        JOIN training_programs ON class_schedules.programID = training_programs.programID
        JOIN staff ON class_schedules.staffID = staff.staffID
        GROUP BY training_programs.program_name;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    elif choice == "Equipment Damage Analysis":
        st.subheader("Equipment Damage Analysis")

        query = """
        SELECT
            DATE_FORMAT(d.damage_date, '%Y-%m') as month,
            i.item_name,
            COUNT(d.damageID) as damage_count,
            SUM(d.cost) as total_cost
        FROM inventory_table i
        JOIN damage d on i.inventoryID = d.inventoryID
        GROUP BY month, i.item_name
        ORDER BY month, damage_count DESC;
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
            m.mtype_price AS membership_price,
            COALESCE(SUM(p.amount), 0) AS total_payments,
            m.mtype_price - COALESCE(SUM(p.amount), 0) AS outstanding_membership_balance,
            COALESCE(SUM(d.cost), 0) AS total_damage_cost,
            COALESCE(SUM(d.cost), 0) - COALESCE(SUM(pd.amount), 0) AS outstanding_damage_balance
        FROM
            members m
        LEFT JOIN
            payment p ON m.memberID = p.person_ID
            AND p.reason_for_payment = 'Annual Membership Fee'
        LEFT JOIN
            damage d ON m.memberID = d.personID
            AND d.person_type = 'member'
        LEFT JOIN
            payment pd ON d.damageID = pd.person_ID
            AND pd.reason_for_payment = 'Equipment Damage'
        GROUP BY
            m.memberID, m.first_name, m.last_name, m.mtype_price
        HAVING
            (m.mtype_price - COALESCE(SUM(p.amount), 0)) > 0
            OR (COALESCE(SUM(d.cost), 0) - COALESCE(SUM(pd.amount), 0)) > 0;
        """
        df = pd.read_sql_query(query, conn)
        st.write(df)

    # elif choice == "Attendance of All Present Individuals":
    #     st.subheader("Attendance of All Present Individuals")

    #     person_type = st.selectbox("Select Person Type", ["member", "staff"])

    #     query = f"""
    #     SELECT
    #         CONCAT(m.first_name, ' ', m.last_name) AS person_name,
    #         a.date,
    #         a.arrival_time,
    #         a.departure_time,
    #         cs.class_name
    #     FROM
    #         attendance a
    #     JOIN members m ON a.personID = m.memberID
    #     # JOIN class_schedules cs ON a.classID = cs.classID
    #     WHERE a.person_type = '{person_type}'
    #     ORDER BY a.date, a.arrival_time, person_name;
    #     """
    #     df = pd.read_sql_query(query, conn)
    #     st.write(df)

    conn.close()

if __name__ == "__main__":
    main()
