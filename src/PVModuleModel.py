import random

lista_di_liste = []
num_liste = 24  # Numero di liste da generare

for _ in range(num_liste):
    lunghezza_lista = 10  # Lunghezza casuale della lista
    nuova_lista = [random.randint(0, 2000) for _ in range(lunghezza_lista)]
    lista_di_liste.append(nuova_lista)

print(lista_di_liste)
