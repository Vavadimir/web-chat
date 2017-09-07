import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''SELECT * FROM COMMS''')
cm = c.fetchall()
print(cm)
for row in c.execute('''SELECT * FROM USERS'''):
    print(row)


conn.commit()
conn.close()