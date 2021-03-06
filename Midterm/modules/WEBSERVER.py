#!/usr/bin/env python3
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
import modules.ENVIRONMENT as ENVIRONMENT
from .SERVO import set_permanent_unlock
import threading

class WebLock():
  def __init__(self):
    with Configurator() as config:
      # Add routes
      config.add_route('home', '/')
      config.add_route('door', '/door')
      config.add_route('bell', '/bell')
      config.add_route('override', '/override')
      config.add_route('users', '/users')

      # Create views for routes
      config.add_view(self.get_home, route_name='home')
      config.add_view(self.door_query, route_name='door', renderer='json')
      config.add_view(self.bell_query, route_name='bell', renderer='json')
      config.add_view(self.door_override, route_name='override')
      config.add_view(self.users_query, route_name='users', renderer='json')

      # Static Routes
      config.add_static_view(name='/', path='main:web_server/public/', cache_max_age=3600)
      
      app = config.make_wsgi_app()

    self.server = make_server('0.0.0.0', 6543, app)

  def start(self):
    print('Web server started on: http://192.168.0.100:6543')
    self.server_thread=threading.Thread(target=self.server.serve_forever,name="Web Server")
    self.server_thread.start()

  def stop(self):
    print("Ending web server")
    self.server.shutdown()

  def get_home(self,req):
    return FileResponse('./web_server/index.html')

  def door_override(self,req):
    the_state=req.params['state'] == 'true'
    set_permanent_unlock(the_state)
    return Response()
  
  def query_db(self,a_table,start_date,end_date,time_zone,user="all_users"):
    db = mysql.connect(host=ENVIRONMENT.db_host, user=ENVIRONMENT.db_user, passwd=ENVIRONMENT.db_pass, database=ENVIRONMENT.db_name)
    cursor = db.cursor()
    cursor.execute(f'SET time_zone = "{time_zone}";')
    if "all_users"==user:
      cursor.execute(
        f'SELECT * FROM {a_table} WHERE timestamp BETWEEN '
        f'"{start_date}" AND "{end_date} 23:59:59";'
      )
    else:  
      cursor.execute(
        f'SELECT * FROM {a_table} WHERE timestamp BETWEEN '
        f'"{start_date}" AND "{end_date} 23:59:59" '
        f'AND name="{user.replace("_"," ")}";'
      )
    record = cursor.fetchall()
    db.close()
    if 0==len(record):
        return False
    print('record found')
    return record

  def door_query(self,req):
    start_date=req.params['start']
    end_date=req.params['end']
    time_zone=req.params['timezone']
    the_user=req.params['user']
    # print(f'start: {start_date}\nend: {end_date}')
    the_record=self.query_db('User_Auth',start_date,end_date,time_zone,the_user)
    if not the_record:
      print("no record")
      return {'id' : "No records."}
    the_response=[]
    for item in the_record:
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
    the_record=self.query_db('Bell_Rings',start_date,end_date,time_zone)

    if not the_record:
      print("no record")
      return {'id' : "No records."}
    the_response=[]
    for item in the_record:
      the_response.append(
        {
          'id' : item[0],
          'ringed' : item[1],
          'timestamp' : str(item[2])
        }
      )
    return the_response

  def users_query(self,req):
    db = mysql.connect(host=ENVIRONMENT.db_host, user=ENVIRONMENT.db_user, passwd=ENVIRONMENT.db_pass, database=ENVIRONMENT.db_name)
    cursor = db.cursor()
    cursor.execute('SELECT name FROM User_Auth GROUP BY name;')
    record = cursor.fetchall()
    db.close()
    if 0==len(record):
        return False
    print('record found')
    the_response=[]
    for item in record:
      the_response.append(
        {
          'value' : item[0].replace(" ","_"),
          'text' : item[0],
        }
      )
    return the_response