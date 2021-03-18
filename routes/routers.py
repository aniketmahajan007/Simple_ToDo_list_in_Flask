import html
import yaml
from flask_mysqldb import MySQL
import json
from flask import request, render_template

from main import app

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


@app.route('/')
def home():
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM task")
    fetch = conn.fetchall()
    return render_template('home.html', task=fetch)


@app.route('/add', methods=['POST'])
def add():
    task = request.get_json()
    error = 0
    try:
        task["task"]
    except:
        error = 1
    if error:
        return {"Error": "Please Fill all rhe required fields"}, 200, {'Content-type': 'application/json'}
    task["task"] = html.escape(task["task"])
    conn = mysql.connection.cursor()
    conn.execute("INSERT INTO task (tasked) VALUE (%s)", {task["task"]})
    mysql.connection.commit()
    conn.close()
    return {"Success": "Successfully Added"}, 200, {'Content-type': 'application/json'}


@app.route('/checked/<int:id>', methods=['PUT'])
def checked(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    conn = mysql.connection.cursor()
    conn.execute("UPDATE task SET status=1 WHERE id=%s", {id})
    mysql.connection.commit()
    conn.close()
    return {"Success": "Successfully Updated"}, 200, {'Content-type': 'application/json'}

@app.route('/unchecked/<int:id>', methods=['PUT'])
def unchecked(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    conn = mysql.connection.cursor()
    conn.execute("UPDATE task SET status=0 WHERE id=%s", {id})
    mysql.connection.commit()
    conn.close()
    return {"Success": "Successfully Updated"}, 200, {'Content-type': 'application/json'}


@app.route('/remove/<int:id>', methods=['DELETE'])
def remove(id):
    if id < 0:
        return {"Error": "Invalid Data"}, 200, {'Content-type': 'application/json'}
    conn = mysql.connection.cursor()
    conn.execute("DELETE FROM task WHERE id=%s", {id})
    mysql.connection.commit()
    conn.close()
    return {"Success": "Successfully Deleted"}, 200, {'Content-type': 'application/json'}

@app.route('/clear', methods=['DELETE'])
def clear():
    conn = mysql.connection.cursor()
    conn.execute("DELETE FROM task")
    mysql.connection.commit()
    conn.close()
    return {"Success": "Successfully Deleted"}, 200, {'Content-type': 'application/json'}