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

