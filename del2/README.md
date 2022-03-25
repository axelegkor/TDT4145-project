# Prosjektoppgave i TDT4145

## Beskrivelser

Applikasjonen startes ved å kjøre python filen `sql.py`. Ved oppstart vil bruker bli spurt om å skrive inn et tall mellom 1 og 5, der tallet tilsvarer hvilken brukerhistorie h*n ønsker å kjøre.

### Brukerhistorie 1
> Input fra bruker:
>   - Epost og passord 	
>   - Kaffebrenneri 	
>   - Kaffenavn 	
>   - Poeng 	
>   - Smaksnotat 	

Brukerhistorie 1 starter ved at du taster inn `1` når programmet starter, som kjører `add_tasting()`. Deretter blir du bedt om å logge inn ved hjelp av _Epost_ og _Passord_. Her har vi antatt at bruker må logge inn med en epost som finnes i databasen, med tilhørende passord. Ved feil passord, avsluttes programmet og en må starte på nytt. Dersom en bruker ikke finnes i databasen fra før, blir brukeren spurt om den vil lage en bruker eller avslutte programmet. Hvis brukeren lager en bruker, skal _Epost_, _Passord_, _Fornavn_ og _Etternavn_ settes inn, og det blir lagt til databasen.

Så blir brukeren bedt om å taste inn navn på kaffebrenneri. Dersom brenneriet ikke eksisterer i databasen, avsluttes programmet, ellers returneres id på kaffebrenneri.

Deretter bes brukeren taste inn kaffenavn. Det sjekkes om den oppgitte kaffen er brent av det oppgitte kaffeberenneriet. Dette gjøres ved en SQL-spørring som forsøker å finne kaffenavnet:
```py
cursor.execute("SELECT Epost from Bruker WHERE Epost = :Epost",
    {"Epost": usr_epost})
result_user_epost = cursor.fetchone()
```
I tillegg sjekkes det om denne verdien er satt. Dersom den ikke er det, avsluttes programmet.

Videre skal bruker oppgi hvor mange poeng den vil gi kaffeen (og det sjekkes at poeng er mellom 1 og 10).

Vi antar også at brukeren ikke skal velge smaksdato selv fordi det er ikke spesifisert som input i brukerhistorien. Derfor blir smaksdato satt til dagens dato ved hjelp av _datetime_-biblioteket i Python, i stedet for at det skal være NULL.

Når alt av input er kommet inn, skal all info settes inn i `Kaffesmaking`-tabellen i databasen ved hjelp av følgende kode:
```py
cursor.execute("INSERT INTO Kaffesmaking VALUES (?,?,?,?,?,?)",
        (new_tasting_id, notes, points, date_tasted, usr_epost, coffee_id))
connection.commit()
```

Riktig id på kaffesmakings finner vi ved å inkrementere største Id-en i `Kaffesmaking`-tabellen. Til slutt vil den opprettede kaffesmakingen til brukeren bli skrevet ut.


### Brukerhistorie 2

Dersom bruker skriver inn `2` ved oppstart vil vår løsning på brukerhistorie 2 kjøre. Dette innebærer å kjøre SQL-spørringen nedenfor gjennom funksjonen `tasted_count()`, som deretter blir skrevet ut i et ryddig format til bruker. Vi bruker `date.today().year` fra _datetime_-biblioteket for å hente året bruker befinner seg i, som er viktig for å filtrere på kaffesmakinger det siste året. Dette kan gjøres ved å sjekke om året (f.eks. _2022_) befinner seg i smaksdatoen til kaffesmakingen med den logiske SQL operatoren `LIKE`, ettersom det kun er årstall som opptrer med fire tall. Videre grupperer vi på eposten til brukere, da dette er primærnøkkel til Bruker-tabellen og vil være unikt for alle brukere. Ved å gjøre dette kan vi telle opp antall rader tilhørende hver gruppe med `COUNT`, for så å sortere resultatet synkende med `ORDER BY _ DESC`.

SQL-spørring:
```SQL
SELECT
Bruker.Fornavn,
Bruker.Etternavn,
COUNT(*) AS Antall

FROM Bruker INNER JOIN Kaffesmaking
ON Bruker.Epost = Kaffesmaking.BrukerEpost

WHERE Kaffesmaking.Smaksdato LIKE '%{date.today().year}%'

GROUP BY Bruker.Epost
ORDER BY Antall DESC
```

### Brukerhistorie 3

Dersom bruker skriver inn `3` ved oppstart vil vår løsning på brukerhistorie 3 kjøre. Dette innebærer å kjøre SQL-spørringen nedenfor gjennom funksjonen `best_deal()`, som deretter blir skrevet ut i et ryddig format til bruker. Vi må gruppere på kaffe sin unike id slik at vi kan regne ut gjennomsnittsscore på kaffen hentet fra alle kaffesmakinger. Vi antar derfor at en kaffe som ikke har kaffesmaking, ikke skal være med i resultatet, og derfor er det noen kaffer som ikke er med, fordi de ikke er smakt av brukere. Når vi til slutt sorterer resultatet er det viktig å ta gjennomsnittet delt på kaffeprisen, da det vil si noe om hvor mye kaffen gir iforhold til prisen, noe brukerhistorien etterspør. `DESC` vil sortere synkende.  

