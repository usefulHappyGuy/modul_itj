# %%
import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
df = pd.read_csv('energydata_complete.csv')
df['date'] = pd.to_datetime(df['date'])

# Wyświetlenie podstawowych informacji
print("Udało się wczytać dane!")
df.info()

# %%
# WYKRES 1: Zużycie energii przez urządzenia
plt.figure(figsize=(10, 4))
plt.plot(df['date'][:500], df['Appliances'][:500], color='orange')
plt.title('Zużycie energii przez urządzenia (wycinek czasu)')
plt.xlabel('Czas')
plt.ylabel('Zużycie energii [Wh]')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# WYKRES 2: Histogram zużycia energii
plt.figure(figsize=(8, 4))
plt.hist(df['Appliances'], bins=50, color='purple', edgecolor='black')
plt.title('Rozkład zużycia energii')
plt.xlabel('Zużycie energii [Wh]')
plt.ylabel('Liczba pomiarów')
plt.tight_layout()
plt.show()

# %%
# WYKRES 3: Dobowy rytm zużycia energii (Średnia dla każdej godziny)
# Wyciągam samą godzinę z daty pomiaru
df['hour'] = df['date'].dt.hour

# Obliczamy średnie zużycie prądu dla poszczególnych godzin
hourly_energy = df.groupby('hour')['Appliances'].mean()

# Rysowanie wykresu
plt.figure(figsize=(10, 5))
plt.bar(hourly_energy.index, hourly_energy.values, color='teal', edgecolor='black')
plt.title('Dobowy profil zużycia energii w domu')
plt.xlabel('Godzina (0-23)')
plt.ylabel('Średnie zużycie energii [Wh]')
plt.xticks(range(0, 24)) # Wymuszamy pokazanie wszystkich 24 godzin na osi
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
# %%
# WYKRES 4: Średni dobowy profil temperatury (Wewnątrz vs Zewnątrz)
# Obliczamy średnią temperaturę wewnątrz (T1) i na zewnątrz (T_out) dla każdej godziny
hourly_temp_in = df.groupby('hour')['T1'].mean()
hourly_temp_out = df.groupby('hour')['T_out'].mean()

plt.figure(figsize=(10, 5))
# Rysujemy dwie linie dla porównania
plt.plot(hourly_temp_in.index, hourly_temp_in.values, label='Śr. Temp. Wewnątrz (Kuchnia)', color='red', marker='o', linewidth=2)
plt.plot(hourly_temp_out.index, hourly_temp_out.values, label='Śr. Temp. na Zewnątrz', color='blue', marker='x', linestyle='--')

plt.title('Dobowy profil temperatury domu')
plt.xlabel('Godzina (0-23)')
plt.ylabel('Temperatura [°C]')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(alpha=0.4, linestyle='--')
plt.tight_layout()
plt.show()
# %%
# WYKRES 5: Zależność temperatury (T1) od wilgotności (RH_1) wewnątrz
plt.figure(figsize=(9, 6))
# Używamy alpha=0.1, żeby kropki były przezroczyste – dzięki temu zobaczymy, gdzie się zagęszczają
plt.scatter(df['RH_1'], df['T1'], alpha=0.1, color='darkcyan', s=15)
plt.title('Zależność temperatury od wilgotności wewnątrz budynku (Kuchnia)')
plt.xlabel('Wilgotność względna [%]')
plt.ylabel('Temperatura [°C]')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# %%
# WYKRES 6 (Ulepszony): Boxplot - Zużycie energii a dzień tygodnia (tylko godziny aktywne)
# Tworzymy nową tabelę, wycinając tylko te pomiary, gdzie godzina jest większa lub równa 8
df_aktywne = df[df['hour'] >= 8]

plt.figure(figsize=(10, 6))
# Zauważ, że używamy teraz df_aktywne zamiast df
df_aktywne.boxplot(column='Appliances', by='day_of_week', grid=False, 
                   patch_artist=True, boxprops=dict(facecolor='lightblue', color='blue'))

# Zamieniamy cyfry (0-6) na ładne nazwy dni
dni_tygodnia = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Ndz']
plt.xticks(range(1, 8), dni_tygodnia)

plt.title('Rozkład zużycia energii w dniach tygodnia (godziny 8:00 - 23:59)')
plt.suptitle('') 
plt.xlabel('Dzień tygodnia')
plt.ylabel('Zużycie energii [Wh]')
plt.ylim(30, 200) # Lekko podniosłem limit, bo w dzień zużycie jest wyższe
plt.tight_layout()
plt.show()

# %%
