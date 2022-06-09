from shapely.geometry import Point

# ubacivanje tacaka, svaka tacka predstavlja jednu stanicu

beograd_centar = Point(20.451872, 44.794022)
novi_beograd = Point(20.418163, 44.806930)
tosin_bunar = Point(20.397305, 44.816374)
zemun = Point(20.371186, 44.836408)
zemun_polje = Point(20.334742, 44.857626)
batajnica = Point(20.271684, 44.899177)
nova_pazova = Point(20.210093, 44.937479)
stara_pazova = Point(20.137890, 44.986221)
indjija = Point(20.092248, 45.048707)
beska = Point(20.041788, 45.140884)
karlo_vinogradi = Point(19.970495, 45.180529)
srem_kratlovci = Point(19.92941, 45.20783)
petrovaradin = Point(19.888095, 45.240412)
novi_sad = Point(19.829477, 45.265810)

tip_tacke = type(beograd_centar)
print(beograd_centar)

lista_tacaka = [(beograd_centar, "Beograd centar"), (novi_beograd,"Novi Beogad"),( tosin_bunar,"Tosin Bunar"), (zemun,"Zemnu"),
                (zemun_polje,"Zemun Polje"),(batajnica,"Batajnica"),( nova_pazova,"Nova Pazova"), (stara_pazova,"Stara Pazova"),
                (indjija,"Indjija"),( beska,"Beska"),(karlo_vinogradi,"Karlovacki vinogradi"),
                (srem_kratlovci,"Sremski Karlovci"), (petrovaradin,"Petrovaradin"), (novi_sad,"Novi Sad")]

import geopandas as gpd
import matplotlib.pyplot as plt
from fiona.crs import from_epsg

prostor_tacke = gpd.GeoDataFrame()
prostor_tacke['geometry'] = None

for indeks, (tacka,naziv) in enumerate(lista_tacaka):
    prostor_tacke.loc[indeks, 'geometry'] = tacka
    prostor_tacke.loc[indeks, 'Ime stanice'] = naziv

prostor_tacke.crs = from_epsg(4326)
prostor_tacke.plot(facecolor='red');
plt.show()

a = r"C:\Users\Adrijana\Desktop\Klk Peulic\tacke.shp"
prostor_tacke.to_file(a)

# radzaljina Beograda i Novog Sada vazdusnom linijom

rastojanjeBg_Ns = beograd_centar.distance(novi_sad)
print('Udaljenost izmedju Beograda i Novog Sada je', rastojanjeBg_Ns)

# Drugi nacin
from shapely.geometry import LineString

razdaljinaBG_NS = LineString([beograd_centar, novi_sad])
duzina = razdaljinaBG_NS.length
print(duzina)

# pravljenje linija od tacaka i koriscenje istih

bg_nbg = LineString([beograd_centar, novi_beograd])
nbg_tbunar = LineString([novi_beograd, tosin_bunar])
tbunar_zemun = LineString([tosin_bunar, zemun])
zemun_zpolje = LineString([zemun, zemun_polje])
zpolje_batajnica = LineString([zemun_polje, batajnica])
batajnica_npazova = LineString([batajnica, nova_pazova])
npazova_spazova = LineString([nova_pazova, stara_pazova])
spazova_indjija = LineString([stara_pazova, indjija])
indjija_beska = LineString([indjija, beska])
beska_kvinogradi = LineString([beska, karlo_vinogradi])
kvinogradi_skarlovci = LineString([karlo_vinogradi, srem_kratlovci])
skarlovci_petrovaradin = LineString([srem_kratlovci, petrovaradin])
petrovaradin_novisad = LineString([petrovaradin, novi_sad])

tip_linije = type(bg_nbg)
print(bg_nbg)

#provera da li se linija dodiruje sa tackom
indjija_beska.touches(beska)
print(indjija_beska.touches(beska))

# 1. kroz listu dobijanje jedinstvene linije i plotovanje

lista_linije = [bg_nbg, nbg_tbunar, tbunar_zemun, zemun_zpolje, zpolje_batajnica, batajnica_npazova, npazova_spazova,
                spazova_indjija, indjija_beska, beska_kvinogradi, kvinogradi_skarlovci, skarlovci_petrovaradin,
                petrovaradin_novisad]

prostor_linije = gpd.GeoDataFrame()
prostor_linije['geometry'] = None

for indeks, t in enumerate(lista_linije):
    prostor_linije.loc[indeks, 'geometry'] = t
    print(indeks, t)

prostor_linije.crs = from_epsg(4326)
prostor_linije.plot(facecolor='blue')
plt.title("Linija Bg-NS")

plt.tight_layout()
plt.show()

# Pomocu multilinije dobijanje jedinstvene linije i plotovanje iste
from shapely.geometry import MultiLineString

multilinije = MultiLineString(
    [bg_nbg, nbg_tbunar, tbunar_zemun, zemun_zpolje, zpolje_batajnica, batajnica_npazova, npazova_spazova,
     spazova_indjija, indjija_beska, beska_kvinogradi, kvinogradi_skarlovci, skarlovci_petrovaradin,
     petrovaradin_novisad])

tip_multilinije = type(multilinije)
print('tip multilinije', multilinije)

broj_linija = len(multilinije)
print('Broj linija je:', broj_linija)

duzina_linije = multilinije.length
print('Duzina linije je:', duzina_linije)

linija_centar = multilinije.centroid
print('Tacka koja predstavlja centar linije je:', linija_centar)

#provera da li multilinija sadrzi tacku "beska"
multilinije.intersects(beska)
print(multilinije.intersects(beska))

prostor_multilinije = gpd.GeoDataFrame()
prostor_multilinije['geometry'] = None

prostor_multilinije.loc[0, 'geometry'] = multilinije

prostor_multilinije.crs = from_epsg(4326)
prostor_multilinije.plot(facecolor='blue')
plt.title("Multilinija")

plt.tight_layout()
plt.show()

b = r"C:\Users\Adrijana\Desktop\Klk Peulic\linije.shp"
prostor_multilinije.to_file(b)

# ubacivanje fajla- opstine kroz koje prolazi vozna linija Beograd - Novi Sad
fp = r"C:\Users\Adrijana\Desktop\Klk Peulic\Opstine_4326 wgs84.shp"

# citanje fajla
prostor_poligon = gpd.read_file(fp)
prostor_poligon

# proveriti trenutni koordinatni sistem
prostor_poligon.crs
print(prostor_poligon.crs)

prostor_poligon['geometry'].head()
print(prostor_poligon['geometry'].head())

# Prikaz karte
prostor_poligon.plot(column='Opstina', cmap='hsv');

# dodavanje naslova
plt.title("WGS84 CRS");
plt.tight_layout()
plt.show()

prostor_poligon = prostor_poligon.rename(columns={'Opstina': 'Ime opstine'})
prostor_poligon.columns
print(prostor_poligon)

# spajanje podataka samo kao prikaz
#provera u kojem kordinatnom sistemu se nalaze podaci

multilinije2 = prostor_multilinije.to_crs(prostor_tacke.crs)
print(multilinije2.crs)
print(prostor_tacke.crs)
prostor_poligon.to_crs(prostor_tacke.crs, inplace=True)
print(prostor_poligon.crs)

spojeno = prostor_tacke.geometry.append(prostor_poligon.geometry).append(prostor_multilinije.geometry)

print(spojeno.crs)
print(spojeno)

spojeno.plot(cmap="hsv")
plt.title("Sve spojeno")
plt.show()



