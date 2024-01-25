import requests
from LoadingMeteorologicalValues import readSensors
from Card import buzz

weather_station_id = "cd048075-b98d-447e-9dcf-bde77f142bb9"


def sendTo(api_url, raw_data):
    
    response = requests.post(api_url, data=raw_data)
    
    if response.status_code == 200:
        print("Zapytanie POST zostało pomyślnie wysłane.")
        print("Odpowiedź serwera:", response.text)
    else:
        print("Wystąpił błąd. Kod statusu:", response.status_code)
        print("Treść odpowiedzi:", response.text)

    return response.status_code


def validateCard(card_id):
    return sendCardData(card_id) == 200



def sendWeatherData(api_url = "http://10.108.33.110:8000/api/send_weather_data/"):
    sendTo(api_url, getWeatherData())


def notifyServerTime(card_id, api_url = "http://10.108.33.110:8000/api/handle_work_time/"):
    sendTo(api_url, {"card_number": card_id, "weather_station": weather_station_id})


def sendCardData(card_id, api_url = "http://10.108.33.110:8000/api/check_employee_card/"):
    return sendTo(api_url, {"card_number": card_id, "weather_station": weather_station_id})


def getWeatherData():

    (temp, hum, press) = readSensors()

    print(temp)
    print(hum)
    print(press)


    data_to_send = {
        "weather_station": weather_station_id,
        "temperature": temp,
        "humidity": hum,
        "pressure": press
    }
    return data_to_send

if __name__ == "__main__":
    sendWeatherData()
    
