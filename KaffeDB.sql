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
	FOREIGN KEY("LandId") REFERENCES "Land"("Id") ON DELETE CASCADE,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Gård" (
	"Id"	INTEGER,
	"Navn"	TEXT NOT NULL,
	"Høyde"	REAL NOT NULL,
	"RegionId"	INTEGER NOT NULL,
	FOREIGN KEY("RegionId") REFERENCES "Region"("Id") ON DELETE CASCADE,
	PRIMARY KEY("Id")
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
	FOREIGN KEY("GårdId") REFERENCES "Gård"("Id") ON DELETE CASCADE,
	FOREIGN KEY("ForedlingsmetodeId") REFERENCES "Foredlingsmetode"("Id") ON DELETE CASCADE,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "Kaffesmaking" (
	"Id"	INTEGER,
	"Smaksnotater"	TEXT NOT NULL,
	"Poeng"	INTEGER NOT NULL,
	"Smaksdato"	TEXT NOT NULL,
	"BrukerEpost"	TEXT NOT NULL,
	"KaffeId"	INTEGER NOT NULL,
	FOREIGN KEY("BrukerEpost") REFERENCES "Bruker"("Epost") ON DELETE CASCADE,
	FOREIGN KEY("KaffeId") REFERENCES "Kaffe"("Id") ON DELETE CASCADE,
	PRIMARY KEY("Id")
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
INSERT INTO "Bruker" VALUES ('ivarnak@stud.ntnu.no','Ivar','Nakken','ivar321');
INSERT INTO "Bruker" VALUES ('mariohar@stud.ntnu.no','Mario','Haroun','mario123');
INSERT INTO "Bruker" VALUES ('axelle@stud.ntnu.no','Axel','Legallais-Korsbakken','axelpassord');
INSERT INTO "Kaffebrenneri" VALUES (1,'Jacobsen & Svart (Trondheims-brenneriet)');
INSERT INTO "Kaffebrenneri" VALUES (2,'Kaffe AS');
INSERT INTO "Kaffebrenneri" VALUES (3,'Kjeldsberg Kaffebrenneri');
INSERT INTO "Land" VALUES (1,'El Salvador');
INSERT INTO "Land" VALUES (2,'Colombia');
INSERT INTO "Land" VALUES (3,'Rwanda');
INSERT INTO "Land" VALUES (4,'Brasil');
INSERT INTO "Region" VALUES (1,'Santa Ana',1);
INSERT INTO "Region" VALUES (2,'Andes',2);
INSERT INTO "Region" VALUES (3,'Gakenke',3);
INSERT INTO "Region" VALUES (4,'Vala de Grama',4);
INSERT INTO "Region" VALUES (5,'Cerrado Mineiro',4);
INSERT INTO "Gård" VALUES (1,'Nombre de Dios',1500.0,1);
INSERT INTO "Gård" VALUES (2,'Finca La Despensa',1421.0,2);
INSERT INTO "Gård" VALUES (3,'Tuzamure Kawa Muyongwe',1644.0,3);
INSERT INTO "Gård" VALUES (4,'Fazenda Maravilhosa',997.0,5);
INSERT INTO "Gård" VALUES (5,'Fazenda de Qualidade',1142.0,5);
INSERT INTO "Foredlingsmetode" VALUES (1,'Bærtørket','Tørket i solen');
INSERT INTO "Foredlingsmetode" VALUES (2,'Vasket','Vasket godt med mye vann');
INSERT INTO "Kaffeparti" VALUES (1,2021,8.0,1,1);
INSERT INTO "Kaffeparti" VALUES (2,2019,6.0,2,2);
INSERT INTO "Kaffeparti" VALUES (3,2017,9.0,3,1);
INSERT INTO "Kaffesmaking" VALUES (1,'Wow – en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!',10,'09.01.2022','ivarnak@stud.ntnu.no',1);
INSERT INTO "Kaffesmaking" VALUES (2,'For en kaffe!!',9,'25.03.2022','mariohar@stud.ntnu.no',1);
INSERT INTO "Art" VALUES (1,'C. arabica');
INSERT INTO "Art" VALUES (2,'C. canephora');
INSERT INTO "Kaffebønne" VALUES (1,'Bourbon',1,1);
INSERT INTO "Kaffebønne" VALUES (2,'Caturra',1,3);
INSERT INTO "Kaffebønne" VALUES (3,'San Ramon',1,5);
INSERT INTO "Kaffebønne" VALUES (4,'Robusta',1,1);
INSERT INTO "PartiBestårAv" VALUES (1,1);
INSERT INTO "PartiBestårAv" VALUES (2,3);
INSERT INTO "PartiBestårAv" VALUES (4,1);
INSERT INTO "Kaffe" VALUES (1,'Vinterkaffe 2022','En velsmakende og kompleks kaffe for mørketiden',600,'Lysbrent','20.01.2022',1,1);
INSERT INTO "Kaffe" VALUES (2,'Sommerkaffe 2022','Passer perfekt til en fin sommerdag',750,'Middelsbrent','06.02.2022',2,2);
COMMIT;
