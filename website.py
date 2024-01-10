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
page = st.sidebar.selectbox("Select Function", ["Home", "Database Requests", "Add Shuttle", "Upload Passengers", "View Data"])

if page == "Home":
    st.title("Welcome to the Airbus Manager!")
    st.write("This website allows Airbus administrators to easily access Airbus data and perform simple tasks.")

elif page == "Database Requests":
    st.title("Ticket Functions")
    message_placeholder = st.empty()  # Placeholder for the success message

    with st.form(key='delete'):
        delete_function = st.selectbox("Delete", ["None", "Passengers and Shuttles", "Passengers"])
        submit_button = st.form_submit_button(label='execute')

        if submit_button:
            query_deletePassenger = """
                DELETE FROM Passengers;
            """
            query_deleteShuttles = """
                DELETE FROM Shuttles;
            """
            try:
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
                conn.commit()

                # Display success message
                message_placeholder.success("Success!")
                time.sleep(5)
                message_placeholder.empty()  # Clear the message after 5 seconds

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
        req_description = st.text_area("Request Information", key='req_description')
        request_button = st.form_submit_button(label='Submit Request')
        message_placeholder = st.empty()  # Create a placeholder for messages

    if request_button:
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
                INSERT INTO Requests (FirstName, LastName, EmailAddress, RequestDescription)
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(insert_query, (first_name, last_name, email, req_description))
            cursor.close()
            conn.commit()

            # Display success message
            message_placeholder.success("Request Added")
            time.sleep(5)
            message_placeholder.empty()  # Clear the message

        except psycopg2.Error as e:
            st.error("An error occurred: " + str(e))
            conn.rollback()

        finally:
            if conn:
                conn.close()

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
    if st.session_state.get('data_processed', False):
        st.success("Successfully added to the database!")
        time.sleep(5)
        st.session_state['data_processed'] = False
        st.session_state['show_uploader'] = True  # Reset uploader visibility
        st.experimental_rerun()

    # Show the file uploader only if the flag is True
    if st.session_state.get('show_uploader', True):
        uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")

        if uploaded_file is not None and uploaded_file.name.endswith('.xlsx'):
            # Button to trigger data processing
            process_data_button = st.button("Process and Upload Data")

            if process_data_button:
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

                    # Iterate and insert data
                    for index, row in df.iterrows():
                        cursor.execute("""
                            INSERT INTO Passengers (FirstName, LastName, CellPhone, TicketQuantity, EmailAddress, ShuttleID)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (row['First Name'], row['Last Name'], row['Cell Phone'], row['Quantity'], row['Email'], row['Ticket Type']))

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
elif page == "View Data":
    st.title("View Data")
    # Use markdown to display a link that opens in a new tab
    st.markdown(
        "[Redirect to Google Sheets](https://docs.google.com/spreadsheets/d/1kCYoZR1U2K7InAW8YwXM8KvbpTDe5kVABEEesske1Ng/edit#gid=819535538)",
        unsafe_allow_html=True,
    )



