wagiPaczek = [10, 15, 7, 20, 5, 8, 10, 3, 18, 17, 6, 9, 22, 21, 17]
max = 25

def podzielPaczki(wagi, max):
    wagiSort = sorted(wagi, reverse = True)
    kursy = []
    for waga in wagi:
        if waga > max:
            raise ValueError(f"Paczka {waga} przekracza maksymalną wagę")

    for waga in wagiSort:
        dodano = False
        for kurs in kursy:
            if sum(kurs) + waga <= max:
                kurs.append(waga)
                dodano = True
                break
        if not dodano:
            kursy.append([waga])

    return len(kursy), kursy

if __name__ == "__main__":
    liczbaKursow, kursy = podzielPaczki(wagiPaczek, max)
    print(f"Liczba kursów: ", liczbaKursow)
    for i, kurs in enumerate(kursy, 1):
        print(f"Kurs {i}: {kurs}, Suma wag: {sum(kurs)}kg")