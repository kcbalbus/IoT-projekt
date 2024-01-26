import requests


def sendTo(api_url, raw_data):

    response = requests.post(api_url, data=raw_data)

    if response.status_code == 200 or response.status_code == 201 or response.status_code == 401:
        print("Zapytanie POST zostało pomyślnie wysłane.")
        print("Odpowiedź serwera:", response.text)
    else:
        print("Wystąpił błąd. Kod statusu:", response.status_code)
        print("Treść odpowiedzi:", response.text)


    return response.status_code


def sendCardData(card_id, api_url = "http://10.108.33.110:8000/api/new_employee_card/"):
    return sendTo(api_url, {"card_number": card_id, "weather_station": "cd048075-b98d-447e-9dcf-bde77f142bb9"})