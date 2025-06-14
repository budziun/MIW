lista_obiektow = []
kolumny_a = ["pogoda", "temperatura", "wilgotnosc", "wiatr"]
with open("SystemDecyzyjny.txt", "r") as plik:
    linijki = plik.readlines()
    for linijka in linijki:
        elementy = linijka.strip().split()
        if len(elementy) >= 6:
            wiersz_danych = {}
            indeks_obiektu = elementy[0]
            for i in range(len(kolumny_a)):
                wiersz_danych[kolumny_a[i]] = elementy[i + 1]
            wiersz_danych["d"] = elementy[-1]

            wiersz_danych["indeks"] = indeks_obiektu
            lista_obiektow.append(wiersz_danych)
for obiekt in lista_obiektow:
    print(obiekt)

wynikowe_reguly = []
juz_uzyte_obiekty = []
ilosc_pasujacych = 0
for rozmiar_grupy in range(1, len(kolumny_a) + 1):
    wszystkie_grupy = []
    if rozmiar_grupy == 1:
        for kolumna in kolumny_a:
            wszystkie_grupy.append([kolumna])
    elif rozmiar_grupy == 2:
        for i in range(len(kolumny_a)):
            for j in range(i + 1, len(kolumny_a)):
                wszystkie_grupy.append([kolumny_a[i], kolumny_a[j]])
    elif rozmiar_grupy == 3:
        for i in range(len(kolumny_a)):
            for j in range(i + 1, len(kolumny_a)):
                for k in range(j + 1, len(kolumny_a)):
                    wszystkie_grupy.append([kolumny_a[i], kolumny_a[j], kolumny_a[k]])
    elif rozmiar_grupy == 4:
        for i in range(len(kolumny_a)):
            for j in range(i + 1, len(kolumny_a)):
                for k in range(j + 1, len(kolumny_a)):
                    for l in range(k + 1, len(kolumny_a)):
                        wszystkie_grupy.append([kolumny_a[i], kolumny_a[j], kolumny_a[k], kolumny_a[l]])
    for indeks_obiektu in range(len(lista_obiektow)):
        if indeks_obiektu in juz_uzyte_obiekty:
            continue
        biezacy_obiekt = lista_obiektow[indeks_obiektu]
        for grupa_atrybutow in wszystkie_grupy:
            if indeks_obiektu in juz_uzyte_obiekty:
                continue
            jest_sprzecznosc = False
            for inny_indeks in range(len(lista_obiektow)):
                if indeks_obiektu == inny_indeks:
                    continue
                porownywany_obiekt = lista_obiektow[inny_indeks]
                wszystkie_zgodne = True
                for atrybut in grupa_atrybutow:
                    if biezacy_obiekt[atrybut] != porownywany_obiekt[atrybut]:
                        wszystkie_zgodne = False
                        break
                if wszystkie_zgodne and biezacy_obiekt["d"] != porownywany_obiekt["d"]:
                    jest_sprzecznosc = True
                    break
            if jest_sprzecznosc:
                continue
            ilosc_pasujacych = 0
            nowo_pokryte = []
            for inny_indeks in range(len(lista_obiektow)):
                porownywany_obiekt = lista_obiektow[inny_indeks]
                pasuje = True
                for atrybut in grupa_atrybutow:
                    if biezacy_obiekt[atrybut] != porownywany_obiekt[atrybut]:
                        pasuje = False
                        break
                if pasuje:
                    ilosc_pasujacych += 1
                    if inny_indeks not in juz_uzyte_obiekty:
                        nowo_pokryte.append(inny_indeks)
            tekst_reguly = f"z D{indeks_obiektu+1}: "
            tekst_reguly += f"{''.join(f'({a}={biezacy_obiekt[a]})' for a in grupa_atrybutow)} -> (d={biezacy_obiekt['d']})"
            if ilosc_pasujacych > 1:
                tekst_reguly += '[' + f"{ilosc_pasujacych}" + ']'
            if tekst_reguly not in wynikowe_reguly:
                wynikowe_reguly.append(tekst_reguly)
                juz_uzyte_obiekty.extend(nowo_pokryte)
for regula in wynikowe_reguly:
    print(regula)