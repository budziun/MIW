#       a1 a2 a3 a4 a5 a6  d
#    o1 [1, 1, 1, 1, 3, 1, 1]
#    o2 [1, 1, 1, 1, 3, 2, 1]
#    o3 [1, 1, 1, 3, 2, 1, 0]
#    o4 [1, 1, 1, 3, 3, 2, 1]
#    o5 [1, 1, 2, 1, 2, 1, 0]
#    o6 [1, 1, 2, 1, 2, 2, 1]
#    o7 [1, 1, 2, 2, 3, 1, 0]
#    o8 [1, 1, 2, 2, 4, 1, 1]

import numpy as np

file = open("values.txt", "r")

data = []
for line in file:
    data.append([int(d) for d in line.split()])

kolumny = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
wiersze = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8"]
x = len(kolumny)
y = len(wiersze)

# dane z pliku
print(kolumny)
for i in range(y):
   print(f"{wiersze[i]} [{'[' + ','.join(map(str, data[i]))  + ']' if i < x - 1 else '[' + ','.join(map(str, data[i]))  + ']'}")

# macierz wierszeXwiersze (tu 8x8) nieodroznialnsoci
mac = np.zeros((y, y), dtype=object)
np.fill_diagonal(mac, 'X')

decyzja_indeks = kolumny.index("d")

for i in range(y):
    for j in range(i + 1, y):
        if data[i][decyzja_indeks] == data[j][decyzja_indeks]:
            mac[i, j] = "X"
            mac[j, i] = "X"

print("\nMacierz nieodróżnialnosci bez atrybutów")
for row in mac:
    print(" ".join(map(str, row)))

# X oznacza że decyzje dla obiektów są takie same

mac2 = np.empty((y,y),dtype=object)
for i in range(y):
    for j in range(y):
        if mac[i,j] == "X":
            mac2[i, j] = "X"
        else:
            atrybut1 = [kolumny[k] for k in range(len(kolumny) - 1) if data[i][k] == data[j][k]]
            mac2[i, j] = " ".join(atrybut1) if atrybut1 else "BRAK"
print("\nMacierz nieodróżnialnosci z atrybutami których wartosci są wspólne dla dwoch obiektów")
print(mac2)

print("\nReguly I rzedu")
sprawdzenie = {'a1', 'a2', 'a3', 'a4', 'a5', 'a6'}
reguly = []
req_2 = []
d_atr = []
for i in range(mac2.shape[1]):
    wszystkie = set()
    for row in mac2[:, i]:
        if row != "X":
            wszystkie.update(row.split())

    brakujace = sprawdzenie - wszystkie

    if brakujace:
        for brak in brakujace:
            indeks_atrybutu = kolumny.index(brak)
            wartosc_atrybutu = data[i][indeks_atrybutu]
            decyzja = data[i][-1]
            reguly.append(f"o{i + 1}: ({brak} = {wartosc_atrybutu}) ==> (d={decyzja})")
            d_atr.append(f"{brak} dla o{i+1}")
            req_2.append(f"o{i+1},{brak}")

print(reguly)
unikalne_reguly = {}
for regula in reguly:
    czesc_atrybutu = regula.split(": ")[1].split(" ==>")[0].strip()
    czesc_decyzji = regula.split("==>")[1].strip()
    pelna_regula = f"{czesc_atrybutu} ==> {czesc_decyzji}"

    if pelna_regula in unikalne_reguly:
        unikalne_reguly[pelna_regula] += 1
    else:
        unikalne_reguly[pelna_regula] = 1

pogrupowane1 = []
for regula, licznik in unikalne_reguly.items():
    if licznik > 1:
        print(f"{regula}[{licznik}]")
        pogrupowane1.append(regula)
        pogrupowane1.append(licznik)
    else:
        print(f"{regula}")
        pogrupowane1.append(regula)

print("\nReguly II rzedu")
print(f"Te wartosci musimy wykluczyc z macierzy {d_atr}\n")

mac3= mac2
sprawdzenie2 = {
'a1a2','a1a3','a1a4','a1a5','a1a6',
'a2a3','a2a4','a2a5','a2a6',
'a3a4','a3a5','a3a6',
'a4a5','a4a6',
'a5a6'
}

reguly2 = []

wykluczenia = {}
for item in req_2:
    parts = item.split(',')
    obiekt = parts[0]
    atrybut = parts[1]

    if obiekt not in wykluczenia:
        wykluczenia[obiekt] = set()

    wykluczenia[obiekt].add(atrybut)

