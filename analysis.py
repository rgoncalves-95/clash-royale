import sqlite3
import pandas as pd

# Create connection
db = sqlite3.connect('db\database.db')

# Query records
df = pd.read_sql_query("""SELECT * 
                          FROM daily_records AS d
                          LEFT JOIN cards_info AS c ON d.card_id = c.id"""
                       , db)


prueba = pd.read_sql_query("""SELECT date,
                            card_id,
                            name,
                            count,
                            LAG(count, 1) OVER (PARTITION BY card_id, player_id ORDER BY date) AS lag,
                            player_id  
                     FROM daily_records AS d
                     LEFT JOIN cards_info AS c ON d.card_id = c.id
                     ORDER BY player_id, card_id, date"""
                  , db)

prueba = pd.read_sql_query("""SELECT date,
                            card_id,
                            name,
                            (count - lag) AS change,
                            SUM(count - lag) OVER (PARTITION BY card_id, player_id ORDER BY date) AS cumsum,
                            player_id
                     FROM (SELECT date,
                                  card_id,
                                  name,
                                  count,
                                  LAG(count, 1) OVER (PARTITION BY card_id, player_id ORDER BY date) AS lag,
                                  player_id  
                           FROM daily_records AS d
                           LEFT JOIN cards_info AS c ON d.card_id = c.id
                           ORDER BY player_id, card_id, date)
                           WHERE lag IS NOT NULL"""
                  , db)


df2 = pd.read_sql_query("""WITH common_cards AS (
                          SELECT id, name
                          FROM cards_info
                          WHERE maxLevel == 14)
                          
                          SELECT name, date, count, player_id
                          FROM daily_records AS d
                          INNER JOIN common_cards AS c ON d.card_id = c.id"""
                        , db)

matches_per_day = pd.read_sql_query("""SELECT date,
                                              matches,
                                              AVG(matches) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS three_day_mean
                                       FROM (SELECT battleTime AS date,
                                                    COUNT(*) AS matches
                                             FROM battle_log
                                             GROUP BY battleTime)"""
                                    , db)

matches_per_day['date'] = pd.to_datetime(matches_per_day['date'], format='%Y-%m-%d')

# Close connection
db.close()
