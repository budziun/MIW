obiekty = []
atrybuty = ["a1", "a2", "a3", "a4"]
with open("SystemDecyzyjny.txt", "r") as plik:
    linijki = plik.readlines()

    for linijka in linijki:
        elementy = linijka.strip().split()

        ### ID Pogoda Temperatura Wilgotnosc Wiatr Decyzja
        id_obiektu = elementy[0]

        obiekt = {
            "id": id_obiektu,
            "a1": elementy[1],  # Pogoda
            "a2": elementy[2],  # Temperatura
            "a3": elementy[3],  # Wilgotnosc
            "a4": elementy[4],  # Wiatr
            "d": elementy[5]  # Decyzja
        }

        obiekty.append(obiekt)

print("Wczytane obiekty:")
for obiekt in obiekty:
    print(f"{obiekt['id']}: {obiekt}")

decyzje = {}
for obiekt in obiekty:
    decyzja = obiekt['d']
    if decyzja not in decyzje:
        decyzje[decyzja] = []
    decyzje[decyzja].append(obiekt)

print(f"\nZnalezione decyzje: {list(decyzje.keys())}")

nazwy_atrybutow = {
    "a1": "Pogoda",
    "a2": "Temperatura",
    "a3": "Wilgotnosc",
    "a4": "Wiatr"
}

wszystkie_reguly = []

