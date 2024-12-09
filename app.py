from flask import Flask, request, render_template, redirect
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def create_database():
    connection = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), ['mydatabase'])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('mydatabase')))
        print("База данных 'mydatabase' создана.")

    cursor.close()
    connection.close()

create_database()

conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def create_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    )
    """)
    conn.commit()

create_table()

@app.route('/')
def index():
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
##№