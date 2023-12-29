import psycopg2


conn = psycopg2.connect(
    dbname="postgres",
    user="T1SSU3",
    password="xu24DYAgldOaP0TcyLGG",
    host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
    port="5432"
)
cursor = conn.cursor()

# SQL to create Shuttles Table
create_shuttles_table = """
CREATE TABLE Shuttles (
    ShuttleID SERIAL PRIMARY KEY,
    DestinationType VARCHAR(10) CHECK (DestinationType IN ('DEPARTING', 'ARRIVING')),
    Location VARCHAR(10) CHECK (Location IN ('DULLES', 'RICHMOND')),
    PickupLocation TEXT,
    DropoffLocation TEXT,
    PickupTime TIMESTAMP,
    OptionalInformation TEXT
)
"""

# SQL to create Status Table
create_status_table = """
CREATE TABLE Status (
    StatusID SERIAL PRIMARY KEY,
    StatusFlag VARCHAR(255)
)
"""

# SQL to create Passenger Table
create_passenger_table = """
CREATE TABLE Passenger (
    PassengerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    MobileNumber VARCHAR(15),
    EmailAddress VARCHAR(255),
    ShuttleID INTEGER REFERENCES Shuttles(ShuttleID)
)
"""

# Execute the SQL statements
try:
    cursor.execute(create_shuttles_table)
    cursor.execute(create_status_table)
    cursor.execute(create_passenger_table)
    conn.commit()
    print("Tables created successfully.")
except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")

# Close the cursor and the connection
cursor.close()
conn.close()


