import requests
from LoadingMeteorologicalValues import readSensors


def sendTo(api_url, raw_data, isCard = False):

    if isCard:
        content_type = "CardData"
    else:
        content_type = "WeatherData"
        
    headers = {
        "Content-Type": content_type,
        "Authorization": "",  
    }
    
    # Wysłanie zapytania POST
    response = requests.post(api_url, data=raw_data)
    
    # Sprawdź status odpowiedzi
    if response.status_code == 200:
        print("Zapytanie POST zostało pomyślnie wysłane.")
        print("Odpowiedź serwera:", response.text)
    else:
        print("Wystąpił błąd. Kod statusu:", response.status_code)
        print("Treść odpowiedzi:", response.text)


def sendWeatherData(api_url = "http://10.108.33.110:8000/api/send_weather_data/"):
    sendTo(api_url, getWeatherData())


def sendCardData(card_id, api_url = "http://10.108.33.110:8000/api/send_weather_data/"):
    sendTo(api_url, card_id, True)


def getWeatherData():

    (temp, hum, press) = readSensors()

    print(temp)
    print(hum)
    print(press)


    data_to_send = {
        "weather_station": "f4085dc7-9284-4e13-b53f-a6284979ce64",
        "temperature": temp,
        "humidity": hum,
        "pressure": press
    }
    return data_to_send

if __name__ == "__main__":
    sendWeatherData()
