import sqlite3
from sqlite3 import Error
import requests
import json
import sqlite3
from datetime import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_daily_user_entry(conn, card_info):
    """
    Create a new project into the projects table
    :param conn:
    :param card_info:
    :return: project id
    """
    sql = ''' INSERT INTO daily_records(card_id,level,count,date,player_id) 
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, card_info)
    conn.commit()
    return cur.lastrowid


def request_info(player_id, api_key):
    headers = {"Authorization": "Bearer " + api_key}
    response = requests.get("https://api.clashroyale.com/v1/players/" + player_id, headers=headers)
    cards = response.json()['cards']
    return cards


def insert_records(cards_info, player_id, conn):
    date = datetime.today().strftime('%Y-%m-%d')

    for record in enumerate(cards_info):
        card_entry = (
            record[1]['id'], record[1]['level'], record[1]['count'], date, player_id)
        card_entry_id = create_daily_user_entry(conn, card_entry)


def main():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdjNmNkNzdjLWM4Y2MtNDM3Yy05ZTgxLTdjNDVmYThhNDVhNCIsImlhdCI6MTY0ODE0ODY3Niwic3ViIjoiZGV2ZWxvcGVyLzYyZjc2NTY2LWZjZDUtY2UxMy03Y2Y5LWNlMjQ3OWZhZGNmNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3OS4xNTMuMTY3LjIxOSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.gzyKON_4Kd1XCvzXhZ_A6dLEu6Gl8qDrE7u5FFUo-AaIKWjGS1VP-Lt4jwOcdU3huVDYAyiBXgICiF8GXBjPiQ"
    database = r"db\database.db"
    player_ids = ["%2392RP8QQL", "%2398V2CR9R2", "%23Y9PVYGCUG", "%23QQGLRVULP", "%2328PJVCQLJ"]

    # create a database connection
    conn = create_connection(database)
    for player in player_ids:
        cards_info = request_info(player_id=player, api_key=api_key)
        insert_records(cards_info=cards_info, player_id=player, conn=conn)

    conn.close()


if __name__ == '__main__':
    main()
