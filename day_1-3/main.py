from matplotlib import pyplot as plt
import numpy as np

import profit_calculator
import generate_random_num
import return_proc

if __name__ == '__main__':

    lista_cen = generate_random_num.generuj_losewe(40,75)

    return = return_proc.stopa_returnu(lista_cen)

    srednia = np.mean(lista_cen)
    zmiennosc = np.std(return)

    print(lista_cen)
    print("Średnia cen to:", srednia)
    print("Zmienność cen to:", zmiennosc, "p%")