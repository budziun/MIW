from collections import Counter
import itertools
from itertools import combinations

# import danych (6 paragonów) i wyswietlanie
d = [
    ['kapusta', 'ogórki', 'pomidory', 'kabaczki'],
    ['ogórki', 'pomidory', 'kabaczki'],
    ['cytryny', 'pomidory', 'woda'],
    ['cytryny', 'woda', 'jajka'],
    ['ogórki', 'grzybki', 'żołądkowa'],
    ['żołądkowa', 'ogórki', 'pomidory']
]
for row in d:
    print(row)

# ustalenie progu częstości
prog = 2

counter = Counter()
for row in d:
    counter.update(row)

# budowanie zbioru F1 w oparciu o prog czestosci
F1 = [item for item, count in counter.items() if count >= prog]
F1 = sorted(F1)

print("\nZbiór F1")
print(F1)

# kombinacje bez powtórzeń dla F1
C2 = list(itertools.combinations(F1, 2))
print("\nKombinacje bez powtórzeń C2:")
print(C2)

def licznik_d_para(para, d):
    count = 0
    for t in d:
        if para[0] in t and para[1] in t:
            count += 1
    return count

# budowanie F2 czyli pary z C2 które wystepuja w danych D
F2 = [para for para in C2 if licznik_d_para(para, d) >= prog]

print("\nF2:")
print(F2)

# tworzenie kombinacji c3 jezeli na pierwszej pozycji w f2 wystepuje minimum prog razy
C3 = []
for i in range(len(F2)):
    for j in range(i + 1, len(F2)):
        a1, a2 = F2[i]
        b1, b2 = F2[j]
        # sprawdzenie czy jest taki sam pierwszy element w obu sprawdzanych
        if a1 == b1:
            # tworzenie i dodawanie do c3 trzech elementow (element wspolny 1 i pozsotale 2 oraz 3)
            candidate = tuple(set([a1, a2, b2]))
            if candidate not in C3:
                C3.append(candidate)

print("\nC3: ")
print(C3)
F2_set = set(F2)

F3 = []
for i in C3:
    pary = list(combinations(i, prog))
    pary = [tuple(sorted(p)) for p in pary]
    if all(para in F2_set for para in pary):
        F3.append(i)

print("\nPo zastosowaniu własności Apriori, kandydaci pozostali w F3:")
print(F3)