reguly2 = []

for i in range(len(mac3)):
    obiekt_nazwa = f"o{i + 1}"
    obiekt_indeks = i
    wszystkie_pary = set()


    wykluczone_atrybuty = set()
    if obiekt_nazwa in wykluczenia:
        wykluczone_atrybuty = wykluczenia[obiekt_nazwa]


    for j in range(len(mac3[i])):
        if mac3[i, j] != "X" and mac3[i, j] != "BRAK":
            atrybuty = mac3[i, j].split()

            atrybuty = [attr for attr in atrybuty if attr not in wykluczone_atrybuty]

            for idx1 in range(len(atrybuty)):
                for idx2 in range(idx1 + 1, len(atrybuty)):
                    para = atrybuty[idx1] + atrybuty[idx2]
                    wszystkie_pary.add(para)

    sprawdzenie_dla_obiektu = set()
    for para in sprawdzenie2:
        zawiera_wykluczone = False
        for atrybut in wykluczone_atrybuty:
            if atrybut in para:
                zawiera_wykluczone = True
                break
        if not zawiera_wykluczone:
            sprawdzenie_dla_obiektu.add(para)

    brakujace2 = sprawdzenie_dla_obiektu - wszystkie_pary

    decyzja = data[obiekt_indeks][-1]

    for para in brakujace2:
        atrybut1 = para[:2]
        atrybut2 = para[2:]

        indeks_atrybut1 = kolumny.index(atrybut1)
        indeks_atrybut2 = kolumny.index(atrybut2)
        wartosc_atrybut1 = data[obiekt_indeks][indeks_atrybut1]
        wartosc_atrybut2 = data[obiekt_indeks][indeks_atrybut2]

        regula = f"{obiekt_nazwa}: ({atrybut1} = {wartosc_atrybut1} & {atrybut2} = {wartosc_atrybut2}) ==> (d={decyzja})"
        reguly2.append(regula)

for regula in reguly2:
    print(regula)

unikalne_reguly2 = {}
for regula in reguly2:
    czesc_atrybutu = regula.split(": ")[1].split(" ==>")[0].strip()
    czesc_decyzji = regula.split("==>")[1].strip()
    pelna_regula = f"{czesc_atrybutu} ==> {czesc_decyzji}"

    if pelna_regula in unikalne_reguly2:
        unikalne_reguly2[pelna_regula] += 1
    else:
        unikalne_reguly2[pelna_regula] = 1

print("\nPogrupowane reguly")
for regula, licznik in unikalne_reguly2.items():
    if licznik > 1:
        print(f"{regula}[{licznik}]")
    else:
        print(f"{regula}")

print("\nReguly III rzedu")

mac4 = mac3
reguly3 = []

sprawdzenie3 = {
'a1a2a3', 'a1a2a4', 'a1a2a5', 'a1a2a6',
'a1a3a4', 'a1a3a5', 'a1a3a6',
'a1a4a5', 'a1a4a6',
'a1a5a6',
'a2a3a4', 'a2a3a5', 'a2a3a6',
'a2a4a5', 'a2a4a6',
'a2a5a6',
'a3a4a5', 'a3a4a6',
'a3a5a6',
'a4a5a6'
}

for i in range(len(mac4)):
    obiekt_nazwa = f"o{i + 1}"
    obiekt_indeks = i

    wszystkie_trojki = set()

    wykluczone_atrybuty = set()
    if obiekt_nazwa in wykluczenia:
        wykluczone_atrybuty = wykluczenia[obiekt_nazwa]

    for j in range(len(mac4[i])):
        if mac4[i, j] != "X" and mac4[i, j] != "BRAK":
            atrybuty = mac4[i, j].split()
            atrybuty = [attr for attr in atrybuty if attr not in wykluczone_atrybuty]

            for idx1 in range(len(atrybuty)):
                for idx2 in range(idx1 + 1, len(atrybuty)):
                    for idx3 in range(idx2 + 1, len(atrybuty)):
                        trojka = atrybuty[idx1] + atrybuty[idx2] + atrybuty[idx3]
                        wszystkie_trojki.add(trojka)

    sprawdzenie_dla_obiektu = set()
    for trojka in sprawdzenie3:
        zawiera_wykluczone = False
        for atrybut in wykluczone_atrybuty:
            if atrybut in trojka:
                zawiera_wykluczone = True
                break
        if not zawiera_wykluczone:
            sprawdzenie_dla_obiektu.add(trojka)

    brakujace3 = sprawdzenie_dla_obiektu - wszystkie_trojki

    decyzja = data[obiekt_indeks][-1]

    for trojka in brakujace3:
        atrybut1 = trojka[:2]
        atrybut2 = trojka[2:4]
        atrybut3 = trojka[4:]

        indeks_atrybut1 = kolumny.index(atrybut1)
        indeks_atrybut2 = kolumny.index(atrybut2)
        indeks_atrybut3 = kolumny.index(atrybut3)

        wartosc_atrybut1 = data[obiekt_indeks][indeks_atrybut1]
        wartosc_atrybut2 = data[obiekt_indeks][indeks_atrybut2]
        wartosc_atrybut3 = data[obiekt_indeks][indeks_atrybut3]

        regula = f"{obiekt_nazwa}: ({atrybut1} = {wartosc_atrybut1} & {atrybut2} = {wartosc_atrybut2} & {atrybut3} = {wartosc_atrybut3}) ==> (d={decyzja})"
        reguly3.append(regula)

