from dotenv import load_dotenv
import os

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
# public_path = os.environ['PUBLIC_PATH']
OLIVIER_ROGERS = os.environ['OLIVIER_ROGERS']
MOISES_LOPEZ = os.environ['MOISES_LOPEZ']
