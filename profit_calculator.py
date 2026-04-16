
def main():

    print("Zysk wynsi:" + get_calculated_profit(10000,2))


# funkcja liczaca zysk z kapitalu i procentu
def get_calculated_profit(kapital, procent):
    zysk = kapital * procent
    return zysk

if __name__ == '__main__':
    main()