import sqlite3

con =sqlite3.connect("C:\\Users\\keoca\\Desktop\\TWP3\\History\\Default\\History")

cur = con.cursor()

res = cur.execute("SELECT url FROM urls")
print(res.fetchall())