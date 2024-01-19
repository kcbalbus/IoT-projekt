import requests
from ReadingData import readSensors
from Card import buzz


def sendTo(api_url, raw_data):
    
    response = requests.post(api_url, data=raw_data)
    
    if response.status_code == 200:
        print("Zapytanie POST zostało pomyślnie wysłane.")
        print("Odpowiedź serwera:", response.text)
    else:
        print("Wystąpił błąd. Kod statusu:", response.status_code)
        print("Treść odpowiedzi:", response.text)


def sendWeatherData(api_url = "http://10.108.33.110:8000/api/send_weather_data/"):
    sendTo(api_url, getWeatherData())


def sendCardData(card_id, api_url = "http://10.108.33.110:8000/api/check_employee_card/"):
    sendTo(api_url, {"card_number": card_id, "weather_station": "f4085dc7-9284-4e13-b53f-a6284979ce64"})


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
    
