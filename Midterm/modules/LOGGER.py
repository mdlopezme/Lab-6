#!/usr/bin/env python3
from time import sleep
import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv('./credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def log_user_auths(user_credentials):
    if(user_credentials[4]==True):
        return
    
    db = mysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name,
    )
    cursor = db.cursor()

    try:
        cursor.execute(f'''
            INSERT INTO User_Auth (name,accepted) VALUES (\'{user_credentials[1]}\',{user_credentials[3]});
        ''')
        db.commit()
        print("LOCK DATABASE UPDATED")
    except:
        print(Exception)
    db.close()
    user_credentials[4]=True

def log_ringer(record_bell_event):
    if(record_bell_event[0]==False):
        return

    db = mysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name,
    )
    cursor = db.cursor()

    try:
        cursor.execute(f'''
            INSERT INTO Bell_Rings (ringed) VALUES (True);
        ''')
        db.commit()
        print("RINGER DATABASE UPDATED")
    except:
        print(Exception)
    db.close()
    record_bell_event[0]=False

def log(user_credentials,bell_event, end_threads):
    while(not end_threads[0]):
        log_user_auths(user_credentials)
        log_ringer(bell_event)
        sleep(1)