# Prosjektoppgave i TDT4145


## Konvensjoner

:TODO: skriv om sql konvensjoner 

## Beskrivelser

Applikasjonen startes ved å kjøre python filen `sql.py`. Ved oppstart vil bruker bli spurt om å skrive inn et tall mellom 1 og 5, der tallet tilsvarer hvilken brukerhistorie h*n ønsker å kjøre.

### Brukerhistorie 1



### Brukerhistorie 2

Dersom bruker skriver inn `2` ved oppstart vil vår løsning på brukerhistorie 2 kjøre. Dette innebærer å kjøre SQL-spørringen nedenfor gjennom funksjonen `tasted_count()`, som deretter blir skrevet ut i et ryddig format til bruker. Vi bruker `date.today().year` fra _datetime_-biblioteket for å hente året bruker befinner seg i, som er viktig for å filtrere på kaffesmakinger det siste året. Dette kan gjøres ved å sjekke om året (f.eks. _2022_) befinner seg i smaksdatoen til kaffesmakingen med den logiske SQL operatoren `LIKE`, ettersom det kun er årstall som opptrer med fire tall. Videre grupperer vi på eposten til brukere, da dette er primærnøkkel til Bruker-tabellen og vil være unikt for alle brukere. Ved å gjøre dette kan vi telle opp antall rader tilhørende hver gruppe med `COUNT`, for så å sortere resultatet synkende med `ORDER BY _ DESC`.

### Brukerhistorie 3

Dersom bruker skriver inn `3` ved oppstart vil vår løsning på brukerhistorie 3 kjøre. Dette innebærer å kjøre SQL-spørringen nedenfor gjennom funksjonen `best_deal()`, som deretter blir skrevet ut i et ryddig format til bruker.

### Brukerhistorie 4



### Brukerhistorie 5


## Resultater

### Brukerhistorie 1



### Brukerhistorie 2



### Brukerhistorie 3



### Brukerhistorie 4



### Brukerhistorie 5
