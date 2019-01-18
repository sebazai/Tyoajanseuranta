#Asennusohje

    1. Asenna Python koneellesi (versio 3.5 tai uudempi)
    2. Lataa sovelluksen koodi Githubista "Clone or download" painikkeesta valitsemalla "Download ZIP".
    3. Pura ZIP tiedosto haluaamasi sijaintiin koneellasi
    4. Avaa terminaali tai Windowsissa terminaaliemulaattori ja navigoi kansioon mihin tiedostot purit
    5. Luo sovellukselle virtuaaliympäristö syöttämällä terminaaliin: python3 -m venv venv
    6. Virtuaaliympäristö pitää vielä aktivoida syöttämällä terminaaliin: source venv/bin/activate tai Windowsissa source venv/scripts/activate.
    7. Päivitä pip komennolla: pip install --upgrade pip.
    8. Asenna projektin riippuvuudet syöttämällä: pip install -r requirements.txt
    9. Nyt sovellus voidaan käynnistää komennolla: python3 run.py
    10. Sovellus voidaan avata selaimessa osoitteessa: localhost:5000

#Käynnistäminen Herokussa

    1. Terminaalissa navigoi projektille ja luo git-versionhallintaan komennolla: git init
    2. Luo projektille oma repositorio Githubissa ja lisätään se versionhallinnan piiriin komennolla: git remote add origin <osoite>
    3. Siirrä tiedostot githubiin komennoilla:
    ```
    git add .
    git push -u origin master
    ```
    4. Luo herokuun projekti komennolla: heroku create <projektin nimi>
    5. Lisää tieto herokusta versionhallintaan komennolla: git remote add heroku https://git.heroku.com/<projektin-nimi>.git
    6. Lähetä projekti herokuun seuraavasti: 
   ```
   git add . 
   git commit -m "Initial commit" 
   git push heroku master
   ```
    7. Nyt projekti on avattavissa kerrotussa osoitteessa.

