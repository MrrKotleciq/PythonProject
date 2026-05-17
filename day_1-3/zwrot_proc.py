from matplotlib import pyplot as plt
import numpy as np

import generate_random_num

def stopa_returnu(lista):
    
    print(lista)
    lista_return = []

    for i in range(len(lista)-1):
        return = (lista[i+1]-lista[i])*100/lista[i]
        lista_return.append(return)

    return lista_return

if __name__ == '__main__':
    return_array = stopa_returnu(generate_random_num.generuj_losewe(80,120))
    print(return_array)