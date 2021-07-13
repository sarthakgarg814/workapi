import mysql.connector as my
from flask import Flask, jsonify
import itertools

app = Flask(__name__)

connection = my.connect(user='root',password='blc332',host='localhost', database='user_info')
cursor = connection.cursor()

table_com  = f'CREATE TABLE IF NOT EXISTS data(username varchar(255) PRIMARY KEY, password varchar(200), description varchar(255))'
cursor.execute(table_com)

@app.route('/app/user/<string:u>/<string:p>')
def create_user(u, p):
    username = u
    passw = p

    try:
        insert_com = 'INSERT INTO data values(%s,%s,%s)'
        data_ = [u,p, 'NULL']
        cursor.execute(insert_com, data_)
        connection.commit()
        return 'Registered Successfully!'

    except my.errors.IntegrityError:
        return 'Username Already Exists'

@app.route('/app/user/auth/<string:au>/<string:ap>')
def auth(au,ap):
    fetch = 'SELECT * FROM data'
    cursor.execute(fetch)
    data_tuple = cursor.fetchall()
    data_list = list(itertools.chain(*data_tuple))

    
    for i in range(0,int(len(data_list)/3)):
        if au == data_list[i*3] and ap == data_list[(i*3)+1]:
            return 'Login Successfull!'
    
    return 'unsucess'


if __name__ == '__main__':
    app.run(debug=True)
