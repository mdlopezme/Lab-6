from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def get_home(req):
    return FileResponse('./web_server/index.html')

def door_override(req):
    return Response("Hello")

def main():
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(get_home, route_name='home')

        config.add_route('door', '/door/{state}')
        config.add_view(door_override, route_name='door')

        config.add_static_view(name='/', path='/home/pi/repositories/ece-140a-winter-2022-mdlopezme/Lab-6/Midterm/web_server/public', cache_max_age=3600)

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    print('Web server started on: http://192.168.0.100:6543')
    server.serve_forever()