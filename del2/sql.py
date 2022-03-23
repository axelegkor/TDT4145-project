import sqlite3


# User story 2
def tasted_count(cursor):
    return cursor.execute("""
        SELECT
        Bruker.Fornavn,
        Bruker.Etternavn,
        COUNT(*) AS TasteCount

        FROM Bruker INNER JOIN Kaffesmaking
        ON Bruker.Epost = Kaffesmaking.BrukerEpost
        
        GROUP BY Bruker.Fornavn, Bruker.Etternavn
        ORDER BY TasteCount DESC""")


# User story 3
def best_deal(cursor):
    return cursor.execute("""
        SELECT
        Kaffebrenneri.Navn AS Brennerinavn,
        Kaffe.Navn AS Kaffenavn,
        Kaffe.KiloprisNOK AS Pris,
        AVG(Kaffesmaking.Poeng) AS Gjennomsnitt
        
        FROM Kaffe INNER JOIN Kaffesmaking
        ON Kaffe.Id = Kaffesmaking.KaffeId
        INNER JOIN Kaffebrenneri
        ON Kaffe.KaffebrenneriId = Kaffebrenneri.Id
        
        GROUP BY Kaffebrenneri.Navn, Kaffe.Navn
        ORDER BY Gjennomsnitt/Pris DESC 
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

    choice = int(input("Choose a number: "))
    print()

    if choice == 1:
        print("Run 1")

    elif choice == 2:
        us2 = tasted_count(cursor).fetchall()
        for i in us2:
            print(i[0], i[1] + ":", str(i[2]))

    elif choice == 3:
        us3 = best_deal(cursor).fetchall()
        for i in us3:
            print(i[1], "burnt at", i[0] + ":", i[2], "NOK,", i[3], "points")

    elif choice == 4:
        us4 = filter_descriptions(cursor, 'floral').fetchall()
        for i in us4:
            print(i[1], "burnt at", i[0])

    elif choice == 5:
        us5 = filter_methods_and_countries(cursor).fetchall()
        for i in us5:
            print(i[1], "burnt at", i[0])

    con.close()


if __name__ == '__main__':
    main()
