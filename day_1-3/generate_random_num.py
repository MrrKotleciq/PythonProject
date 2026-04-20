from matplotlib import pyplot as plt
import numpy as np

def generuj_losewe(low,up):

    ilosc_elementow = int(input("Podaj ilość elementów: "))
    lista_cen = []

    for i in range(ilosc_elementow):
        lista_cen.append(np.random.randint(low,up))
    
    return lista_cen

if __name__ == '__main__':
    
    lista = generuj_losewe(80,120)
    print(lista)