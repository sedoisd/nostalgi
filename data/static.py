import sys

import requests

GEOCODE_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
STATIC_API_SERVER = 'https://static-maps.yandex.ru/v1'

STATIC_API_KEY = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'  # '23b263bf-d98d-43ee-b024-39ccb486f492'
GEOCODER_API_KEY = 'bbf3064a-4087-43a3-bec3-622e7cb6a919'  # '8013b162-6b42-4997-9691-77b7074026e0'


def request_error(response, url, exit=None):
    print("Ошибка выполнения запроса:")
    print('Сервер:', url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    print('url:', response.url)
    print('Выход:', exit)
    sys.exit(1)


# geocoder
def get_toponym(toponym_to_find):
    request_params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(GEOCODE_API_SERVER, request_params)
    if not response:
        request_error(response, GEOCODE_API_SERVER, get_toponym)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_spn(toponym_to_find, mode=None):
    toponym = get_toponym(toponym_to_find)
    lower_corner = list(map(lambda x: float(x), toponym['boundedBy']['Envelope']['lowerCorner'].split()))
    upper_corner = list(map(lambda x: float(x), toponym['boundedBy']['Envelope']['upperCorner'].split()))
    spn = list(map(lambda x, y: round(x - y, 4), upper_corner, lower_corner))
    if mode == 'str':
        return f'{spn[0]},{spn[1]}'
    return spn


def get_ll(toponym_to_find, mode=None):
    toponym = get_toponym(toponym_to_find)
    toponym_coodrs = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrs.split(" ")
    if mode == 'str':
        return f'{toponym_longitude},{toponym_lattitude}'
    return float(toponym_longitude), float(toponym_lattitude)


# static
def get_map_by_toponym(toponym):
    params = {'apikey': STATIC_API_KEY, 'll': get_ll(toponym, 'str'), 'spn': get_spn(toponym, 'str')}
    response = requests.get(STATIC_API_SERVER, params=params)
    if not response:
        request_error(response, STATIC_API_SERVER, get_map_by_toponym)
    return response
