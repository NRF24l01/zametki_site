import sqlite3
from config import db_name

def get_task_list(user_name:str):
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
    tasks_len = int(tasks_len) + 1
    result = []
    for i in range(1, tasks_len):
        #print(i, tasks_len)
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            username = cursor.execute(f"SELECT user_name FROM zametki WHERE id == '{i}'").fetchall()[0][0]

            conn.commit()

        except sqlite3.Error as error:
            print("Error26: ", error)

        finally:
            if (conn):
                conn.close()
        if username == user_name:
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                list_with = cursor.execute(f"SELECT title, text, state, del FROM zametki WHERE id == '{i}'").fetchall()[0]
                conn.commit()

            except sqlite3.Error as error:
                print("Error26: ", error)

            finally:
                if (conn):
                    conn.close()
            deli = bool(list_with[3])
            if deli:
                ne_hlam = {}
                ne_hlam["name"] = list_with[0]
                ne_hlam["description"] = list_with[1]
                ne_hlam["is_done"] = booling(list_with[2])
                result.append(ne_hlam)
    return result


def new_zametka(user_name:str, title:str, text:str):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO 'zametki' (user_name, title, text, state, del) VALUES ('{user_name}','{title}', '{text}', 'False', 'False')")

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

def booling(strg:str):
    if strg == "True" or strg == "1":
        res = True
    elif strg == "False" or strg == "0":
        res = False
    else:
        raise TypeError
    return res