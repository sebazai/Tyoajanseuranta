# Asennusohje paikallisesti

Jostakin selvitettämättömästä syystä tietokannat ei generoidu automaattisesti, joten on sqlite:llä luotava tietokannat käsin. Taulujen luomista varten löydät komennot [täältä](https://github.com/sebazai/tsoha-tyoajanseuranta/blob/master/documentation/databasediagram.md)

1. Asenna Python koneellesi (versio 3.5 tai uudempi) ja sqlite3
2. Lataa sovelluksen koodi Githubista "Clone or download" painikkeesta valitsemalla "Download ZIP".
3. Pura ZIP tiedosto haluaamasi sijaintiin koneellasi
4. Avaa terminaali tai Windowsissa terminaaliemulaattori ja navigoi kansioon mihin tiedostot purit
5. Luo sovellukselle virtuaaliympäristö syöttämällä terminaaliin: `python3 -m venv venv`
6. Virtuaaliympäristö pitää vielä aktivoida syöttämällä terminaaliin: `source venv/bin/activate` tai Windowsissa source `venv/scripts/activate`
7. Päivitä pip komennolla: `pip install --upgrade pip`
8. Asenna projektin riippuvuudet syöttämällä: `pip install -r requirements.txt`
9. Navigoi application kansioon ja kirjoita `touch tuntikirjaus.db`
10. Aja `sqlite3 tuntikirjaus.db` komento
11. Luo tietokannat yllä olevan linkin kautta.
12. Luo admin tunnus: `INSERT INTO account(name, username, password, role) VALUES ('admin', 'admin', 'adminpw', 'ADMIN');`
13. Nyt sovellus voidaan käynnistää komennolla: `python3 run.py` sovelluskansion juuresta.
14. Sovellus voidaan avata selaimessa osoitteessa: `localhost:5000`

# Siirtäminen Herokuun paikallisesta asennuksesta

Asennathan Herokun työvälineet. Asennusohjeet löytyvät [täältä](https://devcenter.heroku.com/articles/heroku-cli)

1. Terminaalissa navigoi projektin kansioon ja luo git-versionhallintaan komennolla: `git init`
2. Luo projektille oma repositorio Githubissa ja lisätään se versionhallinnan piiriin komennolla: `git remote add origin <osoite>`
3. Siirrä tiedostot githubiin komennoilla:
   ```
   git add .
   git push -u origin master
   ```
4. Luo herokuun projekti komennolla: `heroku create <projektin nimi>`
5. Lisää ympäristömuuttujat komennoilla (TZ = Timezone, jonka voit muuttaa tarvittaessa):
   ```
   heroku config:set HEROKU=1
   heroku config:set TZ=Europe/Helsinki
   ```
6. Asenna PostgreSQL tietokanta herokuun:
   ```
   heroku addons:add heroku-postgresql:hobby-dev
   ```
7. Lisää tieto herokusta versionhallintaan komennolla: `git remote add heroku https://git.heroku.com/<projektin-nimi>.git`
8. Lähetä projekti herokuun seuraavasti: 
   ```
   git add . 
   git commit -m "Initial commit" 
   git push heroku master
   ```
9. Nyt projekti on avattavissa kerrotussa osoitteessa.
10. Lisää admin käyttäjä seuraavilla komennoilla:
   ```
   heroku pg:psql
   INSERT INTO account (name, username, password, role) VALUES ('admin', 'admin', 'adminpw', 'ADMIN');
   \q
   ```
