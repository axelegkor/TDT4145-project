from asyncio.windows_events import NULL
import sqlite3


# User story 2
def tasted_count(cursor):
    return cursor.execute("""
        SELECT
        Bruker.Fornavn,
        Bruker.Etternavn,
        COUNT(*) AS Antall

        FROM Bruker INNER JOIN Kaffesmaking
        ON Bruker.Epost = Kaffesmaking.BrukerEpost
        
        GROUP BY Bruker.Fornavn, Bruker.Etternavn
        ORDER BY Antall DESC""")


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
def filter_methods_and_countries(cursor, country1, country2, country3, method1, method2, method3):
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
        
        WHERE (Land.Navn LIKE '{0}' OR Land.Navn LIKE '{1}' OR Land.Navn LIKE '{2}')
        AND Foredlingsmetode.Navn NOT LIKE '{3}' AND Foredlingsmetode.Navn NOT LIKE '{4}' AND Foredlingsmetode.Navn NOT LIKE '{5}'
        
    
    """.format(country1, country2, country3, method1, method2, method3))
    # AND (Foredlingsmetode.Beskrivelse!=%s AND Foredlingsmetode.Beskrivelse!=%s AND Foredlingsmetode.Beskrivelse!=%s)


def main():

    con = sqlite3.connect("kaffe.db")
    cursor = con.cursor()

    print("""Velg mellom en av følgende handlinger:\n
    1. Legg til en kaffesmaking i databasen\n
    2. Se hvor mange unike kaffer hver bruker har smakt\n
    3. Se de ulike kaffenes pris og poeng, sortert etter hvilke kaffer som gir best verdi for pengene\n
    4. Søk etter kaffer ved søkeord\n
    5. Søk etter kaffer ved ønskede land og uønskede foredlingsmetoder
    """)
    choice = int(input("Velg et tall: "))
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
            print(i[1], "brent av", i[0] + ":", i[2], "NOK,", i[3], "poeng")

    elif choice == 4:
        key = input("Søk: ")
        us4 = filter_descriptions(cursor, key).fetchall()
        for i in us4:
            print(i[1], "brent av", i[0])

    elif choice == 5:
        countries = input(
            "Velg opp til tre land å inkludere (på formatet: Land1, Land2, Land3): ")
        methodexcluded = input(
            "Velg opp til tre foredlingsmetoder å ekskludere (på formatet: Metode1, Metode2, Metode3): ")
        countriesList = countries.split(", ")
        for i in range(3-len(countriesList)):
            countriesList.append(NULL)

        methodexcludedList = methodexcluded.split(", ")
        for i in range(3-len(methodexcludedList)):
            methodexcludedList.append(NULL)

        us5 = filter_methods_and_countries(
            cursor, countriesList[0], countriesList[1], countriesList[2], methodexcludedList[0], methodexcludedList[1], methodexcludedList[2]).fetchall()
        for i in us5:
            print(i[1], "brent av", i[0])

    con.close()


if __name__ == '__main__':
    main()
