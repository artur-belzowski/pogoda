import json
import requests
import datetime

latitude = 52.237049
longitude = 21.017532

# poproś użytkownika o podanie daty
searched_date_str = input("Podaj datę w formacie RRRR-MM-DD (lub zostaw puste dla daty jutrzejszej): ")
if searched_date_str == "":
    searched_date = datetime.date.today() + datetime.timedelta(days=1)
else:
    searched_date = datetime.datetime.strptime(searched_date_str, '%Y-%m-%d').date()

# wczytaj wyniki z pliku, jeśli istnieją
try:
    with open('prognoza.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

# jeśli wynik istnieje
if str(searched_date) in data:
    print("Wynik dla daty", searched_date, "został już pobrany:")
    print("Opady deszczu:", data[str(searched_date)])
    quit()

# skonstruuj URL z podaną datą
url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

# pobierz dane z API
resp = requests.get(url.format(latitude=latitude, longitude=longitude, searched_date=searched_date))
api_data = resp.json()

# wydrukuj dane
# print(api_data)
rain = api_data['daily']['rain_sum']
rain = float(rain[0])
if rain > 0.0:
    print("Będzie padać.")
    result = "Będzie padać."
elif rain == 0.0:
    print("Nie będzie padać.")
    result = "Nie będzie padać."
else:
    print("Nie wiadomo.")
    result = "Nie wiadomo."

# zapisz wynik zapytania do pliku
data[str(searched_date)] = result
with open('prognoza.json', 'w') as f:
    json.dump(data, f)

