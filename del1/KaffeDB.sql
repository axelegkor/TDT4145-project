BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Bruker" (
	"Epost"	TEXT,
	"Fornavn"	TEXT NOT NULL,
	"Etternavn"	TEXT NOT NULL,
	"Passord"	TEXT NOT NULL,
	PRIMARY KEY("Epost")
);
CREATE TABLE IF NOT EXISTS "Kaffebrenneri" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Land" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Region" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"LandId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("LandId") REFERENCES "Land"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Gård" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"Høyde"	REAL NOT NULL,
	"RegionId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("RegionId") REFERENCES "Region"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Foredlingsmetode" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"Beskrivelse"	TEXT,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Kaffeparti" (
	"Id"	INTEGER,
	"Innhøstingsår"	INTEGER NOT NULL,
	"KiloprisUSD"	REAL NOT NULL,
	"GårdId"	INTEGER NOT NULL,
	"ForedlingsmetodeId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("GårdId") REFERENCES "Gård"("Id") ON DELETE CASCADE,
	FOREIGN KEY("ForedlingsmetodeId") REFERENCES "Foredlingsmetode"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Kaffesmaking" (
	"Id"	INTEGER,
	"Smaksnotater"	TEXT NOT NULL,
	"Poeng"	INTEGER NOT NULL,
	"Smaksdato"	TEXT NOT NULL,
	"BrukerEpost"	TEXT NOT NULL,
	"KaffeId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("BrukerEpost") REFERENCES "Bruker"("Epost") ON DELETE CASCADE,
	FOREIGN KEY("KaffeId") REFERENCES "Kaffe"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Art" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Kaffebønne" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"ArtId"	INTEGER,
	"GårdId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("ArtId") REFERENCES "Art"("Id") ON DELETE CASCADE,
	FOREIGN KEY("GårdId") REFERENCES "Gård"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "PartiBestårAv" (
	"KaffebønneId"	INTEGER,
	"KaffepartiId"	INTEGER,
	PRIMARY KEY("KaffebønneId","KaffepartiId"),
	FOREIGN KEY("KaffebønneId") REFERENCES "Kaffebønne"("Id") ON DELETE CASCADE,
	FOREIGN KEY("KaffepartiId") REFERENCES "Kaffeparti"("Id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Kaffe" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"Beskrivelse"	TEXT,
	"KiloprisNOK"	NUMERIC NOT NULL,
	"Brenningsgrad"	TEXT NOT NULL,
	"Dato"	TEXT NOT NULL,
	"KaffepartiId"	INTEGER NOT NULL,
	"KaffebrenneriId"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("KaffebrenneriId") REFERENCES "Kaffebrenneri"("Id") ON DELETE CASCADE,
	FOREIGN KEY("KaffepartiId") REFERENCES "Kaffeparti"("Id") ON DELETE CASCADE
);
COMMIT;
