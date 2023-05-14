import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut 
import time
from log import *

"""Парсим сайт Whole Foods Market"""

# На 'https://www.wholefoodsmarket.com/stores/' → нет магазинов США, поэтому воспользуемся Google-поиском

# 'https://www.google.com/maps/search/%22whole+foods+market%22/@39.3684851,-104.4275619,4.3z'

# Используя расширение Google Chrome 'Instant Data Scraper' находим все адреса магазинов и записываем в файл 'WFM_stores.csv'
# Редактируем файл 'WFM_stores.csv' так, чтобы в нём остался только столбец с адресами

# Достаём данные из файла 'WFM_stores.csv'
with open('./DataStores/WFM_stores.csv') as file:
    data_WFM_stores = list(csv.reader(file))
    print('Data_WFM_stores cvs is loaded')

# Приводим список адресов в читаемый вид
WFM_stores = []
for i in range(len(data_WFM_stores)):
    WFM_stores.append(data_WFM_stores[i][0])

# Переводим адреса в координаты используя библиотеку 'geopy'
WFM_store_coord = []
WFM_coord = []
WFM_longitude = [] 
WFM_latitude = []

print('start geolocation...')
def WFM_findGeocode(city): 
    try: 
        geolocator = Nominatim(user_agent="Tester")
        return geolocator.geocode(city, exactly_one=True, timeout=60) 
    except GeocoderTimedOut: 
        return WFM_findGeocode(city)     
cnt = 0
for adress in WFM_stores: 
    cnt += 1
    print(cnt)
    if WFM_findGeocode(adress) != None: 
        loc = WFM_findGeocode(adress) 
        WFM_latitude.append(loc.latitude) 
        WFM_longitude.append(loc.longitude) 
    else: 
        WFM_latitude.append(None) 
        WFM_longitude.append(None)
    time.sleep(2)

# # Объединяем координаты в один список
for i in range(len(WFM_stores)):
    WFM_store_coord.append([WFM_stores[i], WFM_latitude[i], WFM_longitude[i]])

# # # Сохраняем файлы с адресами и координатами
saveData('./DataStores/WFM_stores_coord.json', 'w', WFM_store_coord)