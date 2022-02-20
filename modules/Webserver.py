from logging import shutdown
from sys import modules
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
import mysql.connector as mysql
from dotenv import load_dotenv
import os
# import datetime
from .SERVO import set_permanent_unlock
from time import sleep
import threading

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
public_path = os.environ['PUBLIC_PATH']

class WebLock():
  def __init__(self):
    with Configurator() as config:
      config.add_route('home', '/')
      config.add_view(self.get_home, route_name='home')

      config.add_route('lock', '/lock/{state}')
      config.add_view(self.door_override, route_name='lock')
      config.add_route('door', '/door')
      config.add_view(self.door_querry, route_name='door', renderer='json')
      config.add_route('bell', '/bell')
      config.add_view(self.bell_query, route_name='bell', renderer='json')
      config.add_route('override', 'override')
      config.add_view(self.door_override, route_name='override', renderer='json')

      # config.add_static_view(name='/', path=public_path, cache_max_age=3600)
      config.add_static_view(name='/', path='main:web_server/public/', cache_max_age=3600)
      app = config.make_wsgi_app()

    self.server = make_server('0.0.0.0', 6543, app)

  def start(self):
    print('Web server started on: http://192.168.0.100:6543')
    self.server_thread=threading.Thread(target=self.server.serve_forever,name="Web Server")
    self.server_thread.start()

  def stop(self):
    # print(f'server thread is {self.server_thread.is_alive()}')
    print("Ending web server")
    self.server.shutdown()
    s_shutdown=threading.Thread(target=self.server.shutdown, name="server shutdown")
    s_shutdown.start()
    # print(f'server thread is {self.server_thread.is_alive()}')

  def get_home(self,req):
    return FileResponse('./web_server/index.html')

  def door_override(self,req):
    the_state=req.params['state'] == 'true'
    set_permanent_unlock(the_state)
    theResponse = []
    return theResponse
  
  def querry_db(self,a_table,start_date,end_date,time_zone):
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

  def door_querry(self,req):
    start_date=req.params['start']
    end_date=req.params['end']
    time_zone=req.params['timezone']
    print(f'start: {start_date}\nend: {end_date}')
    the_record=self.querry_db('User_Auth',start_date,end_date,time_zone)
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
    return the_response
  
  def bell_query(self,req):
    start_date=req.params['start']
    end_date=req.params['end']
    time_zone=req.params['timezone']
    print(f'start: {start_date}\nend: {end_date}')
    the_record=self.querry_db('Bell_Rings',start_date,end_date,time_zone)

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
    return the_response

