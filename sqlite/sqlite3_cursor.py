import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('SHOW TABLES')

for t in c:
    print(t)


conn.commit()
conn.close()
