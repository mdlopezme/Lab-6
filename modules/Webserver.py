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
from .SERVO import set_permanet_unclock
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

      # config.add_static_view(name='/', path='/home/pi/repositories/ece-140a-winter-2022-mdlopezme/Lab-6/Midterm/web_server/public', cache_max_age=3600)

      # # add PUBLIC_PATH = /home/pi/repositories/ece-140a-winter-2022-mdlopezme/Lab-6/Midterm/web_server/public> 
      # # to credentials.env
      config.add_static_view(name='/', path=public_path, cache_max_age=3600)
      # config.add_static_view(name='/', path='./public', cache_max_age=3600)

      self.app = config.make_wsgi_app()

    self.server = make_server('0.0.0.0', 6543, self.app)

  def start(self):
    print('Web server started on: http://192.168.0.100:6543')
    self.server_thread=threading.Thread(target=self.server.serve_forever(),name="Web Server")
    self.server_thread.start()

  def stop(self):
    print("Ending web server")
    s_shutdown=threading.Thread(target=self.server.shutdown(), name="server shutdown")
    s_shutdown.start()

  def get_home(self,req):
    return FileResponse('./web_server/index.html')

  def door_override(self,req):
    state=req.params['state'] == 'true'
    set_permanet_unclock(state)
    theResponse = []
    return theResponse
  
