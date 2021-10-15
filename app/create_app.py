import os
import mysql.connector

class DBManager:
    def __init__(self, database='andrey04', host="db", user="root", password="root"):
        self.connection = mysql.connector.connect(
            user=user, 
            password=password,
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()
    
    def query_titles(self):
        self.cursor.execute('SELECT * FROM nomenclature')
        rec = []
        for c in self.cursor.fetchall():
            rec.append(c)
        return rec

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