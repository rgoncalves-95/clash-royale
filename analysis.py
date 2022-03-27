import sqlite3
import pandas as pd

# Create connection
db = sqlite3.connect('db\database.db')

# Query records
df = pd.read_sql_query("""SELECT * 
                          FROM daily_records AS d
                          LEFT JOIN cards_info AS c ON d.card_id = c.id"""
                       , db)

df2 = pd.read_sql_query("""WITH common_cards AS (
                          SELECT id, name
                          FROM cards_info
                          WHERE maxLevel == 14)
                          
                          SELECT name, date, count, player_id
                          FROM daily_records AS d
                          INNER JOIN common_cards AS c ON d.card_id = c.id"""
                        , db)

df3 = pd.read_sql_query("""SELECT * 
                           FROM battle_log"""
                        , db)

# Close connection
db.close()
