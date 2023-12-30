import streamlit as st
import psycopg2
import time

# Initialize session state variables if not already set
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

# Dropdown menu for navigation
page = st.sidebar.selectbox("Select Function", ["Home", "Shuttle Data", "Event Manager"])

if page == "Home":
    st.title("Welcome to the Airbus Manager!")
    st.write("This website allows Airbus administrators to easily access Airbus data and perform simple tasks.")

elif page == "Shuttle Data":
    st.title("Shuttle Data")
    st.write("Here you can view and manage shuttle data.")

elif page == "Event Manager":
    st.title("Event Manager")

    # Check if form was previously submitted; if so, clear the form
    if st.session_state['form_submitted']:
        st.session_state['form_submitted'] = False
        st.rerun()

    with st.form(key='shuttle_form'):
        destination_type = st.selectbox("Destination Type", ["DEPARTING", "ARRIVING"])
        location = st.selectbox("Location", ["DULLES", "RICHMOND"])
        pickup_location = st.text_area("Pickup Location", key='pickup_location')
        dropoff_location = st.text_area("Dropoff Location", key='dropoff_location')
        pickup_time = st.text_input("Pickup Time", value="", key='pickup_time')
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
                INSERT INTO Shuttles (DestinationType, Location, PickupLocation, DropoffLocation, PickupTime, OptionalInformation)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (destination_type, location, pickup_location, dropoff_location, pickup_time, optional_info))
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