SQL-spørring:
```SQL
SELECT
Kaffebrenneri.Navn AS Brennerinavn,
Kaffe.Navn AS Kaffenavn,
Kaffe.KiloprisNOK AS Pris,
AVG(Kaffesmaking.Poeng) AS Gjennomsnitt

FROM Kaffe INNER JOIN Kaffesmaking
ON Kaffe.Id = Kaffesmaking.KaffeId
INNER JOIN Kaffebrenneri
ON Kaffe.KaffebrenneriId = Kaffebrenneri.Id

GROUP BY Kaffe.Id
ORDER BY Gjennomsnitt / Pris DESC
```

### Brukerhistorie 4
> Input fra bruker:
> - Nøkkel (søkeord)

Brukerhistorie 4 starter man ved å taste inn `4` ved begynnelsen av programmet. Her blir brukeren først bedt om å taste inn et _søkeord_. Vi bruker `SELECT DISTINCT` for å unngå å få likt resultat flere ganger. Deretter slår vi sammen tabellene `Kaffe`, `Kaffesmaking` og `Kaffebrenneri`. Videre filtrerer vi tabellen på om enten Kaffebeskrivelse eller Kaffesmakingsnotater (som er attributter i henholdsvis Kaffe og Kaffesmaking) inneholder det oppgitte søkeordet. Brukeren får da en liste over alle kaffer og hvilket brenneri de er brent av. Dersom ingen kaffer eller kaffesmakinger inneholder søkeordet, printes ingenting ut til bruker.

For å få resultet som er beskrevet i brukerhistorie 4, skriver en «floral» ved input av søkeord. Legg også merke til at koden under er python, og ikke ren SQL.

SQL-spørring:
```py
"""SELECT DISTINCT Kaffebrenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn

FROM Kaffe INNER JOIN Kaffesmaking
ON Kaffe.Id = Kaffesmaking.KaffeId
INNER JOIN Kaffebrenneri
ON Kaffe.kaffebrenneriId = Kaffebrenneri.Id

WHERE Kaffe.Beskrivelse LIKE ?
OR Kaffesmaking.Smaksnotater LIKE ?
""", ["%" + key + "%", "%" + key + "%"]
```

### Brukerhistorie 5
> Input fra bruker: 
> - Fra ett til tre land
> - Fra én til tre foredlingsmetoder

For å kjøre brukerhistorie 5, taster man inn `5` ved begynnelsen av programmet, som kjører `filter_methods_and_countries()`. Først tar programmet inn ett eller tre _land_ som input fra bruker, og deretter én eller tre _foredlingsmetoder_. Vi velger ut brennerinavn og kaffenavn fra `Kaffebrenneri` og `Kaffe`, og starter med å slå sammen tabellene `Kaffebrenneri`, `Kaffe`, `Kaffeparti`, `Gård`, `Region`, `Land` og til slutt `Foredlingsmetode`. Deretter filtrere vi på de ønskede land(ene) som ikke har de/den oppgitte foredingsmetoden(e). Her antar vi skal oppgi kaffer fra de landene som ikke har de oppgitte foredlingsmetodene, altså at det ikke skal være samme kaffe som kommer fra f.eks. Rwanda og Colombia og som ikke har oppgitt foredlingsmetode, men at kaffene kan være forskjellige fra de oppgite landa. Til slutt skrives ut en liste av kaffen og hvilket brenneri det er brent av på et ryddig format. 

For å få resultatet som er beskrevet i brukerhistorie 5, kan en skrive inn "Rwanda" og "Colombia" på land-input og "Vasket" på foredlingsmetoder-input. Legg merke til at koden under er python, og ikke ren SQL.

SQL-spørring:
```py
"""
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

WHERE (Land.Navn = ? OR Land.Navn = ? OR Land.Navn = ?)
AND Foredlingsmetode.Navn != ? AND Foredlingsmetode.Navn != ? AND Foredlingsmetode.Navn != ?
""", (country1, country2, country3, method1, method2, method3)
```

## Resultater

### Resultat fra brukerhistorie 1
Her taster en inn slik som vist på bildet, og til slutt printes det som ble lagt til:

![Brukerhistorie 1](./resultat_bilder/brukerhistorie1.png)

### Resultat fra brukerhistorie 2 
Her kjører en python-koden og trykker `2`. Slik ser resultatet ut:

![Bukerhistorie 2](./resultat_bilder/brukerhistorie2.png)

### Resultat fra brukerhistorie 3
For brukerhistorie 3 tenger du også å bare taste inn `3` ved oppstart av programmet. Her er resultat for brukerhistorie 3:

![Brukerhistorie 3](./resultat_bilder/brukerhistorie3.png)

### Resultat fra brukerhistorie 4
Slik det er beskrevet i oppgavebeskrivelsen, vil brukeren taste inn søkerdet "floral" (men programmet kan ta inn hvilket som helst søkeord). Slik vil det se ut med input og output: 

![Resultat fra brukerhistorie 4](./resultat_bilder/brukerhistorie4.png)

### Resultat fra brukerhistorie 5
I oppgaveteskten øsnker brukeren å finne kaffer som ikke er vasket (foredlingsmetode) og som kommer fra Rwanda og Colombia. Etter å taste inn `5` ved oppstart, taster man inn landene "Rwanda" og "Colombia", og "Vasket" på foredlingsmetode:

![Resultat fra brukerhistorie 5](./resultat_bilder/brukerhistorie5.png)