# Dla każdej decyzji generujemy reguły
for decyzja in decyzje:
    print(f"\n\nLEM2 - Koncept {decyzja}")

    obiekty_decyzji = decyzje[decyzja]

    obiekty_inne = []
    for inna_decyzja in decyzje:
        if inna_decyzja != decyzja:
            obiekty_inne.extend(decyzje[inna_decyzja])

    print(f"\nObiekty z decyzją {decyzja}:")
    for o in obiekty_decyzji:
        print(f"{o['id']}: {o}")

    reguly = []
    pokrycia_regul = []
    niepokryte = list(range(len(obiekty_decyzji)))

    while len(niepokryte) > 0:
        print(f"\nNiepokryte obiekty: {[obiekty_decyzji[i]['id'] for i in niepokryte]}")

        regula = {}
        aktualne_obiekty = niepokryte.copy()
        print(f"Rozważane obiekty: {[obiekty_decyzji[i]['id'] for i in aktualne_obiekty]}")

        while aktualne_obiekty:
            jest_spojna = True
            for obj_inny in obiekty_inne:
                pokryty = True
                for atr, wart in regula.items():
                    if obj_inny[atr] != wart:
                        pokryty = False
                        break
                if pokryty:
                    jest_spojna = False
                    break

            if jest_spojna and len(aktualne_obiekty) > 0:
                break

            najlepszy_atrybut = None
            najlepsza_wartosc = None
            najlepszy_wynik = 0
            najlepsze_pokryte = []

            for atrybut in atrybuty:
                if atrybut in regula:
                    continue

                licznik_wartosci = {}
                for i in aktualne_obiekty:
                    wartosc = obiekty_decyzji[i][atrybut]
                    if wartosc not in licznik_wartosci:
                        licznik_wartosci[wartosc] = []
                    licznik_wartosci[wartosc].append(i)

                # Wybieramy wartości ktora jest najczęsciej
                for wartosc, pokryte in licznik_wartosci.items():
                    if len(pokryte) > najlepszy_wynik:
                        najlepszy_atrybut = atrybut
                        najlepsza_wartosc = wartosc
                        najlepszy_wynik = len(pokryte)
                        najlepsze_pokryte = pokryte
                    # Jezeli remis to wybor tej co jest pierwsza w tabeli
                    elif len(pokryte) == najlepszy_wynik and najlepszy_atrybut is not None and atrybuty.index(
                            atrybut) < atrybuty.index(najlepszy_atrybut):
                        najlepszy_atrybut = atrybut
                        najlepsza_wartosc = wartosc
                        najlepszy_wynik = len(pokryte)
                        najlepsze_pokryte = pokryte

            if najlepszy_atrybut is not None:
                regula[najlepszy_atrybut] = najlepsza_wartosc
                aktualne_obiekty = najlepsze_pokryte

                print(f"Dodajemy warunek ({nazwy_atrybutow[najlepszy_atrybut]}={najlepsza_wartosc})")
                print(f"Zawężamy poszukiwania do: {[obiekty_decyzji[i]['id'] for i in aktualne_obiekty]}")
            else:
                print("Nie znaleziono odpowiedniego warunku")
                break

        sprzecznosc_wszystkich = False
        if len(regula) == len(atrybuty):
            pokryte_z_innych = []
            for obj_inny in obiekty_inne:
                pokryty = True
                for atr, wart in regula.items():
                    if obj_inny[atr] != wart:
                        pokryty = False
                        break
                if pokryty:
                    pokryte_z_innych.append(obj_inny['id'])

            if pokryte_z_innych:
                sprzecznosc_wszystkich = True
                print(
                    f"Wykryto sprzeczność na wszystkich atrybutach! Obiekty pokryte z innych decyzji: {pokryte_z_innych}")

        if regula:
            pokryte_obiekty = []
            for i, obj in enumerate(obiekty_decyzji):
                pokryty = True
                for atr, wart in regula.items():
                    if obj[atr] != wart:
                        pokryty = False
                        break
                if pokryty:
                    pokryte_obiekty.append(i)

            reguly.append(regula)
            pokrycia_regul.append(len(pokryte_obiekty))

            print("Utworzona reguła: ", end="")
            for i, (atr, wart) in enumerate(regula.items()):
                if i > 0:
                    print(" I ", end="")
                print(f"({nazwy_atrybutow[atr]}={wart})", end="")

            if sprzecznosc_wszystkich:
                alternatywa_decyzji = " -> ("
                for i, d in enumerate(decyzje.keys()):
                    if i > 0:
                        alternatywa_decyzji += " ∨ "
                    alternatywa_decyzji += f"Decyzja={d}"
                alternatywa_decyzji += ")"
                print(alternatywa_decyzji)
            else:
                print(f" -> (Decyzja={decyzja})")

            nowe_niepokryte = []
            for i in niepokryte:
                pokryty = True
                for atr, wart in regula.items():
                    if obiekty_decyzji[i][atr] != wart:
                        pokryty = False
                        break
                if not pokryty:
                    nowe_niepokryte.append(i)
                else:
                    print(f"Obiekt {obiekty_decyzji[i]['id']} został pokryty, usuwamy go z niepokrytych")

            niepokryte = nowe_niepokryte
        else:
            print(f"Nie udało się utworzyć reguły, usuwamy obiekt {obiekty_decyzji[niepokryte[0]]['id']}")
            niepokryte.pop(0)

    print(f"\nReguły dla konceptu Decyzja={decyzja}:")
    for i, (regula, pokrycie) in enumerate(zip(reguly, pokrycia_regul), 1):
        napis_reguly = f"Reguła {i}: "

        sprzecznosc = False
        if len(regula) == len(atrybuty):
            for obj_inny in obiekty_inne:
                pokryty = True
                for atr, wart in regula.items():
                    if obj_inny[atr] != wart:
                        pokryty = False
                        break
                if pokryty:
                    sprzecznosc = True
                    break

        for j, (atrybut, wartosc) in enumerate(regula.items()):
            if j > 0:
                napis_reguly += " ∧ "
            napis_reguly += f"({nazwy_atrybutow[atrybut]}={wartosc})"

        if sprzecznosc:
            napis_reguly += " -> ("
            for j, d in enumerate(decyzje.keys()):
                if j > 0:
                    napis_reguly += " ∨ "
                napis_reguly += f"Decyzja={d}"
            napis_reguly += ")"
        else:
            if pokrycie > 1:
                napis_reguly += f" -> (Decyzja={decyzja})[{pokrycie}]"
            else:
                napis_reguly += f" -> (Decyzja={decyzja})"

        print(napis_reguly)
        wszystkie_reguly.append((f"Reguła{len(wszystkie_reguly) + 1}", regula, decyzja, pokrycie, sprzecznosc))

print("\nWszystkie reguły:")
for i, (id_reguly, regula, decyzja, pokrycie, sprzecznosc) in enumerate(wszystkie_reguly, 1):
    napis_reguly = f"{id_reguly} "

    for j, (atrybut, wartosc) in enumerate(regula.items()):
        if j > 0:
            napis_reguly += " ∧ "
        napis_reguly += f"({nazwy_atrybutow[atrybut]} = {wartosc})"

    if sprzecznosc:
        napis_reguly += " => ("
        for j, d in enumerate(decyzje.keys()):
            if j > 0:
                napis_reguly += " ∨ "
            napis_reguly += f"Decyzja = {d}"
        napis_reguly += ")"
    else:
        if pokrycie > 1:
            napis_reguly += f" => (Decyzja = {decyzja})[{pokrycie}]"
        else:
            napis_reguly += f" => (Decyzja = {decyzja})"

    print(napis_reguly)