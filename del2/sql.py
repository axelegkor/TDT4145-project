import sqlite3

def main():
    con = sqlite3.connect("kaffe.db")

    cursor = con.cursor()

    # Executions
    cursor.execute("SELECT Bruker.Fornavn FROM Bruker")

    con.close()

if __name__ == '__main__':
    main()
