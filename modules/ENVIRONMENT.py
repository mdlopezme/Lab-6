from dotenv import load_dotenv
import os

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Include NFC IDs for all authorized users
OLIVIER_ROGERS = 397475334654 
MOISES_LOPEZ = 288461690070