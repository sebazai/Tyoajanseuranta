# Käyttäjätarinoita

Tälle sivulle on koottu käyttäjätarinoita projektiin liittyen. Käyttäjätarinoiden alle on kirjattu ehtoja, joiden kautta nämä katsotaan toteutuneeksi. Jokaisen käyttäjätarinan kohdalla on myös avattu SQL-lauseet ja tarvittaessa täydennetty pseudokoodilla.

#### 1. Oman työajan selaaminen

Käyttäjänä voin nähdä kaikki merkatut työaikani "Merkatut työajat" linkin kautta.

* Käyttäjä voi tarkastella kirjaamiaan työaikoja.

```sql
SELECT * FROM kirjaus WHERE account_id = <kirjautunut_id> ORDER BY kirjaus.sisaankirjaus DESC;
```
* Käyttäjä näkee viimeisimmän sisäänleimauksen, mikäli ei ole leimannut ulos.
```sql
SELECT * FROM Kirjaus WHERE account_id = ? AND uloskirjaus IS NULL;

```

#### 2. Työajan kirjaaminen

Käyttäjänä voin kirjata työajan

* Käyttäjä voi lisätä työajan.
```sql
INSERT INTO kirjaus (sisaankirjaus, uloskirjaus, "tehdytMinuutit", kertyma, account_id) 
VALUES (<sisaankirjaus_aika>, <uloskirjaus_aika>, <tehdyt_minuutit>, <kertyma>, <kirjautuneen_käyttäjän_id>);
```
* Käyttäjä voi leimata sisään kirjautumisen jälkeen.
```sql
INSERT INTO kirjaus (sisaankirjaus, uloskirjaus, "tehdytMinuutit", kertyma, account_id) 
VALUES (<sisaankirjaus_aika_nyt>, <NULL>, <NULL>, <NULL>, <kirjautuneen_käyttäjän_id>);
```
* Käyttäjä voi leimata ulos kirjautumisen jälkeen, mikäli on leimannut sisään ja kyseiselle tapahtumalle ei ole merkattu uloskirjausta.
```sql
UPDATE kirjaus 
SET date_modified=CURRENT_TIMESTAMP, uloskirjaus=<uloskirjaus_aika_nyt> 
WHERE kirjaus.id = <kirjaus_id_lomakkeesta>;
```

#### 3. Kirjautuminen

Käyttäjä voi kirjautua sisään. Sovellus toimii ainoastaan kirjautuneena

* Käyttäjä voi kirjautua sivustolle.
```sql
SELECT * FROM account 
WHERE account.username = <lomakkeen_käyttäjätunnus> 
AND account.password = <lomakkeen_salasana>;
```

#### 4. Projektihallinta

Pääkäyttäjä voi liittää käyttäjän projektiin ja merkitä tämän ensisijaiseksi projektiksi (paaprojekti)

```sql
INSERT INTO userproject ("onAsiakas", account_id, project_id, unique_id, paaprojekti) VALUES (<lomakkeesta_boolean>, <lomakkeesta_accountId>, <lomakkeesta_projectId>, <accountId+projectId yhdistettyna>, <lomakkeesta boolean>)
```





