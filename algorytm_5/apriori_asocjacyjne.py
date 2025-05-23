from collections import Counter
import itertools
from itertools import combinations

# Dane wejściowe - transakcje (paragony)
d = [
    ['kapusta', 'ogórki', 'pomidory', 'kabaczki'],
    ['ogórki', 'pomidory', 'kabaczki'],
    ['cytryny', 'pomidory', 'woda'],
    ['cytryny', 'woda', 'jajka'],
    ['ogórki', 'grzybki', 'żołądkowa'],
    ['żołądkowa', 'ogórki', 'pomidory']
]
print("D:")
for row in d:
    print(row)
# Próg częstości
prog = 2

# zliczanie wystąpienia zbioru elementów w danych
def count_occurrences(itemset, transactions):
    count = 0
    for transaction in transactions:
        if all(item in transaction for item in itemset):
            count += 1
    return count

# budowanie zbioru F1 w oparciu o prog czestosci
counter = Counter()
for transaction in d:
    counter.update(transaction)

F1 = [item for item, count in counter.items() if count >= prog]
F1.sort()

print("\nF1:")
print(F1)

# lista dla wszystkich zbiorów częstych
wszystkie_zbiory_czeste = []
wszystkie_zbiory_czeste.append(F1)

# Start od k=2 (Fk, Ck np. F2 i C2 itd...)
k = 2
aktualne_czeste = F1

while True:
    # Generowanie Ck na podstawie Fk-1
    kandydaci = list(combinations(F1, k))
    print(f"\nC{k}:")
    print(kandydaci)

    # Sprawdzanie częstości kandydatów - tworzenie Fk
    czeste_zbiory = []
    for kandydat in kandydaci:
        if count_occurrences(kandydat, d) >= prog:
            # dla k>2 sprawdzamy własność Apriori
            if k > 2:
                # wszystkie podzbiory o długości k-1 muszą być częste
                poprawny = True
                for podzbior in combinations(kandydat, k - 1):
                    # sprawdzamy czy podzbiór jest w poprzednim zbiorze częstym
                    if podzbior not in wszystkie_zbiory_czeste[-1]:
                        poprawny = False
                        break
                if not poprawny:
                    continue
            czeste_zbiory.append(kandydat)

    print(f"F{k}:")
    print(czeste_zbiory)

    # jeśli znaleziono tylko jeden = koniec algorytmu
    if not czeste_zbiory or len(czeste_zbiory) <= 1:
        if czeste_zbiory:
            wszystkie_zbiory_czeste.append(czeste_zbiory)  # dodajemy ostatni zbiór
            print(f"\nAlgorytm zakończony - znaleziono jeden zbiór częsty w F{k}: {czeste_zbiory[0]}")
        break

    wszystkie_zbiory_czeste.append(czeste_zbiory)
    k += 1

print("\nWszystkie znalezione zbiory dla d")
for i, j in enumerate(wszystkie_zbiory_czeste, 1):
    print(f"F{i} (zbiory {i}-elementowe): {j}")

print("\nREGUŁY ASOCJACYJNE")

# funkcja do liczenia wsparcia reguły
def wsparcie_reguly(poprzednik, nastepnik, transactions):
    # liczba transakcji gdzie występuje poprzednik => następnik
    licznik_reguly = 0
    for transaction in transactions:
        # sprawdzamy czy wszystkie elementy poprzednika są w transakcji
        if all(item in transaction for item in poprzednik):
            # sprawdzamy czy wszystkie elementy następnika też są
            if all(item in transaction for item in nastepnik):
                licznik_reguly += 1
    # wsparcie = liczba pasujących / wszystkie transakcje
    return licznik_reguly / len(transactions)


# funkcja do liczenia ufności reguły
def ufnosc_reguly(poprzednik, nastepnik, transactions):
    # liczba transakcji gdzie występuje poprzednik => następnik
    licznik_reguly = 0
    # liczba transakcji gdzie występuje sam poprzednik
    licznik_poprzednika = 0

    for transaction in transactions:
        poprzednik_pasuje = all(item in transaction for item in poprzednik)
        if poprzednik_pasuje:
            licznik_poprzednika += 1
            # sprawdzamy też następnik
            if all(item in transaction for item in nastepnik):
                licznik_reguly += 1

    # ufność = liczba z regułą / liczba z poprzednikiem
    if licznik_poprzednika == 0:
        return 0
    return licznik_reguly / licznik_poprzednika


# generowanie wszystkich reguł ze zbiorów częstych
wszystkie_reguly = []

# przechodzimy przez wszystkie zbiory częste oprócz F1 (bo potrzebujemy min 2 elementy)
for i in range(1, len(wszystkie_zbiory_czeste)):
    for zbior_czesty in wszystkie_zbiory_czeste[i]:
        # dla każdego zbioru częstego generujemy reguły
        # poprzednik ma k-1 elementów, następnik 1 element
        k = len(zbior_czesty)

        # generujemy wszystkie możliwe podzbiory o wielkości k-1 jako poprzedniki
        for poprzednik in combinations(zbior_czesty, k - 1):
            # następnik to element którego brakuje
            nastepnik = []
            for element in zbior_czesty:
                if element not in poprzednik:
                    nastepnik.append(element)

            # liczymy parametry reguły
            wsp = wsparcie_reguly(poprzednik, nastepnik, d)
            ufn = ufnosc_reguly(poprzednik, nastepnik, d)
            jakosc = wsp * ufn

            # zapisujemy regułę
            regula = {
                'poprzednik': poprzednik,
                'nastepnik': nastepnik,
                'wsparcie': wsp,
                'ufnosc': ufn,
                'jakosc': jakosc
            }
            wszystkie_reguly.append(regula)

# sortujemy reguły według jakości (malejąco)
wszystkie_reguly.sort(key=lambda x: x['jakosc'], reverse=True)

# wyświetlamy wszystkie reguły
print("\nWszystkie wygenerowane reguły:")
for regula in wszystkie_reguly:
    poprzednik_str = ' ∧ '.join(regula['poprzednik'])
    nastepnik_str = ' ∧ '.join(regula['nastepnik'])
    print(f"{poprzednik_str} => {nastepnik_str}")
    print(f"  wsparcie = {regula['wsparcie']:.3f}, ufność = {regula['ufnosc']:.3f}, jakość = {regula['jakosc']:.3f}")

# próg jakości reguł (wsparcie * ufność)
prog_jakosci = 0.3 # czyli 1/3

print(f"\n\nReguły dla progu jakości >= {prog_jakosci}:")

licznik_regul = 0
for regula in wszystkie_reguly:
    if regula['jakosc'] >= prog_jakosci:
        poprzednik_str = ' ∧ '.join(regula['poprzednik'])
        nastepnik_str = ' ∧ '.join(regula['nastepnik'])
        print(f"{poprzednik_str} => {nastepnik_str}")
        print(
            f"  wsparcie = {regula['wsparcie']:.3f}, ufność = {regula['ufnosc']:.3f}, jakość = {regula['jakosc']:.3f}")
        licznik_regul += 1

print(f"\nLiczba reguł spełniających próg: {licznik_regul}")