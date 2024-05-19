import sqlite3

conn = sqlite3.connect('quizapp.db')

cursor = conn.cursor()



cursor.execute("SELECT rowid, * FROM quiz_tbl")
users = cursor.fetchall()
for user in users:
    print(user)

conn.commit()
conn.close()