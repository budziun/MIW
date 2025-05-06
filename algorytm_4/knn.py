import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from collections import Counter

# baza danych iris
iris = datasets.load_iris()
X, y = iris.data, iris.target

# podzial danych iris - 70% treningowe, 30% testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

print(f"\nZbiór treningowy = {X_train.shape[0]} próbek")
print(f"Zbiór testowy {X_test.shape[0]} próbek\n")

# lista mettryk ktore beda testowane w petli for
metryki = ['euklidesowa', 'manhattan', 'cosinusowa']

# Metryki (euklidesowa, manhatan i cosinusowa
def metryka_euklidesowa(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))
def metryka_manhattan(x1, x2):
    return np.sum(np.abs(x1 - x2))
def metryka_cosinusowa(x1, x2):
    return 1 - np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))
class KNN:
    def __init__(self, k=3, metryka='euklidesowa'):
        # ilu sąsiadów i jaka metryka wybrana
        self.k = k
        self.metryka = metryka
    def trenuj(self, X, y):
        # zapameitanie ktore sa danymi testowymi
        self.X_train = X
        self.y_train = y
    def przewidywanie(self, X):
        # przewidywanie klasy dla każdej próbki w zbiorze testowym dlatego jest petla po X
        przewidywania = [self._przewidywanie(x) for x in X]
        return przewidywania
    def _przewidywanie(self, x):
        # obliczanie odleglosci od x do kazdej probki z zbioru testowego
        if self.metryka == 'euklidesowa':
            odleglosc = [metryka_euklidesowa(x, x_train) for x_train in self.X_train]
        elif self.metryka == 'manhattan':
            odleglosc = [metryka_manhattan(x, x_train) for x_train in self.X_train]
        elif self.metryka == 'cosinusowa':
            odleglosc = [metryka_cosinusowa(x, x_train) for x_train in self.X_train]

        # sortowanie w celu znalezienia najblizszych punktów (lub punktu jak k=1) wedlug odleglosci
        k_indeksy = np.argsort(odleglosc)[:self.k]
        # sprawdzamy etykiete klasy k najblizszych punktow
        k_najblizsze_etykiety = [self.y_train[i] for i in k_indeksy]
        # zliczanie ktora klasa jest najliczniejsza i wtedy decyzja ze zwracana jest klasa ktora wystepuje najczesciej wsrod sasiadow
        najczestsze = Counter(k_najblizsze_etykiety).most_common()
        return najczestsze[0][0]

for metryka in metryki:
    k = 3
    # tworzenie obiektu klasyfikatora i trenowanie go na danych treningowych
    klasyfikator = KNN(k=k, metryka=metryka)
    klasyfikator.trenuj(X_train, y_train)
    # przewidywanie klasy na danych treningowych
    przewidywania = klasyfikator.przewidywanie(X_test)

    #obliczanie i wyswietlanie dla kazdej metryki dokladnosci
    accuracy = np.sum(przewidywania == y_test) / len(y_test)
    print(f"Dokładność metryki {metryka} dla k={k}: {accuracy:.4%}\n")