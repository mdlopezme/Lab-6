import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(user=db_user,password=db_pass,host=db_host)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE Smart_Home;")
except:
    print('Database already exists, exiting')
    db.close()
    exit()

cursor.execute("USE Smart_Home;")

cursor.execute("DROP TABLE IF EXISTS Bell_Rings;")
cursor.execute("DROP TABLE IF EXISTS User_Auth;")

try:
    cursor.execute("""
        CREATE TABLE User_Auth (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(50) NOT NULL,
            timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accepted    BOOL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE Bell_Rings (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            ringed      BOOL NOT NULL,
            timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        );
    """)
except RuntimeError as err:
    print('RuntimeError: {err}')

db.close()