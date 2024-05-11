##
import os
import pyodbc

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/main', methods=['POST'])
def main():
    #DB_HOST = os.getenv("DB_HOST")
    #DB_USER = os.getenv("DB_USER")
    #DB_PASS = os.getenv("DB_PASS")
    #DB_DDBB = os.getenv("DB_DDBB")

    # Configuración de los parámetros de conexión
    DB_DDBB = "ZRZ2"
    DB_HOST = "zrz-udp-server.database.windows.net"
    DB_PASS = "Undertaker3:16"
    DB_USER = "dbravofl"

    # Cadena de conexión
    connection_string = f"""
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={DB_HOST};
    DATABASE={DB_DDBB};
    UID={DB_USER};
    PWD={DB_PASS};
    """

    print(DB_PASS)
  
    #try:
    connection = pyodbc.connect(connection_string)
    
    cursor = connection.cursor()
    cursor.execute("SELECT @@version;")  # Puedes cambiar esto por tu consulta SQL
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()        

    print("conexión exitosa")
    id = str(request.json['id'])

    sql = "select id, nombre, apellido, telefono, email, contrasena, fecha_nacimiento, genero, tipo_usuario, status from usuarios where tipo_usuario='alumno' and id='"+id+"';"
    cursor.execute(sql)
    resp = cursor.fetchall()
    print(str(resp))

    arrayUsers=[]
    retorno = {
        "users":{}
    }
    for registro in resp:
        item={
            "id":registro[0],
            "nombre":registro[1],
            "apellido":registro[2],
            "telefono":registro[3],
            "email":registro[4],
            #"contrasena":registro[5],
            "fecha_nacimiento":registro[6],
            "genero":registro[7],
            "tipo_usuario":registro[8],
            "status":registro[9]
        }
        arrayUsers.append(item)
    retorno['users'] = arrayUsers
    return retorno


if __name__ == '__main__':
   app.run()
