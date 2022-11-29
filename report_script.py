import sqlite3, time
from datetime import datetime, timedelta

conn = sqlite3.connect('FACES.db')
cur = conn.cursor()
#за какое время нужен отчет о пришедших
DELTA_TIME = 2
#определяем разницу во времени с текущего времени
delta = datetime.now() - timedelta(hours=DELTA_TIME)
#делаем выборку
#cur.execute('SELECT * FROM attend3 WHERE date>? AND date <? ORDER BY att_id ;', (delta, datetime.now()))
#print(cur.fetchall())

cur.execute('''SELECT name, date FROM faces
                JOIN attend3 
                WHERE faces.userid = attend3.userid AND
                 date>? AND date <?;''', (delta, datetime.now()))


print(cur.fetchall())

cur.close()
conn.close()