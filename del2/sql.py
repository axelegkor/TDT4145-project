#from asyncio.windows_events import NULL
from datetime import date
import sqlite3
import os


def add_tasting(connection, cursor):
    """User story 1

    :param cursor
    :return
    """

    # Login info
    usr_epost = input("Hva er eposten din? ")
    usr_pw = input("Hva er passordet ditt? ")

    # Handle if user does not exist
    cursor.execute("SELECT Epost from Bruker WHERE Epost = :Epost", {
                   "Epost": usr_epost})
    result_user_epost = cursor.fetchone()

    # Validate user
    if result_user_epost:
        cursor.execute("SELECT Passord FROM Bruker WHERE Epost = :Epost AND Passord = :Passord",
                       {"Epost": usr_epost, "Passord": usr_pw})
        pw = cursor.fetchone()

        # Validate password
        if not pw:
            print("Ugyldig passord.")
            return

        print("Gyldig bruker.\n")
    else:
        print("Fant ingen bruker med denne e-mailen i databasen.")
        make_new_user = input("Ønsker du å lage en ny bruker? (J/N) ")

        if make_new_user == "J":
            first_name = input("Hva er fornavnet ditt? ")
            surname = input("Hva er etternavnet ditt? ")
            new_pw = input("Oppgi et passord: ")
            cursor.execute("INSERT INTO Bruker VALUES (?,?,?,?)",
                           (usr_epost, first_name, surname, new_pw))
            connection.commit()

            cursor.execute("SELECT * FROM Bruker WHERE Epost = :Epost",
                           {"Epost": usr_epost})
            new_usr = cursor.fetchone()
            print("Denne brukeren er nå lagt til databasen: " + str(new_usr) + "\n")
        else:
            return

    roastery = input("Hva er navnet på brenneriet? ")

    # Validate and get Id of roastery
    cursor.execute("SELECT Id FROM Kaffebrenneri WHERE Navn = :Kaffebrenneri_navn",
                   {"Kaffebrenneri_navn": roastery})
    result_roastery = cursor.fetchone()

    if result_roastery:
        roastery_id = result_roastery[0]
        print(roastery + " er gyldig.\n")
    else:
        print(roastery + " eksisterer ikke i databasen.")
        return

    coffee_name = input("Hva er navnet på kaffen? ")

    # Find coffee_ID based on roastery
    cursor.execute("SELECT Id FROM Kaffe WHERE Navn = :Kaffe_Navn AND Kaffebrenneriid = :Kaffebrenneri",
                   {"Kaffe_Navn": coffee_name, "Kaffebrenneri": roastery_id})
    result_coffee_name = cursor.fetchone()

    if result_coffee_name:
        coffee_id = result_coffee_name[0]
        print(coffee_name + " er gyldig.\n")
    else:
        print(
            "Kaffenavn eksisterer ikke i databasen eller kaffebrenneriId stemmer ikke overens med kaffenavn.\n")
        return

    points = int(input("Hvor mange poeng vil du gi kaffen? "))

    # Validate points, has to be int: 1-10
    if 10 < points < 1:
        print("Poeng må være mellom 1 og 10.")
        return

    notes = input("Kaffenotater: ")
    if not notes:
        print("Du må oppgi kaffenotater.\n")
        return

    # Sets the tasting date to today
    date_tasted = date.today().strftime("%d.%m.%Y")

    cursor.execute("SELECT MAX(Id) FROM Kaffesmaking")
    new_tasting_id = cursor.fetchone()[0] + 1

    cursor.execute(
        "INSERT INTO Kaffesmaking VALUES (?,?,?,?,?,?)",
        (new_tasting_id, notes, points, date_tasted, usr_epost, coffee_id))
    connection.commit()

    # Print last added element
    cursor.execute("SELECT * FROM Kaffesmaking")
    last_added = cursor.fetchall()
    print("Denne smakingen er lagt til i databasen:", last_added[-1])



def tasted_count(cursor):
    """User story 2

    :param cursor
    :return
    """
    return cursor.execute(f"""
        SELECT
        Bruker.Fornavn,
        Bruker.Etternavn,
        COUNT(*) AS Antall

        FROM Bruker INNER JOIN Kaffesmaking
        ON Bruker.Epost = Kaffesmaking.BrukerEpost

        WHERE Kaffesmaking.Smaksdato LIKE '%{date.today().year}%'
        
        GROUP BY Bruker.Epost
        ORDER BY Antall DESC
    """)


def best_deal(cursor):
    """User story 3

    :param cursor
    :return
    """
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


def filter_descriptions(cursor, key):
    """User story 4

    :param cursor
    :return
    """
    return cursor.execute("""
        SELECT DISTINCT Kaffebrenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn
        
        FROM Kaffe INNER JOIN Kaffesmaking
        ON Kaffe.Id = Kaffesmaking.KaffeId
        INNER JOIN Kaffebrenneri
        ON Kaffe.kaffebrenneriId = Kaffebrenneri.Id
        
        WHERE Kaffe.Beskrivelse LIKE '%{0}%'
        OR Kaffesmaking.Smaksnotater LIKE '%{0}%'
    """.format(key))


def filter_methods_and_countries(cursor, country1, country2, country3, method1, method2, method3):
    """User story 5

    :param cursor
    :return
    """
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

def main():

    con = sqlite3.connect(f"{os.getcwd()}/kaffe.db")
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
        add_tasting(con, cursor)

    elif choice == 2:
        us2 = tasted_count(cursor).fetchall()
        for i in us2:
            print(i[0], i[1] + ":", str(i[2]))

    elif choice == 3:
        us3 = best_deal(cursor).fetchall()
        for i in us3:
            print(i[1], "brent av", i[0] + ":", i[2], "NOK,", i[3], "poeng")

    elif choice == 4:
        key = input("Hvilket ord ønsker du å søke etter? ")
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
            countriesList.append(None)

        methodexcludedList = methodexcluded.split(", ")
        for i in range(3-len(methodexcludedList)):
            methodexcludedList.append(None)

        us5 = filter_methods_and_countries(
            cursor, countriesList[0], countriesList[1], countriesList[2], methodexcludedList[0], methodexcludedList[1], methodexcludedList[2]).fetchall()
        for i in us5:
            print(i[1], "brent av", i[0])

    con.close()


if __name__ == '__main__':
    main()
