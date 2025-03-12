#       a1 a2 a3 a4 a5 a6  d
#    o1 [1, 1, 1, 1, 3, 1, 1]
#    o2 [1, 1, 1, 1, 3, 2, 1]
#    o3 [1, 1, 1, 3, 2, 1, 0]
#    o4 [1, 1, 1, 3, 3, 2, 1]
#    o5 [1, 1, 2, 1, 2, 1, 0]
#    o6 [1, 1, 2, 1, 2, 2, 1]
#    o7 [1, 1, 2, 2, 3, 1, 0]
#    o8 [1, 1, 2, 2, 4, 1, 1]

file = open("values.txt", "r")

data = []
for line in file:
    data.append([int(d) for d in line.split()])

kolumny = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
wiersze = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8"]

x = len(kolumny)
y = len(wiersze)

print("Kolumny", x)
print("Wiersze", y)

# stworzenie listy dla regul co wyjda i dla bazy danych aby modyfikowac kopie
reguly = []
obiekty = []

for i in range(len(data)):
    obiekty.append([i, data[i]])

# lista obiektów do rozważenia
obiekty2 = list(range(len(data)))

print("Reguły I rzędu")

for indeks in range(len(data)):
    # jesli obiekt juz usuniety to pominac
    if indeks not in obiekty2:
        continue
    # obj[-1] to kolumna z decyzja
    obj = data[indeks]
    decyzja = obj[-1]
    regula_znaleziona = False

    # sprawdzenie kazdego atrybutu oprocz decyzji
    for indeks2 in range(len(kolumny) - 1):
        wartosc = obj[indeks2]
        pokryte_obiekty = []

        # sprawdzenie czy reguła jest niesprzeczna
        czy_pokryty = True
        for sprawdzone_indeksy in range(len(data)):
            sprawdzone_obiekty = data[sprawdzone_indeksy]
            # jesli obiekt ma te sama wartosc atrybutu ale inna decyzje to regula jest sprzeczna
            if sprawdzone_obiekty[indeks2] == wartosc:
                if sprawdzone_obiekty[-1] != decyzja:
                    czy_pokryty = False
                    break
                # jesli jest ta sama decyzja to obiekt jest pokryty przez regule
                else:
                    pokryte_obiekty.append(sprawdzone_indeksy)

        # sprawdzamy czy_pokryty po sprawdzeniu wszystkich obiektów
        if czy_pokryty and pokryte_obiekty:
            regula_tekst = f"({kolumny[indeks2]} = {wartosc}) ==> (d = {decyzja})"
            if len(pokryte_obiekty) > 1:
                regula_tekst += f"[{len(pokryte_obiekty)}]"

            # dodawanie reguly do listy
            reguly.append(([(indeks2, wartosc)], decyzja, pokryte_obiekty))

            print(f"z {wiersze[indeks]} {regula_tekst}, wyrzucamy z rozważań obiekty {', '.join([wiersze[idx] for idx in pokryte_obiekty])}.")

            # Usuwanie pokrytych obiektów z rozważań
            for pokryte_indeksy in pokryte_obiekty:
                if pokryte_indeksy in obiekty2:
                    obiekty2.remove(pokryte_indeksy)

            regula_znaleziona = True
            break

    # Jeżeli nie ma reguly znalezionej
    if not regula_znaleziona:
        print(f"z {wiersze[indeks]} Nie mo")

print("Reguły II rzędu")

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

            if czy_pokryty and pokryte_obiekty:
                regula_tekst = f"({kolumny[indeks3]} = {indeks3_wartosc}) ∧ ({kolumny[indeks4]} = {indeks4_wartosc}) ==> (d = {decyzja})"
                if len(pokryte_obiekty) > 1:
                    regula_tekst += f"[{len(pokryte_obiekty)}]"

                reguly.append(([(indeks3, indeks3_wartosc), (indeks4, indeks4_wartosc)], decyzja, pokryte_obiekty))

                print(
                    f"z {wiersze[indeks]} {regula_tekst}, wyrzucamy z rozważań obiekt {', '.join([wiersze[idx] for idx in pokryte_obiekty])}")

                for pokryte_indeksy in pokryte_obiekty:
                    if pokryte_indeksy in obiekty2:
                        obiekty2.remove(pokryte_indeksy)

                regula_znaleziona = True
                break

        if regula_znaleziona:
            break

    if not regula_znaleziona and indeks in obiekty2:
        print(f"z {wiersze[indeks]} Nie mo - wszystkie kombinacje sprzeczne")

# Sprawdzenie czy wszystkie obiekty zostaly pokryte
if obiekty2:
    print("Niepokryte obiekty: ")
    for idx in obiekty2:
        print(f"{wiersze[idx]}: {data[idx]}")
else:
    print("Wszystkie obiekty pokryte :)")

# Podsumowanie
print("Wygenerowane reguły I i II rzędu")
for j, (reguły_warunki, decyzja, pokryte_obiekty) in enumerate(reguly):
    if len(reguły_warunki) == 1:
        indeks2, wartosc = reguły_warunki[0]
        regula2 = f"({kolumny[indeks2]} = {wartosc}) ==> (d = {decyzja})"
    else:
        regula2 = " ∧ ".join([f"({kolumny[indeks2]} = {wartosc})" for indeks2, wartosc in reguły_warunki])
        regula2 += f" ==> (d= {decyzja})"

    print(f"Reguła {j+1}: {regula2}")