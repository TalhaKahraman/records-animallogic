import sqlite3
import os

def create_connection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS records")
    sql ='''CREATE TABLE records(
    id integer primary key autoincrement,
    name CHAR(50),
    address CHAR(60),
    phone_number INT
    )'''
    cursor.execute(sql)
    print("Table created successfully........")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    records_db_file = os.path.dirname(os.path.abspath(__file__)) + '/records.db'
    conn = create_connection(records_db_file)
    create_table(conn)