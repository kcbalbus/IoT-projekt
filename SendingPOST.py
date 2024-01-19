import requests
import json

# Adres API, do którego będziemy wysyłać zapytanie POST
api_url = "https://example.com/api/endpoint"

# Dane, które chcemy przesłać (w formie słownika)
data_to_send = {
    "key1": "value1",
    "key2": "value2",
}

# Konwertuj dane na format JSON
json_data = json.dumps(data_to_send)

# Nagłówki (opcjonalne, zależy od wymagań API)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Dodaj token autoryzacyjny, jeśli wymagany
}

# Wysłanie zapytania POST
response = requests.post(api_url, data=json_data, headers=headers)

# Sprawdź status odpowiedzi
if response.status_code == 200:
    print("Zapytanie POST zostało pomyślnie wysłane.")
    print("Odpowiedź serwera:", response.text)
else:
    print("Wystąpił błąd. Kod statusu:", response.status_code)
    print("Treść odpowiedzi:", response.text)