import sqlite3
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def app_db():
    conection = sqlite3.connect('app.db')
    cursor = conection.cursor() #указатель
    #execute - выполнение sql-выражения; fetchmany() - получение данных (указать чило); commit - сохранение
    # text - не имеет определённой длины, varchar - органиченная длина
    # команда - название таблицы - поля

    cursor.execute("""create table if not exists users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(20) UNIQUE NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARSHAR(60) NOT NULL, 
        register_date text not null)""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id integer primary key,
        user_id integer not null,
        title varchar(30) not null,
        content text,
        start_date date default CURRENT_DATE,
        end_date text,
        status boolean default 0)""")

    cursor.execute('select * from users')
    print(cursor.fetchall())
    cursor.execute('select * from tasks')
    print(cursor.fetchall())

    conection.commit()
    conection.close()


def add_user(name, email, password):
    date = datetime.date.today().isoformat()
    password = generate_password_hash(password)    
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""insert into users
        (name, email, password, register_date)
        values (?,?,?,?)""", [name, email, password, date])
        cursor.execute('select * from users')
        print(cursor.fetchall())
        connection.commit()


def login_user(email, password):
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute(""" select * from users 
        where email=?""", 
        [email])
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            return user
        return False


def get_user_id(name):
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""select * from users
        where name=?""", [name])
        user_id = cursor.fetchone()[0]
        print(user_id)
        return user_id


def add_task(user_id, title, content, end_date):
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""insert into tasks
        (user_id, title, content, end_date)
        values (?,?,?,?)""", [user_id, title, content, end_date])
        cursor.execute('select * from tasks')
        print(cursor.fetchall())
        connection.commit()


def get_tasks(name):
    user_id = get_user_id(name)
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""select * from tasks
        where user_id=?""", [user_id])
        user_tasks = cursor.fetchall()
        print(user_tasks)
        return user_tasks

        
def delete_task(username, id):
    user_tasks = get_tasks(username)
    task_id = user_tasks[int(id)-1][0]
    with sqlite3.connect('app.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""delete from tasks where id = ?""", [task_id])
        connection.commit()


        

        


# app_db()
# add_user('test1', 'test@test3.com', '123456')


# cursor.execute("""insert into users(name, email, password, register_date)
#     values ('test 1', 'test1@test.com', '123123', '20.01.20')""") 

# cursor.execute("""insert into tasks(user_id, title, content, end_date) 
#     values (1, 'repair your watches', 'immediatly', '2020-02-01')""")