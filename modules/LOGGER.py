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

def log_ringer(ringer_info):
    if(ringer_info[2]==True):
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
            INSERT INTO Bell_Rings (ringed) VALUES ({ringer_info[0]});
        ''')
        db.commit()
        print("RINGER DATABASE UPDATED")
    except:
        print(Exception)
    db.close()
    ringer_info[2]=True

def log(user_credentials,ringer_info, kill_threads):
    while(not kill_threads[0]):
        log_user_auths(user_credentials)
        log_ringer(ringer_info)
        sleep(1)