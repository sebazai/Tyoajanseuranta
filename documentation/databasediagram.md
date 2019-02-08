Alustava tietokantasuunnitelma, joka voi vielä muuttua projektin edetessä.

![Schema](https://github.com/sebazai/tsoha-tyoajanseuranta/blob/master/documentation/tietokantakaavio.png)

## Tietokannan rakenne:
```sql
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	role VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
CREATE TABLE projekti (
	date_created DATETIME, 
	date_modified DATETIME, 
	id INTEGER NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	customer VARCHAR(144) NOT NULL, 
	vakiotyoaika INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE userproject (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	onasiakas BOOLEAN DEFAULT 'False' NOT NULL, 
	account_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	paaprojekti BOOLEAN DEFAULT 'False' NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id, project_id), 
	CHECK (onasiakas IN (0, 1)), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(project_id) REFERENCES projekti (id), 
	CHECK (paaprojekti IN (0, 1))
);
CREATE TABLE kirjaus (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	sisaankirjaus DATETIME, 
	uloskirjaus DATETIME, 
	"tehdytMinuutit" INTEGER, 
	kertyma INTEGER, 
	account_id INTEGER NOT NULL, 
	userproject_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(userproject_id) REFERENCES userproject (id)
);
```
