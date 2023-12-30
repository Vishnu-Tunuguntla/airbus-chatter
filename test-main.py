import psycopg2


# Establishing the connection
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="T1SSU3",
        password="xu24DYAgldOaP0TcyLGG",
        host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cursor = conn.cursor()
    # SQL query to fetch all data from Shuttles table
    query = "SELECT * FROM Shuttles;"
    cursor.execute(query)

    # Fetch and print all rows from the database
    records = cursor.fetchall()
    cursor.close()
    for row in records:
        print(row)

except psycopg2.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Closing the cursor and connection
    if conn:
        conn.close()
