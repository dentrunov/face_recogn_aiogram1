import sqlite3, time
from datetime import datetime, timedelta

conn = sqlite3.connect('FACES.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS faces(
    userid INT PRIMARY KEY,
    name TEXT);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS attend3(
    att_id INT PRIMARY KEY,
    userid INT,
    date timestamp);
""")
cur.execute('DELETE FROM attend3')
conn.commit()
#определяем время два часа назад
DELTA_TIME = 2
delta = datetime.now - timedelta(hours=DELTA_TIME)
cur.execute('SELECT * FROM attend3 ORDER BY att_id WHERE date=?;', delta)
print(cur.fetchall())

cur.close()
conn.close()