for regula in reguly3:
    print(regula)

warunki_regul2 = []
for regula in reguly2:
    czesc_warunku = regula.split("==>")[0].strip()
    if "(" in czesc_warunku and ")" in czesc_warunku:
        warunek = czesc_warunku[czesc_warunku.find("(") + 1:czesc_warunku.find(")")]
    else:
        warunek = czesc_warunku
    warunki_regul2.append(warunek)

niepokryte_reguly3 = []

for regula3 in reguly3:
    czesc_warunku3 = regula3.split("==>")[0].strip()
    if "(" in czesc_warunku3 and ")" in czesc_warunku3:
        warunek3 = czesc_warunku3[czesc_warunku3.find("(") + 1:czesc_warunku3.find(")")]
    else:
        warunek3 = czesc_warunku3

    atrybuty_wartosci3 = {}
    czesci = warunek3.split("&")
    for czesc in czesci:
        atrybut_wartosc = czesc.strip().split("=")
        atrybut = atrybut_wartosc[0].strip()
        wartosc = atrybut_wartosc[1].strip()
        atrybuty_wartosci3[atrybut] = wartosc

    jest_pokryta = False

    for warunek2 in warunki_regul2:
        atrybuty_wartosci2 = {}
        czesci = warunek2.split("&")
        for czesc in czesci:
            atrybut_wartosc = czesc.strip().split("=")
            atrybut = atrybut_wartosc[0].strip()
            wartosc = atrybut_wartosc[1].strip()
            atrybuty_wartosci2[atrybut] = wartosc

        jest_podzbiorem = True
        for atrybut, wartosc in atrybuty_wartosci2.items():
            if atrybut not in atrybuty_wartosci3 or atrybuty_wartosci3[atrybut] != wartosc:
                jest_podzbiorem = False
                break

        if jest_podzbiorem:
            jest_pokryta = True
            break

    if not jest_pokryta:
        niepokryte_reguly3.append(regula3)

print("\nReguly III rzędu z pokryciem przez reguły II rzędu):")
for regula in niepokryte_reguly3:
    print(regula)

unikalne_niepokryte_reguly3 = {}
for regula in niepokryte_reguly3:
    czesc_atrybutu = regula.split(": ")[1].split(" ==>")[0].strip()
    czesc_decyzji = regula.split("==>")[1].strip()
    pelna_regula = f"{czesc_atrybutu} ==> {czesc_decyzji}"

    if pelna_regula in unikalne_niepokryte_reguly3:
        unikalne_niepokryte_reguly3[pelna_regula] += 1
    else:
        unikalne_niepokryte_reguly3[pelna_regula] = 1

if len(niepokryte_reguly3) <= 1:
    print("\nKoniec dzialania algorytmu - znaleziono zero albo jedna regule III rzedu\n")
    print("Wszystkie reguly")
    print("Reguly I rzedu")
    for regula, licznik in unikalne_reguly.items():
        if licznik > 1:
            print(f"{regula}[{licznik}]")
        else:
            print(f"{regula}")
    print("Reguly II rzedu")
    for regula, licznik in unikalne_reguly2.items():
        if licznik > 1:
            print(f"{regula}[{licznik}]")
        else:
            print(f"{regula}")
    print("Reguly III rzedu")
    for regula in unikalne_niepokryte_reguly3:
        print(regula)