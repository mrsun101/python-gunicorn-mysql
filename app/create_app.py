import os
from mymod.dbmanager import DBManager

conn = None

def create_app(environ, start_response):
    global conn
    if not conn:
        conn = DBManager()        
    rec = conn.query_titles()
    response = ''
    for c in rec:
        response = response  + '<div> ' + str(c[0]) + '. '+str(c[1])+'</div>'
    for key,volume in environ.items():
        response = response + '<div>' + str(key)+ ' --> '+str(volume)+'</div>'
    response = response.encode('utf-8')
    data = b'Hello,world!!!\n'
    start_response('200 OK',[
        ('Content-type','text/html; charset=utf-8'),
        ('Content-length',str(len(response)))
    ])
    return iter([response])