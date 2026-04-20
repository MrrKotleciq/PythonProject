from matplotlib import pyplot as plt
import numpy as np

import generate_random_num

def stopa_zwrotu(lista):
    
    print(lista)
    lista_zwrot = []

    for i in range(len(lista)-1):
        zwrot = (lista[i+1]-lista[i])*100/lista[i]
        lista_zwrot.append(zwrot)

    return lista_zwrot

if __name__ == '__main__':
    zwrot_array = stopa_zwrotu(generate_random_num.generuj_losewe(80,120))
    print(zwrot_array)