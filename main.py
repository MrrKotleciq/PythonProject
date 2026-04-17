from matplotlib import pyplot as plt
import numpy as np

import profit_calculator
import generate_random_num
import zwrot_proc

if __name__ == '__main__':

    lista_cen = generate_random_num.generuj_losewe(40,75)

    zwrot = zwrot_proc.stopa_zwrotu(lista_cen)

    srednia = np.mean(lista_cen)
    zmiennosc = np.std(zwrot)

    print(lista_cen)
    print("Średnia cen to:", srednia)
    print("Zmienność cen to:", zmiennosc, "p%")