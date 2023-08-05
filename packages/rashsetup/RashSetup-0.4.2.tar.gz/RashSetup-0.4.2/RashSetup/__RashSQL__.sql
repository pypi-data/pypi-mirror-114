CREATE TABLE IF NOT EXISTS "Container"(
    "Name" TEXT PRIMARY KEY NOT NULL UNIQUE,
    "Hosted" TEXT NOT NULL UNIQUE,
    "Version" VARCHAR(20) NOT NULL,
    "Template" VARCHAR(20) NOT NULL,
    "Readme" TEXT DEFAULT "",
    "Default" BOOL DEFAULT FALSE
);


INSERT OR IGNORE INTO "Container"(
    "Name", "Hosted", "Version", "Template", "Default") VALUES (
    "Rash", "https://github.com/RahulARanger/Rash/tree/master/Rash", "0.0.4", "Main", TRUE
);


INSERT OR IGNORE INTO "Container"(
"Name", "Hosted", "Version", "Template", "Default") VALUES (
"RashLogger", "https://github.com/RahulARanger/Rash/tree/master/RashLogger/RashLogger", "0.0.1", "Tool", TRUE
);

CREATE TABLE IF NOT EXISTS "Sql"(
    "Hash" INT PRIMARY KEY NOT NULL UNIQUE,
    "SQL" TEXT NOT NULL,
    "Empty" BOOLEAN NOT NULL DEFAULT TRUE
);


INSERT OR IGNORE INTO "Sql"(
'Hash', 'SQL', "Empty") VALUES(
0, "SELECT SQL, Empty FROM Sql WHERE Hash = ?", FALSE
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
1, "SELECT * FROM Container;"
); -- for selecting all entities in Container


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
2, "SELECT * FROM Container WHERE Name = ?;", FALSE
); -- searches in container through Name column


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
3, "SELECT Hosted FROM Container WHERE NAME = ?;", False);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
4, "SELECT Version FROM Container WHERE NAME = ?;", False);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
5, "SELECT * FROM Container WHERE Hosted = ?;", False);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
6, "SELECT Name FROM Container;", True);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
7, "UPDATE Container SET Readme = ? WHERE NAME = ?;", False);
