# from urllib import response
from sys import modules
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
import mysql.connector as mysql
from dotenv import load_dotenv
import os
# import datetime
from .SERVO import set_permanet_unclock
from time import sleep

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
public_path = os.environ['PUBLIC_PATH']

def get_home(req):
    return FileResponse('./web_server/index.html')

def querry_db(a_table,start_date,end_date,time_zone):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    cursor.execute(f'SET time_zone = "{time_zone}";')
    cursor.execute(
        f'SELECT * FROM {a_table} WHERE timestamp BETWEEN '
        f'"{start_date}" AND "{end_date} 23:59:59";'
    )
    record = cursor.fetchall()
    db.close()
    if 0==len(record):
        return False
    print('record found')
    return record


def door_querry(req):
    start_date=req.params['start']
    end_date=req.params['end']
    time_zone=req.params['timezone']
    print(f'start: {start_date}\nend: {end_date}')
    the_record=querry_db('User_Auth',start_date,end_date,time_zone)
    # print(the_record)
    if not the_record:
        print("no record")
        return {'id' : "No records."}
    the_response=[]
    for item in the_record:
        # print(item[2])
        # the_timestamp=item[2]
        # print(the_timestamp)
        the_response.append(
            {
                'id' : item[0],
                'name' : item[1].strip(),
                'timestamp' : str(item[2]),
                'success' : item[3]
            }
        )

    # print(the_response)
    return the_response

def bell_query(req):
    start_date=req.params['start']
    end_date=req.params['end']
    time_zone=req.params['timezone']
    print(f'start: {start_date}\nend: {end_date}')
    the_record=querry_db('Bell_Rings',start_date,end_date,time_zone)

    if not the_record:
        print("no record")
        return {'id' : "No records."}
    the_response=[]
    for item in the_record:
        # print(item[2])
        # the_timestamp=item[2]
        # print(the_timestamp)
        the_response.append(
            {
                'id' : item[0],
                'ringed' : item[1],
                'timestamp' : str(item[2])
            }
        )
    # print(the_response)
    return the_response

def door_override(req):
    state=req.params['state'] == 'true'
    set_permanet_unclock(state)
    theResponse = []
    return theResponse

def main(kill_threads):
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(get_home, route_name='home')

        config.add_route('lock', '/lock/{state}')
        config.add_view(door_override, route_name='lock')
        config.add_route('door', '/door')
        config.add_view(door_querry, route_name='door', renderer='json')
        config.add_route('bell', '/bell')
        config.add_view(bell_query, route_name='bell', renderer='json')
        config.add_route('override', 'override')
        config.add_view(door_override, route_name='override', renderer='json')

        # config.add_static_view(name='/', path='/home/pi/repositories/ece-140a-winter-2022-mdlopezme/Lab-6/Midterm/web_server/public', cache_max_age=3600)

        # # add PUBLIC_PATH = /home/pi/repositories/ece-140a-winter-2022-mdlopezme/Lab-6/Midterm/web_server/public> 
        # # to credentials.env
        config.add_static_view(name='/', path=public_path, cache_max_age=3600)
        # config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    print('Web server started on: http://192.168.0.100:6543')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Closing webserver')
        server.server_close()

if __name__ == '__main__':
    main()