# Käyttäjätarinoita

Tälle sivulle on koottu käyttäjätarinoita projektiin liittyen. Käyttäjätarinoiden alle on kirjattu ehtoja, joiden kautta nämä katsotaan toteutuneeksi. Jokaisen käyttäjätarinan kohdalla on myös avattu SQL-lauseet ja tarvittaessa täydennetty pseudokoodilla.

Jokaisessa tietokannassa on myös date_created ja date_modified sekä id, näitä ei ole käyttäjätarinoissa merkitty, ellei erikseen mainittu.

#### 1. Oman työajan selaaminen

Käyttäjänä voin nähdä kaikki merkatut työaikani "Merkatut työajat" linkin kautta.

* Käyttäjä voi tarkastella kirjaamiaan työaikojaan pääprojektistaan.

```sql
SELECT * FROM kirjaus WHERE account_id = <kirjautunut_id> ORDER BY kirjaus.sisaankirjaus DESC;
```
* Käyttäjä näkee viimeisimmän sisäänleimauksen, mikäli ei ole leimannut ulos.
```sql
SELECT * FROM Kirjaus WHERE account_id = ? AND uloskirjaus IS NULL;

```

#### 2. Työajan kirjaaminen

Käyttäjänä voin kirjata työajan, leimata sisään ja ulos reaaliajassa.

* Käyttäjä voi lisätä työajan "Lisää työaika" linkin kautta.
```sql
INSERT INTO kirjaus (sisaankirjaus, uloskirjaus, tehdytminuutit, kertyma, account_id) 
VALUES (<sisaankirjaus_aika>, <uloskirjaus_aika>, <tehdyt_minuutit>, <kertyma>, <current_user.id>)
```
* Käyttäjä voi leimata sisään kirjautumisen jälkeen tai painamalla "Työajanseuranta" vasemmassa yläkulmassa.
```sql
INSERT INTO kirjaus (sisaankirjaus, uloskirjaus, tehdytminuutit, kertyma, account_id) 
VALUES (<sisaankirjaus_aika_nyt>, <NULL>, <NULL>, <NULL>, <kirjautuneen_käyttäjän_id>);
```
* Käyttäjä voi leimata ulos kirjautumisen jälkeen, mikäli on leimannut sisään ja kyseiselle tapahtumalle ei ole merkattu uloskirjausaikaa.
```sql
UPDATE kirjaus 
SET date_modified=CURRENT_TIMESTAMP, uloskirjaus=<uloskirjaus_aika_nyt> 
WHERE kirjaus.id = <kirjaus_id_lomakkeesta>;
```

#### 3. Kirjautuminen ja käyttäjähallinta

Käyttäjä voi kirjautua sisään. Sovellus toimii ainoastaan kirjautuneena.

* Käyttäjä voi kirjautua sivustolle.
```sql
SELECT * FROM account 
WHERE account.username = <lomakkeen_käyttäjätunnus> 
AND account.password = <lomakkeen_salasana>;
```

* Käyttäjät listataan Hallinnoi käyttäjiä sivulla
```sql
SELECT * FROM account
```

* Pääkäyttäjä voi päivittää käyttäjän nimen ja salasana voidaan vaihtaa.
```sql
UPDATE account SET name=<lomakkeesta_uusi_nimi>, password=<lomakkeesta_salasana> 
WHERE account.id = <lomakkeesta_id>
```

* Pääkäyttäjä voi lisätä uuden käyttäjän ja ohjelmisto liittää sille samalla pääprojektin mitä työstää.
account_id palautuu tietokannasta userproject lisäystä varten, mikäli se läpäisee validoinnin.

```sql
INSERT INTO account (name, username, password, role) 
VALUES (<lomakkeesta_nimi>, <lomakkeesta_tunnus>, <lomake_salasana>, <lomake_boolean>)

INSERT INTO userproject ("onAsiakas", account_id, project_id, paaprojekti) 
VALUES (<always_false>, <palautettu_arvo_aikaisemmasta_lisayksesta>, <lomake_projekti>, <always_true>)
```

* Pääkäyttäjä voi poistaa käyttäjän, tämä poistaa myös käyttäjäliitokset ja kaikki kirjaukset.
```sql
DELETE FROM kirjaus WHERE Kirjaus.account_id = <poistettavan_id>
DELETE FROM userproject WHERE Userproject.account_id = <poistettavan_id>
DELETE FROM account WHERE Account.id = <poistettavan_id>
```


#### 4. Projektihallinta

* Projektit listataan sivulla "Hallinnoi projekteja"

```sql
SELECT * FROM projekti
```

