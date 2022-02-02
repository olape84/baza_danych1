# `ex_01_conection_to_db.py`

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to a SQLite database """
   conn = None #dlaczego tu jest 'None'? 
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()

def create_connection_in_memory():
   """ create a database connection to a SQLite database """
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()

if __name__ == '__main__':
   create_connection(r"database.db") #r od 'raw'? dlaczego tak?
   create_connection_in_memory()

def execute_sql(conn, sql): #dobrze rozumiem, że w parametrze sql wpisuję dowolne query sqlowe? 
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_projekt(conn, projekt):
   """
   Create a new projekt into the projects table
   :param conn:
   :param projekt:
   :return: projekt id
   """
   sql = '''INSERT INTO projects(nazwa, start_date, end_date) 
             VALUES(?,?,?)''' #ten 'sql' jest podany by po każdym uruchomieniu funkcji dodawał dane wg tego samego schematu? 
   cur = conn.cursor() #tu wyskakuje błąd:  AttributeError: 'NoneType' object has no attribute 'cursor'
   cur.execute(sql, projekt)
   conn.commit()
   return cur.lastrowid

conn = create_connection("database.db")
projekt = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00") #czy to nie powinno się nazywać sql values?
pr_id = add_projekt(conn, projekt)

def select_zadanie_by_status(conn, status):
   """
   Query tasks by priority
   :param conn: the Connection object
   :param status:
   :return:
   """
   cur = conn.cursor()
   cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

   rows = cur.fetchall()
   return rows


def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query): #nie rozumiem co ma do tego słownik?
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = [] #nie powinny tu być {}? inaczej to jest lista nie słownik
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):
   """
   update status, begin_date, and end date of a task
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)           #tu nie wiem o co chodzi
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete(conn, table):
   """
   delete table 
   :param conn:
   :param table: table name
   :return:
   """

   sql = f''' delete from {table}
        '''
   try:
       cur = conn.cursor()
       cur.execute(sql)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

if __name__ == "__main__":
   conn = create_connection("database.db")
   update(conn, "tasks", 2, status="started")
   update(conn, "tasks", 2, stat="started")
   conn.close()

#jak użyć tych funkcji żeby zmienić aplikację todo? ja bym zmieniła models na ten plik. 