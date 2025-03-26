import numpy as np

plik = open("SystemDecyzyjny.txt", "r")
dane = []
for wiersz in plik:
    dane.append(wiersz.strip().split())

nazwy_kolumn = ["indeks", "pogoda", "temperatura", "wilgotnosc", "wiatr", "decyzja"]
nazwy_wierszy = [wiersz[0] for wiersz in dane]

print("\nDane:")
for i, wiersz in enumerate(dane):
    print(f"{wiersz[0]} {wiersz[1:]}")

y = len(dane)
mac = np.zeros((y, y), dtype=object)
np.fill_diagonal(mac, 'X')

indeks_decyzji = nazwy_kolumn.index("decyzja")
for i in range(y):
    for j in range(i + 1, y):
        if dane[i][indeks_decyzji] == dane[j][indeks_decyzji]:
            mac[i, j] = "X"
            mac[j, i] = "X"

print("\nMacierz nieodróżnialności bez atrybutów:")
for wiersz in mac:
    print(" ".join(map(str, wiersz)))

# X oznacza że decyzje dla obiektów są takie same

mac2 = np.empty((y,y),dtype=object)


