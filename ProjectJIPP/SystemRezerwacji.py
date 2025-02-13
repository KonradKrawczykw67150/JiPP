from ProjectJIPP.BazaDanych import BazaDanych
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import Calendar


class SystemRezerwacji:
    def __init__(self, root):
        self.baza = BazaDanych()
        self.root = root
        self.root.title("System Rezerwacji Wizyt Lekarskich")

        self.label = tk.Label(root, text="Zaloguj się")
        self.label.pack()

        self.btn_login = tk.Button(root, text="Logowanie", command=self.logowanie)
        self.btn_login.pack()

    def logowanie(self):
        email = simpledialog.askstring("Logowanie", "Podaj adres email:")
        haslo = simpledialog.askstring("Logowanie", "Podaj hasło:", show="*")
        uzytkownik = self.baza.sprawdz_uzytkownika(email, haslo)

        if uzytkownik:
            rola = uzytkownik[5]
            if rola == "admin":
                self.okno_admina()
            elif rola == "pacjent":
                self.okno_pacjenta(uzytkownik[0])
            elif rola == "lekarz":
                self.okno_lekarza(uzytkownik[0])
        else:
            messagebox.showinfo("Błąd", "Nieprawidłowe dane logowania")

    def okno_admina(self):
        admin_okno = tk.Toplevel(self.root)
        admin_okno.title("Panel Administratora")

        tk.Label(admin_okno, text="Dodaj nowego użytkownika").pack()
        tk.Button(admin_okno, text="Dodaj użytkownika", command=self.dodaj_uzytkownika).pack()

        tk.Label(admin_okno, text="Usuń użytkownika").pack()
        tk.Button(admin_okno, text="Usuń użytkownika", command=self.usun_uzytkownika).pack()

    def dodaj_uzytkownika(self):

        imie = simpledialog.askstring("Dodaj uzytkownika", "Podaj imię:")
        nazwisko = simpledialog.askstring("Dodaj uzytkownika", "Podaj nazwisko:")
        email = simpledialog.askstring("Dodaj uzytkownika", "Podaj email:")
        haslo = simpledialog.askstring("Dodaj użytkownika", "Podaj hasło:")
        rola = simpledialog.askstring("Dodaj użytkownika", "Podaj rola (admin/lekarz/pacjent):")
        opis = simpledialog.askstring("Dodaj użytkownika", "Podaj opis:")

        if imie and nazwisko and email and haslo and rola in ["admin", "pacjent", "lekarz"] and opis:
            if self.baza.dodaj_uzytkownika(imie, nazwisko, email, haslo, rola, opis):
                messagebox.showinfo("Użytkownik został dodany")
        else:
            messagebox.showerror("Błąd, nieprawidłowe dane!")

    def usun_uzytkownika(self):

        email = simpledialog.askstring("Usuń użytkownika", "Podaj email użytkownika do usunięcia:")

        if email:
            self.baza.usun_uzytkownika(email)
            messagebox.showinfo("Sukces", "Użytkownik został usunięty")
        else:
            messagebox.showerror("Podano niestniejący adres email do usunięcia")

    def okno_pacjenta(self, pacjent_id):
        self.okno_rezerwacji(pacjent_id)

    def okno_lekarza(self, lekarz_id):
        lekarz_okno = tk.Toplevel(self.root)
        lekarz_okno.title("Panel Lekarza")

        wizyty = self.baza.pobierz_wizyty_dla_lekarza(lekarz_id)
        lista_wizyt = "\n".join([f"ID {w[0]} - Pacjent {w[1]} Data: {w[3]}" for w in wizyty])

        tk.Label(lekarz_okno, text="Twoje wizyty").pack()
        tk.Label(lekarz_okno, text=lista_wizyt, justify="left").pack()

        tk.Button(lekarz_okno, text="Odwołaj wizytę", command=lambda: self.odwolaj_wizyte(lekarz_id)).pack()

    def okno_rezerwacji(self, pacjent_id):
        rezerwacja_okno = tk.Toplevel(self.root)
        rezerwacja_okno.title("Rezerwacji Wizyt")

        tk.Label(rezerwacja_okno, text="Wybierz lekarza:").pack()
        lekarze = self.baza.pobierz_lekarzy()

        self.lekarz_var = tk.StringVar()
        lekarz_menu = ttk.Combobox(rezerwacja_okno, textvariable=self.lekarz_var)
        lekarz_menu['values'] = [f"{lek[1]} {lek[2]}" for lek in lekarze]
        lekarz_menu.pack()

        tk.Label(rezerwacja_okno, text="Wybierz datę wizyty:").pack()
        kalendarz = Calendar(rezerwacja_okno, selectmode='day', year=2025, month=2, day=1)
        kalendarz.pack()

        tk.Label(rezerwacja_okno, text="Wybierz godzinę wizyty:").pack()
        godziny = [f"{h:02}:00" for h in range(8, 16)]
        self.godzina_var = tk.StringVar()
        godzina_menu = ttk.Combobox(rezerwacja_okno, textvariable=self.godzina_var, values=godziny)
        godzina_menu.pack()

        tk.Button(rezerwacja_okno, text="Zarezerwuj", command=lambda: self.rezerwuj_wizyte(pacjent_id, lekarze,
                                                                                           lekarz_menu, kalendarz,
                                                                                           godzina_menu)).pack()

    def rezerwuj_wizyte(self, pacjent_id, lekarze, lekarz_menu, kalendarz, godzina_menu):
        lekarz_nazwisko = lekarz_menu.get()
        wybrany_lekarz = next((lek for lek in lekarze if f"{lek[1]} {lek[2]}" == lekarz_nazwisko), None)

        if wybrany_lekarz:
            lekarz_id = wybrany_lekarz[0]
            data = f"{kalendarz.get_date()} {godzina_menu.get()}"
            self.baza.dodaj_wizyte(pacjent_id, lekarz_id, data)
            messagebox.showinfo("Potwierdzenie", "Wizyta została umówiona")
        else:
            messagebox.showerror("Błąd", "Wybierz lekarza!")

    def odwolaj_wizyte(self, lekarz_id):
        wizyty = self.baza.pobierz_wizyty_dla_lekarza(lekarz_id)

        if not wizyty:
            messagebox.showinfo("Brak wizyt", "Nie masz żadnych wizyt do odwołania.")
            return
        wizyty_dict = {f"Id {w[0]} - Pacjent {w[1]} Data {w[3]}": w[0] for w in wizyty}
        wybrana_wizyta = simpledialog.askstring("Odwołaj wizytę", "Podaj ID wizyty do odwołania:\n" +
                                                "\n".join(wizyty_dict.keys()))

        if wybrana_wizyta and wybrana_wizyta in wizyty_dict:
            if self.baza.odwolaj_wizyte(wizyty_dict[wybrana_wizyta]):
                messagebox.showinfo("Sukces", "Wizyta została odwołana.")
            else:
                messagebox.showerror("Błąd", "Nie udało się odowołać wizyty")
        else:
            messagebox.showerror("Błąd", "Podano nieprawidłowe ID wizyty")
