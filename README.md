# Turun kaupungin kulkijalaskentakokeilu 12/2018 - 2/2019

Turun kaupungissa on tehty kulkijamittauksia 26 pisteessä 3 kuukauden ajan. Ohjelma kertoo tilastoja mittauspisteistä.

Käyttäjää pyydetään kertomaan, mistä mittauspisteestä hän haluaa tilastoja. Jos käyttäjä haluaa lisäksi piirtää valitsemansa mittauspisteen kartalle, geopandas pitää olla asennettuna.

Data on saatavilla Turun kaupungin sivuilta, https://www.avoindata.fi/data/fi/dataset/turun-kaupungin-kulkijalaskentakokeilu. Mittauspisteiden sijaintitiedon piirtämiseen on käytetty Turun kaupungin jakamaa paikkatietoa, https://api.turku.fi/wfs2gml/.

Varsinainen ajettava ohjelma on kulkija.py. Tämän lisäksi ohjelma käyttää abo_measurements.py-tiedoston funktioita kaupunkidatan käsittelyyn ja street_info.py tilastotietojen laskemiseksi ja tulostamiseksi.
