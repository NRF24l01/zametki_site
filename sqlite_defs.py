import sqlite3
from config import db_name

def get_task_list():
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        tasks_len = cursor.execute("SELECT COUNT(*) FROM zametki").fetchall()[0][0]

        conn.commit()

    except sqlite3.Error as error:
        print("Error26: ", error)

    finally:
        if (conn):
            conn.close()

    for i in range(tasks_len):
        pass


def new_zametka(user_name:str, title:str, text:str):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO 'zametki' (user_name, title, text, state) VALUES ('{user_name}','{title}', '{text}', 'False')")

        conn.commit()
    except sqlite3.Error as error:
        print("Error sql8: ", error)

    finally:
        if conn:
            conn.close()

def login(user_name:str, password:str) -> bool:
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        dt_pass = cursor.execute(f"SELECT pass FROM user WHERE name == '{user_name}'").fetchall()

        conn.commit()

    except sqlite3.Error as error:
        print("Error26: ", error)

    finally:
        if (conn):
            conn.close()

    try:
        bob = dt_pass[0][0]
    except:
        bob = "None"
    #print(user_name, password)
    if bob == "None":
        #print("bobiki")
        new_user(user_name, password)
        return True
    else:
        if password==dt_pass:
            return True
        else:
            return False

def new_user(user_name:str, password:str):
    #print(user_name, password)
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO 'user' (name, pass) VALUES ('{user_name}','{password}')")

        conn.commit()

    except sqlite3.Error as error:
        print("Error26: ", error)

    finally:
        if (conn):
            conn.close()