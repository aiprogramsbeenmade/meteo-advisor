import customtkinter as ctk
from weather_engine import WeatherEngine


class MeteoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Meteo Advisor v2.0")
        self.geometry("450x650")  # Aumentata l'altezza per far stare tutto

        # --- UI RICERCA ---
        self.label_titolo = ctk.CTkLabel(self, text="🌤️ Meteo Advisor", font=("Roboto", 24, "bold"))
        self.label_titolo.pack(pady=20)

        # Frame per raggruppare Entry e tasto Favoriti
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(pady=10)

        self.entry_citta = ctk.CTkEntry(self.search_frame, placeholder_text="Inserisci città...", width=200)
        self.entry_citta.pack(side="left", padx=5)

        self.btn_add_fav = ctk.CTkButton(self.search_frame, text="⭐", width=40, command=self.save_to_fav)
        self.btn_add_fav.pack(side="left", padx=5)

        self.btn_cerca = ctk.CTkButton(self, text="Cerca", command=self.update_ui)
        self.btn_cerca.pack(pady=10)

        # --- AREA PREFERITI (Bottoni) ---
        self.fav_list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.fav_list_frame.pack(pady=5)

        # --- UNIT SWITCH ---
        self.unit_switch = ctk.CTkSwitch(self, text="Fahrenheit", command=self.update_ui)
        self.unit_switch.pack(pady=10)

        self.label_main = ctk.CTkLabel(self, text="", font=("Roboto", 20, "bold"))
        self.label_main.pack(pady=10)

        # --- SEZIONE PREVISIONI ---
        self.forecast_frame = ctk.CTkFrame(self)
        self.forecast_frame.pack(pady=10, padx=20, fill="x")
        self.forecast_labels = []

        # Carica preferiti all'avvio
        self.render_favorites()

    def render_favorites(self):
        for widget in self.fav_list_frame.winfo_children():
            widget.destroy()

        favs = WeatherEngine.get_favorites()
        for city in favs:
            btn = ctk.CTkButton(self.fav_list_frame, text=city, width=70, height=24,
                                fg_color="gray30", command=lambda c=city: self.update_ui(c))
            btn.pack(side="left", padx=5)

    def save_to_fav(self):
        city = self.entry_citta.get()
        if city:
            if WeatherEngine.add_favorite(city):
                self.render_favorites()

    def update_ui(self, city_override=None):
        citta = city_override if city_override else self.entry_citta.get()
        if not citta: return

        if city_override:
            self.entry_citta.delete(0, 'end')
            self.entry_citta.insert(0, city_override)

        dati = WeatherEngine.fetch_data(citta)

        if dati:
            # Gestione Unità di misura
            is_fahrenheit = self.unit_switch.get()
            temp = dati['current_temp']
            unit = "°C"

            if is_fahrenheit:
                temp = WeatherEngine.to_fahrenheit(temp)
                unit = "°F"

            self.label_main.configure(text=f"{dati['name']}: {temp}{unit}")

            # Aggiornamento Previsioni
            for widget in self.forecast_labels:
                widget.destroy()
            self.forecast_labels = []

            for day in dati['forecasts']:
                icon = WeatherEngine.get_weather_icon(day['code'])
                data_split = day['date'].split("-")
                data_formattata = f"{data_split[2]}/{data_split[1]}"

                t_max = day['temp_max']
                if is_fahrenheit: t_max = WeatherEngine.to_fahrenheit(t_max)

                info_text = f"{data_formattata}   {icon}   {t_max}{unit}"
                lbl = ctk.CTkLabel(self.forecast_frame, text=info_text, font=("Roboto", 15))
                lbl.pack(pady=5)
                self.forecast_labels.append(lbl)
        else:
            self.label_main.configure(text="Città non trovata! ❌")


if __name__ == "__main__":
    app = MeteoApp()
    app.mainloop()