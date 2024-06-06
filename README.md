# Creating the README file with the provided content


# Projekt Satelitarny

## Opis

### Skrypt `ground_track_multicore.py`

Jego zadaniem jest wyliczenie czasów połączeń satelitów ze stacjami bazowymi. Zmiana podstawowych zmiennych następuje w pliku `settings.json`, który jest głównym plikiem konfiguracyjnym. Możemy tam załączyć pliki, z których ma korzystać skrypt. Poniżej zamieszczone są podstawowe zmienne:

- **altitude**: Wysokość orbity satelity.
- **HPBW**: Kąt połowy mocy anteny.
- **tps**: Ticks per second, liczba kroków symulacji na sekundę.
- **time**: Całkowity czas symulacji w sekundach.
- **orbit_time**: Czas trwania jednego pełnego obiegu orbity w sekundach.
- **min_encounter_time**: Minimalny czas spotkania, aby zostało ono uznane.
- **cities_file**: Plik JSON z danymi miast.
- **satelites_file**: Plik JSON z danymi satelitów.
- **encounters_file**: Plik JSON do zapisu wyników spotkań.

### Skrypt `plot_data.py`

Dodatkowy skrypt, który służy do wyświetlania stacji bazowych na mapie świata, aby zobrazować, gdzie występują połączenia. Skrypt ładuje dane z plików JSON, normalizuje wartości numeryczne i wyświetla je na mapie jako kolorowe markery.

## Podstawowe Zmienne

- **location_file**: Plik JSON zawierający dane lokalizacji miast.
- **data_file**: Plik JSON zawierający dane numeryczne powiązane z miastami.

## Instrukcja Użytkowania

1. **Konfiguracja**
   - Edytuj plik `settings.json`, aby ustawić odpowiednie zmienne i pliki z danymi.
   - Upewnij się, że pliki z danymi (`cities_file`, `satelites_file`) są poprawnie skonfigurowane i znajdują się w odpowiednich lokalizacjach.

2. **Uruchomienie symulacji**
   - Użyj skryptu `ground_track_multicore.py`, aby obliczyć czasy połączeń satelitów ze stacjami bazowymi:
     ```bash
     python ground_track_multicore.py
     ```

3. **Wizualizacja wyników**
   - Użyj skryptu `plot_data.py`, aby wyświetlić lokalizacje stacji bazowych na mapie świata:
     ```bash
     python plot_data.py
     ```

## Pliki JSON

### `settings.json`
Główny plik konfiguracyjny, który zawiera następujące ustawienia:
```json
{
    "altitude": 500, 
    "HPBW": 30, 
    "tps": 1, 
    "time": 86400, 
    "orbit_time": 5400, 
    "min_encounter_time": 10, 
    "cities_file": "cities128_land.json", 
    "satelites_file": "satelites.json", 
    "encounters_file": "encounters.json"
}
```

### `cities128_land.json`
Plik zawierający dane lokalizacji miast, np.:
```json
[
    {
        "near": "City Name",
        "latitude": 52.2297,
        "longitude": 21.0122
    },

]
```

### `satelites.json`
Plik zawierający dane satelitów, np.:
```json
[
    {
        "sat_no": 1,
        "latitude": 0,
        "longitude": 0
    },

]
```



### `encounters.json`
Plik, do którego zapisywane są wyniki symulacji, np.:
```json
[
    {
        "Station": "City Name",
        "satelite": 1,
        "time": 1234.56
    },

]
```

### Wymagania
- **Python 3.x** 
- **Biblioteki**: numpy, matplotlib, cartopy, json, multiprocessing
  
### Instalacja
Zainstaluj wymagane biblioteki używając pip:
```bash
pip install numpy matplotlib cartopy
```
