import sqlite3
con = sqlite3.connect("kaffe.db")

cursor = con.cursor()

# Executions
cursor.execute("SELECT Bruker.Fornavn FROM Bruker")


con.close()
