import pyodbc

class BazaDanych:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-ODQ3HOF5;'
            'DATABASE=PrzychodniaDB;'
            'Trusted_Connection=yes;'
        )
        self.cur = self.conn.cursor()
        self.conn.commit()

    def sprawdz_uzytkownika(self, email, haslo):
        self.cur.execute("SELECT * FROM Użytkownicy WHERE email = ? AND Hasło = ?", (email, haslo))
        return self.cur.fetchone()

    def dodaj_uzytkownika(self, imie, nazwisko, email, haslo, rola, opis):
        self.cur.execute(
            "INSERT INTO Użytkownicy (Imię, Nazwisko, email, Hasło, Rola, Opis) VALUES (?, ?, ?, ?, ?, ?) ",
            (imie, nazwisko, email, haslo, rola, opis))
        self.conn.commit()

    def usun_uzytkownika(self, email):
        self.cur.execute("DELETE FROM Użytkownicy WHERE email = ?", (email,))
        self.conn.commit()

    def dodaj_wizyte(self, pacjent_id, lekarz_id, data):
        self.cur.execute("INSERT INTO Wizyty (pacjent_id, lekarz_id, DataWizyty) VALUES (?, ?, ?)",
                         (pacjent_id, lekarz_id, data))
        self.conn.commit()

    def odwolaj_wizyte(self, wizyta_id):
        self.cur.execute("DELETE FROM Wizyty WHERE Id= ?", (wizyta_id,))
        self.conn.commit()

    def pobierz_wizyty_dla_lekarza(self, lekarz_id):
        self.cur.execute("SELECT * FROM Wizyty WHERE lekarz_id = ?", (lekarz_id,))
        return self.cur.fetchall()

    def pobierz_lekarzy(self):
        self.cur.execute("SELECT ID, Imię, Nazwisko FROM Użytkownicy WHERE Rola ='lekarz'")
        wynik = self.cur.fetchall()
        if wynik:
            return wynik
        return []
