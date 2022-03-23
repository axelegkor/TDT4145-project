import sqlite3


# User story 3
def best_deal(cursor):
    return cursor.execute("""
        SELECT
        Kaffebrenneri.Navn AS Brennerinavn,
        Kaffe.Navn AS Kaffenavn,
        AVG(Kaffesmaking.Poeng) AS Gjennomsnitt
        
        FROM Kaffe INNER JOIN Kaffesmaking
        ON Kaffe.Id = Kaffesmaking.KaffeId
        INNER JOIN Kaffebrenneri
        ON Kaffe.KaffebrenneriId = Kaffebrenneri.Id
        
        GROUP BY Kaffebrenneri.Navn, Kaffe.Navn
        ORDER BY Gjennomsnitt DESC 
    """)


# User story 4
def filter_descriptions(cursor, key):
    return cursor.execute("""
        SELECT Kaffebrenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn
        
        FROM Kaffe INNER JOIN Kaffesmaking
        ON Kaffe.Id = Kaffesmaking.KaffeId
        INNER JOIN Kaffebrenneri
        ON Kaffe.kaffebrenneriId = Kaffebrenneri.Id
        
        WHERE Kaffe.Beskrivelse LIKE '%{0}%'
        OR Kaffesmaking.Smaksnotater LIKE '%{0}%' 
    """.format(key))


# User story 5
def filter_methods_and_countries(cursor):
    return cursor.execute("""
    
        SELECT Kaffebrenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn

        FROM Kaffebrenneri INNER JOIN Kaffe
        ON Kaffebrenneri.Id = Kaffe.KaffebrenneriId
        INNER JOIN Kaffeparti
        ON Kaffe.KaffepartiId = Kaffeparti.Id
        INNER JOIN Gård
        ON Kaffeparti.GårdId = Gård.Id
        INNER JOIN Region
        ON Gård.RegionId = Region.Id
        INNER JOIN Land
        ON Region.LandId = Land.Id
        INNER JOIN Foredlingsmetode
        ON Kaffeparti.ForedlingsmetodeId = Foredlingsmetode.Id
        
        WHERE (Land.Navn = 'Rwanda' OR Land.Navn = 'Colombia')
        AND Foredlingsmetode.Beskrivelse != 'Vasket'    
    
    """)


def main():
    con = sqlite3.connect("kaffe.db")
    cursor = con.cursor()

    us3 = best_deal(cursor).fetchall()
    print("User story 3:\n", us3, "\n")

    us4 = filter_descriptions(cursor, 'Wow').fetchall()
    print("User story 4:\n", us4, "\n")

    us5 = filter_methods_and_countries(cursor).fetchall()
    print("User story 5:\n", us5, "\n")

    con.close()


if __name__ == '__main__':
    main()
