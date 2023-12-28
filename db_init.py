import psycopg2


conn = psycopg2.connect(
    dbname="airbus-database", 
    user="T1SSU3", 
    password="xu24DYAgldOaP0TcyLGG", 
    host="airbus-database.c9gssgcyk1lb.us-east-1.rds.amazonaws.com", 
    port="5432"
)

cursor = conn.cursor()

