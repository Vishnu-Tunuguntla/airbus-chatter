import streamlit as st
import psycopg2
import time
import pandas as pd

# Initialize session state variables if not already set
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False
if 'data_processed' not in st.session_state:
    st.session_state['data_processed'] = False
if 'show_uploader' not in st.session_state:
    st.session_state['show_uploader'] = True

# Dropdown menu for navigation
page = st.sidebar.selectbox("Select Function", ["Home", "Database Requests", "Add Shuttle", "Upload Passengers"])

if page == "Home":
    st.title("Welcome to the Airbus Manager!")
    st.write("This website allows Airbus administrators to easily access Airbus data and perform simple tasks.")

elif page == "Database Requests":
    st.title("Ticket Functions")
    with st.form(key='delete'):
        delete_function = st.selectbox("Delete", ["None", "Passengers and Shuttles", "Passengers"])
        submit_button = st.form_submit_button(label='execute')
        #Deleting from Database
        if submit_button:
            query_deletePassenger = """
                DELETE FROM Passengers;
            """
            query_deleteShuttles = """
                DELETE FROM Shuttles;
            """
            try:
                # Database connection parameters
                conn = psycopg2.connect(
                    dbname="postgres",
                    user="T1SSU3",
                    password="xu24DYAgldOaP0TcyLGG",
                    host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
                    port="5432"
                )
                cursor = conn.cursor()
                if delete_function == "Passengers and Shuttles":
                    cursor.execute(query_deletePassenger)
                    cursor.execute(query_deleteShuttles)
                elif delete_function == "Passengers":
                    cursor.execute(query_deletePassenger)

                cursor.close()
                # Commit the transaction
                conn.commit()
            except psycopg2.Error as e:
                st.error("An error occurred: " + str(e))
                conn.rollback()

            finally:
                if conn:
                    conn.close()
                    st.rerun()

    with st.form(key='switch'):
        first_name = st.text_area("First Name", key='first_name')
        last_name = st.text_area("Last Name", key='last_name')
        email = st.text_area("Email Address", key='email')
        switch_request = st.text_area("Request Information", key='switch_request')
        request_button = st.form_submit_button(label='Submit Request')
        #Adding special request to database


elif page == "Add Shuttle":
    st.title("Add Shuttle")

    # Check if form was previously submitted; if so, clear the form
    if st.session_state['form_submitted']:
        st.session_state['form_submitted'] = False
        st.rerun()

    with st.form(key='shuttle_form'):
        primary_identification_key = st.text_area("Ticket Type [Primary Key]", key='primary_identification_key')
        route = st.selectbox("Route", ["DULLES -> UVA", "RICHMOND -> UVA", "UVA -> DULLES", "UVA -> RICHMOND"])
        pickup_time = st.text_area("Pickup Time", key='pickup_time')
        optional_info = st.text_area("Optional Information", key='optional_info')
        submit_button = st.form_submit_button(label='Add Shuttle')

        if submit_button:
            # Display success message
            st.success("Submitted Shuttle Information!")
            # Set form submitted state to True
            st.session_state['form_submitted'] = True
            # Pause to show the message, then rerun to clear the form
            time.sleep(5)

            # Database Insert
            try:
                # Database connection parameters
                conn = psycopg2.connect(
                    dbname="postgres",
                    user="T1SSU3",
                    password="xu24DYAgldOaP0TcyLGG",
                    host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
                    port="5432"
                )
                cursor = conn.cursor()

                # SQL query to insert data
                insert_query = """
                INSERT INTO Shuttles (ShuttleID, Route, PickupTime, OptionalInformation)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (primary_identification_key, route, pickup_time, optional_info))
                cursor.close()
                # Commit the transaction
                conn.commit()
                st.success("Shuttle information added successfully!")

            except psycopg2.Error as e:
                st.error("An error occurred: " + str(e))
                conn.rollback()

            finally:
                if conn:
                    conn.close()

            # Rerun the app to clear the form
            st.rerun()
elif page == "Upload Passengers":

    # Check if data was processed; if so, display message and reset states
    if st.session_state['data_processed']:
        st.success("Successfully added to the database!")
        time.sleep(5)
        st.session_state['data_processed'] = False
        st.session_state['show_uploader'] = True  # Reset uploader visibility
        st.experimental_rerun()

    # Show the file uploader only if the flag is True
    if st.session_state['show_uploader']:
        uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")

        # Validate file upload and verify .xlsx
        if uploaded_file is not None and uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

            # Establishing connection
            try:
                conn = psycopg2.connect(
                    dbname="postgres",
                    user="T1SSU3",
                    password="xu24DYAgldOaP0TcyLGG",
                    host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
                    port="5432"
                )
                cursor = conn.cursor()

                # Iterate over the DataFrame and insert each row into the database
                for index, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO Passengers (FirstName, LastName, CellPhone, TicketQuantity, EmailAddress, ShuttleID)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (row['First Name'], row['Last Name'], row['Cell Phone'], row['Quantity'], row['Email'], row['Ticket Type']))

                # Commit the changes and close the connection
                conn.commit()
                st.session_state['data_processed'] = True
                st.session_state['show_uploader'] = False  # Hide the uploader
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error inserting row {index}: {e}")
            finally:
                if conn:
                    conn.close()
                    cursor.close()