* Pääkäyttäjä voi poistaa projektin. Tämä poistaa myös käyttäjäliitokset projekteihin ja kirjaukset jotka tehty projektiin.
```sql
DELETE FROM Kirjaus WHERE userproject_id = (SELECT id FROM userproject WHERE project_id = <poistettava_id>)
DELETE FROM Userproject WHERE Userproject.projekti_id = <poistettava_id>
DELETE FROM Projekti WHERE projekti.id = <poistettava_id>
```

* Pääkäyttäjä voi lisätä uuden projektin.
```sql
INSERT INTO projekti (name, customer, vakiotyoaika) 
VALUES (<lomakkeesta_nimi>, <lomakkeesta_asiakas>, <lomakkeesta_minuutit>)

```

* Pääkäyttäjä voi muokata projektin tietoja.
```sql
UPDATE projekti SET date_modified=CURRENT_TIMESTAMP, 
name=<lomakkeesta_nimi>, customer=<lomakkeesta_asiakas>, vakiotyoaika=<lomakkeesta_aika> 
WHERE projekti.id = ?
```

#### 5. Käyttäjäliitokset ja Asetukset sivu


* Pääkäyttäjä voi liittää käyttäjän projektiin ja merkitä tämän ensisijaiseksi projektiksi (paaprojekti) tai asiakkaaksi

```sql
INSERT INTO userproject (onasiakas, account_id, project_id, paaprojekti) 
VALUES (<lomakkeesta_boolean>, <lomakkeesta_accountId>, <lomakkeesta_projectId>, <lomakkeesta boolean>)
```

* Pääkäyttäjä voi päivittää käyttäjän ensisijaista projektia (pääprojekti) ja merkitä myös käyttäjän asiakkaaksi.

```sql
UPDATE userproject SET paaprojekti = <lomakkeesta_boolean>, onAsiakas = <lomakkeesta_boolean> 
WHERE account_id = <lomake_selectfield> AND project_id = <lomake_selectfield>
```
Huom! Jos asiakas on merkittynä lomakkeessa, kahdessa ylläolevassa kyselyssä, päivitetään käyttäjän rooli
```sql
UPDATE account SET role = 'ASIAKAS' WHERE id = <lomakkeesta_accountId>
```


Kirjautunut käyttäjä voi muokata omia asetuksia oikeasta yläkulmasta "Asetukset" linkin takaa.

* Käyttäjä näkee projektit mihin hänet on liitetty ja näkee onko projektin asiakas mikäli käyttäjä on merkittynä asiakkaaksi projektiin.
```sql
SELECT Account.id, Account.name, Account.username, Projekti.name AS projekti, 
Userproject.onasiakas, Userproject.paaprojekti FROM account 
INNER JOIN Userproject ON Userproject.account_id = Account.id 
INNER JOIN Projekti ON Projekti.id = Userproject.project_id 
WHERE Account.id = <current_user.id>
```

* Käyttäjä voi muuttaa työstettävää projektia, jolloin vanhasta projektista muutetaan "paaprojekti" boolean false ja uusi projekti true jonka käyttäjä on valinnut. Tämä ei vaihda ASIAKAS statusta.
```sql
UPDATE userproject SET paaprojekti = False WHERE account_id = <current_user.id> AND paaprojekti = True

UPDATE userproject SET paaprojekti = True 
WHERE account_id = <current_user.id> AND project_id = <lomakkeesta>
```

## Yhteenvetokyselyt

Käyttäjä saa leimausnäkymäänsä kertyneen saldon pääprojektistaan.

```sql
SELECT SUM(kertyma) FROM Kirjaus 
WHERE account_id = <kirjautuneen_id> 
AND userproject_id = <käyttäjän_pääprojekti>;
```

Asiakas saa Merkatut työajat näkymässä yhteenvedon tehdyistä tunneista. (tehdytMinuutit/60)

```sql
SELECT SUM(tehdytMinuutit), Account.name, Projekti.name AS projektinimi FROM Kirjaus 
INNER JOIN Account ON Account.id = Kirjaus.account_id 
INNER JOIN Userproject ON Userproject.project_id = :projekti 
AND Userproject.account_id = Kirjaus.account_id 
AND Kirjaus.userproject_id = Userproject.id 
INNER JOIN Projekti ON Projekti.id = :projekti 
GROUP BY Account.name, Projekti.name ORDER BY Account.name ASC;
```

Esimies/pääkäyttäjä näkee kuinka resurssit on jaettu eri projekteihin käyttäjäliitos sivulta, eli montako työntekijää kussakin projektissa on kyseisellä hetkellä. (käyttäjillä pääprojekti = true)

```sql
SELECT COUNT(Account.id), Projekti.name FROM Account 
INNER JOIN Userproject ON Userproject.account_id = Account.id 
AND Userproject.paaprojekti = True 
INNER JOIN Projekti ON Projekti.id = Userproject.project_id 
GROUP BY Projekti.name;
```
