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
print(data)

cols_d = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
rows_d = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8"]

x = len(cols_d)
y = len(rows_d)

print("Szerokość",x)
print("Wysokość",y)

for i in range(y):
    for j in range(x):
        print(f'Wartość w {rows_d[i]} {cols_d[j]}: {data[i][j]}')