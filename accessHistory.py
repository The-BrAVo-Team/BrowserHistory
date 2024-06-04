import sqlite3

con =sqlite3.connect("C:\\Users\\keoca\\Desktop\\TWP3\\TestUser\\Default\\History")

cur = con.cursor()

res = cur.execute("SELECT url FROM urls ORDER BY last_visit_time")
print(res.fetchall())