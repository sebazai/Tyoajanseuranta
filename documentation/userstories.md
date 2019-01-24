# Käyttäjätarinoita

Tälle sivulle on koottu käyttäjätarinoita projektiin liittyen. Käyttäjätarinoiden alle on kirjattu ehtoja, joiden kautta nämä katsotaan toteutuneeksi. Jokaisen käyttäjätarinan kohdalla on myös avattu SQL-lauseet ja tarvittaessa täydennetty pseudokoodilla.

1. Oman työajan selaaminen

Käyttäjänä voin nähdä kaikki merkatut työaikani "Merkatut työajat" linkin kautta.

* Käyttäjä voi tarkastella kirjaamia työaikoja.

```sql
SELECT * FROM kirjaus ORDER BY kirjaus.sisaankirjaus DESC
```

2. Työajan kirjaaminen

Käyttäjänä voin kirjata työajan.

* Käyttäjä voi lisätä työajan.
* Käyttäjä voi leimata sisään.
* Käyttäjä voi leimata ulos, mikäli on leimannut sisään.

```sql
INSERT INTO kirjaus (date_created, date_modified, sisaankirjaus, uloskirjaus, "tehdytMinuutit", kertyma, account_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <sisaankirjaus_aika>, <uloskirjaus_aika>, <tehdyt_minuutit_laskukaava>, <kertyma>, <kirjautuneen_käyttäjän_id>);

INSERT INTO kirjaus (date_created, date_modified, sisaankirjaus, uloskirjaus, "tehdytMinuutit", kertyma, account_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, <sisaankirjaus_aika_nyt>, <NULL>, <NULL>, <NULL>, <kirjautuneen_käyttäjän_id>);

SELECT * FROM Kirjaus WHERE account_id = ? AND uloskirjaus IS NULL;
UPDATE kirjaus SET date_modified=CURRENT_TIMESTAMP, uloskirjaus=<uloskirjaus_aika_nyt> WHERE kirjaus.id = <kirjaus_id_lomakkeesta>;

```

3. Kirjautuminen

Käyttäjä voi kirjautua sisään.

* Käyttäjä voi kirjautua sivustolle
* Sivuston tiedot näkyvät vain kirjautuneille käyttäjille.

```sql
SELECT * FROM account WHERE account.username = <lomakkeen_käyttäjätunnus> AND account.password = <lomakkeen_salasana>;
```





