import sqlite3
from sqlite3 import Error
import requests
import json


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_entries(conn, card_info):
    """
    Create a new project into the projects table
    :param conn:
    :param card_info:
    :return: project id
    """
    sql = ''' INSERT INTO cards_info(id,name,maxLevel) 
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, card_info)
    conn.commit()
    return cur.lastrowid


def request_info(api_key):
    headers = {"Authorization": "Bearer " + api_key}
    response = requests.get("https://api.clashroyale.com/v1/cards", headers=headers)
    cards = response.json()['items']
    return cards


def insert_records(cards_info, conn):
    for record in enumerate(cards_info):
        card_entry = (
            record[1]['id'], record[1]['name'], record[1]['maxLevel'])
        card_entry_id = create_entries(conn, card_entry)


def main():
    database = r"db\database.db"
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdjNmNkNzdjLWM4Y2MtNDM3Yy05ZTgxLTdjNDVmYThhNDVhNCIsImlhdCI6MTY0ODE0ODY3Niwic3ViIjoiZGV2ZWxvcGVyLzYyZjc2NTY2LWZjZDUtY2UxMy03Y2Y5LWNlMjQ3OWZhZGNmNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3OS4xNTMuMTY3LjIxOSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.gzyKON_4Kd1XCvzXhZ_A6dLEu6Gl8qDrE7u5FFUo-AaIKWjGS1VP-Lt4jwOcdU3huVDYAyiBXgICiF8GXBjPiQ"

    sql_create_daily_records_table = """CREATE TABLE IF NOT EXISTS daily_records (
                                        id integer PRIMARY KEY,
                                        card_id integer NOT NULL,
                                        level integer NOT NULL,
                                        count integer NOT NULL,
                                        date text NOT NULL,
                                        player_id text NOT NULL
                                    );"""

    sql_create_cards_info_table = """CREATE TABLE IF NOT EXISTS cards_info (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        maxLevel integer NOT NULL
                                    );"""

    sql_create_battle_log_table = """CREATE TABLE IF NOT EXISTS battle_log (
                                        id integer PRIMARY KEY,
                                        type text NOT NULL,
                                        battleTime text NOT NULL,
                                        isLadderTournament text NOT NULL,
                                        player_id text NOT NULL
                                    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create cards table
        create_table(conn, sql_create_daily_records_table)
        create_table(conn, sql_create_cards_info_table)
        create_table(conn, sql_create_battle_log_table)
    else:
        print("Error! cannot create the database connection.")

    # Add data to the cards table
    cards_info = request_info(api_key=api_key)
    insert_records(cards_info=cards_info, conn=conn)

    conn.close()


if __name__ == '__main__':
    main()
