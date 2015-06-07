Elisa Viihde -skriptejä
=======================
Erilaisia skriptejä Elisa Viihteen käyttöön. Laita kaikki skriptit `/usr/local/bin`-hakemistoon ja anna niille suoritusoikeudet (`chmod +x`). Lisäksi muokkaa Elisa Viihteen tunnuksesi `elisa_url.py`-tiedostoon. 

`elisa_url.py` on Python-skripti, joka hakee videotiedoston url-osoitteen annetun sivun url-osoitteen perusteella. Sitä käytetään yleensä osana jotain muuta skriptiä, kuten tässä olevat bash-skriptit. 

`elisa_latain.sh` on bash-skripti, joka lataa videon annetun URL-osoitteen perusteella annettuun hakemistoon käyttäen `elisa_url.py`:tä ja `wget`:iä. Sitä käytetään antamalla toiseksi viimeiseksi parametriksi videon sivun osoite ja viimeiseksi kohdetiedosto. Muut parametrit annetaan suoraan `wget`:lle. 

`elisa_katso.sh` on bash-skripti, joka toistaa videon VLC-soittimella ladaten sitä samaan aikaan `wget`:llä. Se käyttää `elisa_url.py`:tä ja myös `inotifywait`:iä, mikäli se on käytettävissä. Videon katselun päätyttyä eli kun VLC suljetaan, video poistetaan koneelta. Oletus tallennuspaikka on `/tmp`-hakemistossa, mutta sitä kannattaa muuttaa mikäli `/tmp` on sijoitettu keskusmuistiin tai on muuten liian pieni. Skriptissä on ehdotettu `.cache`-hakemistoa kotihakemistossa. Tätä skriptiä käytetään antamalla viimeisenä parametrina videon sivun osoite. Muut parametrit annetaan suoraan `wget`:lle. 

`launchy.xml` on Firefoxin Launchy-lisäosan asetustiedosto, joka laitetaan hakemistoon `~/.mozilla/firefox/profiilisi/chrome` ja Firefoxiin asennetaan Lauchy-lisäosa. Tämän jälkeen on mahdollista avata viedoita klikkaamalla niiden linkkiä oikealla hiirennapilla ja valitsemalla *Launchy / Open Link in Katso Elisa Viihteessä*. `launchy.xml` on public domain.
