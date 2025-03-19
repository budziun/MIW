#       a1 a2 a3 a4 a5 a6  d
#    o1 [1, 1, 1, 1, 3, 1, 1]
#    o2 [1, 1, 1, 1, 3, 2, 1]
#    o3 [1, 1, 1, 3, 2, 1, 0]
#    o4 [1, 1, 1, 3, 3, 2, 1]
#    o5 [1, 1, 2, 1, 2, 1, 0]
#    o6 [1, 1, 2, 1, 2, 2, 1]
#    o7 [1, 1, 2, 2, 3, 1, 0]
#    o8 [1, 1, 2, 2, 4, 1, 1]
wiersze2 = {
    "o1": [1, 1, 1, 1, 3, 1, 1],
    "o2": [1, 1, 1, 1, 3, 2, 1],
    "o3": [1, 1, 1, 3, 2, 1, 0],
    "o4": [1, 1, 1, 3, 3, 2, 1],
    "o5": [1, 1, 2, 1, 2, 1, 0],
    "o6": [1, 1, 2, 1, 2, 2, 1],
    "o7": [1, 1, 2, 2, 3, 1, 0],
    "o8": [1, 1, 2, 2, 4, 1, 1]
}

import numpy as np

file = open("values.txt", "r")

data = []
for line in file:
    data.append([int(d) for d in line.split()])

kolumny = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
wiersze = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8"]
x = len(kolumny)
y = len(wiersze)

print(kolumny)
for i in range(y):
   print(f"{wiersze[i]} [{'[' + ','.join(map(str, data[i]))  + ']' if i < x - 1 else '[' + ','.join(map(str, data[i]))  + ']'}")

# macierz wierszeXwiersze (tu 8x8) nieodroznialnsoci
mac = np.zeros((y, y), dtype=object)
np.fill_diagonal(mac, 'X')

print(mac)

for i in range(y):
    for j in range(i+1,y):
            mac[i,j] = "X"
            mac[j,i] = "X"

print(mac)