import sqlite3
import pandas as pd

# Create connection
db = sqlite3.connect('db\database.db')

# Query records
df = pd.read_sql_query("""SELECT * 
                          FROM daily_records AS d
                          LEFT JOIN cards_info AS c ON d.card_id = c.id"""
                       , db)

# Close connection
db.close()
