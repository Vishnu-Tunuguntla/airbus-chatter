import psycopg2

conn = None
try:
    # Connect to the database
    conn = psycopg2.connect(
        dbname="postgres",
        user="T1SSU3",
        password="xu24DYAgldOaP0TcyLGG",
        host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cursor = conn.cursor()

    # Optionally disable foreign key checks
    cursor.execute("SET session_replication_role = 'replica';")

    # Find all table names
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()

    # Drop each table
    for table_name, in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        print(f"Dropped table {table_name}")

    # Optionally re-enable foreign key checks
    cursor.execute("SET session_replication_role = 'origin';")

    conn.commit()

except psycopg2.Error as e:
    print(f"An error occurred: {e}")
    if conn is not None:
        conn.rollback()

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
