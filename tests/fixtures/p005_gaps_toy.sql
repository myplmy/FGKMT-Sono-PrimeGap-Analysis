PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE gaps (gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,gapcert TEXT,discoverer TEXT,year INTEGER,merit REAL,primedigits INTEGER,startprime BLOB);
INSERT INTO gaps VALUES(2,1,'C','F','C','toy',2026,1.0,1,'3');
INSERT INTO gaps VALUES(4,1,'C','F','C','toy',2026,1.0,1,'7');
COMMIT;
