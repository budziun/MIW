file = open("SystemDecyzyjny.txt", "r")

content = file.read().strip()
file.close()

lines = content.splitlines()
data = []
wiersze = []

for line in lines:
    if not line.strip():
        continue

    parts = line.split(' ', 1)

    if len(parts) < 2:
        print(f"Nieprawidłowy tekst, pomijam: {line}")
        continue

    wiersz_id = parts[0]
    wiersze.append(wiersz_id)

    elementy = parts[1].strip().split(' ')

    if len(elementy) < 1:
        print(f"Uwaga: Wiersz {wiersz_id} nie ma elementów")
        continue

    # Ostatni element to decyzja (Tak/Nie)
    decyzja = 1 if elementy[-1] == "Tak" else 0

    # Reszta to atrybuty
    atrybuty = elementy[:-1]

    # Dodaj wiersz danych
    data.append(atrybuty + [decyzja])

kolumny = ["Pogoda", "Temperatura", "Wilgotnosc", "Wiatr", "d"]

x = len(kolumny)
y = len(wiersze)

print("Liczba Kolumn:", x)
print("Liczba Wierszy:", y)
print("Dane po przetworzeniu:")
for i, row in enumerate(data):
    print(f"{wiersze[i]}: {row}")

# Stworzenie listy dla reguł
reguly = []
obiekty = []

for i in range(len(data)):
    obiekty.append([i, data[i]])

# Lista obiektów do rozważenia
obiekty2 = list(range(len(data)))

print("Reguły I rzędu")

for indeks in range(len(data)):
    # Jeśli obiekt już usunięty to pominąć
    if indeks not in obiekty2:
        continue
    # obj[-1] to kolumna z decyzją
    obj = data[indeks]
    decyzja = obj[-1]
    regula_znaleziona = False

    # Sprawdzenie każdego atrybutu oprócz decyzji
    for indeks2 in range(len(kolumny) - 1):
        wartosc = obj[indeks2]
        pokryte_obiekty = []

        # Sprawdzenie czy reguła jest niesprzeczna
        czy_pokryty = True
        for sprawdzone_indeksy in range(len(data)):
            sprawdzone_obiekty = data[sprawdzone_indeksy]
            # Jeśli obiekt ma tę samą wartość atrybutu ale inną decyzję to reguła jest sprzeczna
            if sprawdzone_obiekty[indeks2] == wartosc:
                if sprawdzone_obiekty[-1] != decyzja:
                    czy_pokryty = False
                    break
                # Jeśli jest ta sama decyzja to obiekt jest pokryty przez regułę
                else:
                    pokryte_obiekty.append(sprawdzone_indeksy)

        # Sprawdzamy czy_pokryty po sprawdzeniu wszystkich obiektów
        if czy_pokryty and pokryte_obiekty:
            decyzja_tekst = "Tak" if decyzja == 1 else "Nie"
            regula_tekst = f"({kolumny[indeks2]} = {wartosc}) ==> (d = {decyzja_tekst})"
            if len(pokryte_obiekty) > 1:
                regula_tekst += f"[{len(pokryte_obiekty)}]"

            # Dodawanie reguły do listy
            reguly.append(([(indeks2, wartosc)], decyzja, pokryte_obiekty))

            print(
                f"z {wiersze[indeks]} {regula_tekst}, wyrzucamy z rozważań obiekty {', '.join([wiersze[idx] for idx in pokryte_obiekty])}.")

            # Usuwanie pokrytych obiektów z rozważań
            for pokryte_indeksy in pokryte_obiekty:
                if pokryte_indeksy in obiekty2:
                    obiekty2.remove(pokryte_indeksy)

            regula_znaleziona = True
            break

    if not regula_znaleziona:
        print(f"z {wiersze[indeks]} Nie mo")

print("\nReguły II rzędu")

for indeks in range(len(data)):
    if indeks not in obiekty2:
        continue

    obj = data[indeks]
    decyzja = obj[-1]
    regula_znaleziona = False

    for indeks3 in range(len(kolumny) - 1):
        for indeks4 in range(indeks3 + 1, len(kolumny) - 1):
            indeks3_wartosc = obj[indeks3]
            indeks4_wartosc = obj[indeks4]
            pokryte_obiekty = []

            czy_pokryty = True
            for sprawdzone_indeksy in range(len(data)):
                sprawdzone_obiekty = data[sprawdzone_indeksy]
                if sprawdzone_obiekty[indeks3] == indeks3_wartosc and sprawdzone_obiekty[indeks4] == indeks4_wartosc:
                    if sprawdzone_obiekty[-1] != decyzja:
                        czy_pokryty = False
                        break
                    else:
                        pokryte_obiekty.append(sprawdzone_indeksy)

            # Sprawdzamy czy_pokryty po sprawdzeniu wszystkich obiektów
            if czy_pokryty and pokryte_obiekty:
                decyzja_tekst = "Tak" if decyzja == 1 else "Nie"
                regula_tekst = f"({kolumny[indeks3]} = {indeks3_wartosc}) ∧ ({kolumny[indeks4]} = {indeks4_wartosc}) ==> (d = {decyzja_tekst})"
                if len(pokryte_obiekty) > 1:
                    regula_tekst += f"[{len(pokryte_obiekty)}]"

                reguly.append(([(indeks3, indeks3_wartosc), (indeks4, indeks4_wartosc)], decyzja, pokryte_obiekty))

                print(
                    f"z {wiersze[indeks]} {regula_tekst}, wyrzucamy z rozważań obiekty {', '.join([wiersze[idx] for idx in pokryte_obiekty])}")

                for pokryte_indeksy in pokryte_obiekty:
                    if pokryte_indeksy in obiekty2:
                        obiekty2.remove(pokryte_indeksy)

                regula_znaleziona = True
                break

        if regula_znaleziona:
            break

    if not regula_znaleziona and indeks in obiekty2:
        print(f"z {wiersze[indeks]} Nie mo - wszystkie kombinacje sprzeczne")

# Sprawdzenie czy wszystkie obiekty zostały pokryte
if obiekty2:
    print("\nNiepokryte obiekty: ")
    for idx in obiekty2:
        print(f"{wiersze[idx]}: {data[idx]}")
else:
    print("\nWszystkie obiekty pokryte :)")

# Podsumowanie
print("\nWygenerowane reguły I i II rzędu")
for j, (reguły_warunki, decyzja, pokryte_obiekty) in enumerate(reguly):
    decyzja_tekst = "Tak" if decyzja == 1 else "Nie"
    if len(reguły_warunki) == 1:
        indeks2, wartosc = reguły_warunki[0]
        regula2 = f"({kolumny[indeks2]} = {wartosc}) ==> (d = {decyzja_tekst})"
    else:
        regula2 = " ∧ ".join([f"({kolumny[indeks2]} = {wartosc})" for indeks2, wartosc in reguły_warunki])
        regula2 += f" ==> (d = {decyzja_tekst})"

    print(f"Reguła {j + 1}: {regula2}")