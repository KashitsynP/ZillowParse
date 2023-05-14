import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from log import * 

"""Парсим сайт Trader Joe's"""

url_tj = "https://locations.traderjoes.com/"

response_tj = requests.get(url_tj)

soup_tj = BeautifulSoup(response_tj.content, "lxml")

locations_tj = soup_tj.findAll("a", class_="ga_w2gi_lp listitem")


# Находим все ссылки на штаты, записываем в список "url_tj_state"
url_tj_state = []
for link in locations_tj:
    if link.has_attr('href'):
        url_tj_state.append(link['href'])
print("State done!")


# Находим все города и записываем в список "url_tj_city"
url_tj_city = []
for state in url_tj_state:
    response_tj_state = requests.get(state)
    soup_tj_state = BeautifulSoup(response_tj_state.content, "lxml")
    locations_tj_state = soup_tj_state.findAll("a", class_="ga_w2gi_lp listitem")
    for link in locations_tj_state:
        if link.has_attr('href'):
            url_tj_city.append(link['href'])
print("City done!")


# Находим ссылку на каждый магазин в городе и записываем в список "url_tj_stores"
url_tj_city_stores = []
for store in url_tj_city:
    response_tj_store = requests.get(store)
    soup_tj_store = BeautifulSoup(response_tj_store.text, "lxml")
    locations_tj_store = soup_tj_store.findAll("a", class_="ga_w2gi_lp directions")
    for link_store in locations_tj_store:
        if link_store.has_attr('href'):
            url_tj_city_stores.append(link_store['href'])
print("Store done!")


# Создаём список с адресами магазинов
store_tj_address = []
for store_info in url_tj_city_stores:
    response_tj_store_info = requests.get(store_info)
    soup_tj_store_info = BeautifulSoup(response_tj_store_info.text, 'lxml')
    address_tj_store = soup_tj_store_info.findAll('div', class_='addressline')

    for item in address_tj_store:
        store_tj_address.append(item.text.split())
print('Parsing done!')

# Преобразуем адреса в читаемый формат
addresses = []
for i in range(len(store_tj_address)):
    address = ' '.join(store_tj_address[i])
    addresses.append(address)

# Сохраняем в файле, дабы не перегружать сайт частыми запросами
saveData('./DataStores/T_J_stores.json', 'w', addresses)

#######################################################################################

# Загружаем файл с адресами магазинов
tj_stores = loadData('./DataStores/T_J_stores.json')

# Убираем из списка номера телефонов (оставляем только адрес)
adresses_TJ = []
for i in range(len(tj_stores)):
    adresses_TJ.append(tj_stores[i][:len(tj_stores[i])-26])

# Переводим адреса в координаты используя библиотеку 'geopy'
T_J_store_coord = []
T_J_coord = []
longitude = [] 
latitude = []

print('start geocoding...')
def findGeocode(city): 
    try: 
        geolocator = Nominatim(user_agent="Tester") 
        return geolocator.geocode(city, exactly_one=True, timeout=60) 
    except GeocoderTimedOut: 
        return findGeocode(city)  
cnt = 0
for i in adresses_TJ: 
    cnt += 1
    print(cnt)
    if findGeocode(i) != None: 
        loc = findGeocode(i) 
        latitude.append(loc.latitude) 
        longitude.append(loc.longitude) 
    else: 
        latitude.append(None) 
        longitude.append(None)
    time.sleep(1)


# Объединяем координаты в один список
for i in range(len(adresses_TJ)):
    T_J_store_coord.append([adresses_TJ[i], latitude[i], longitude[i]])

# Сохраняем файлы с адресами и координатами
saveData('./DataStores/T_J_stores_coord.json', 'w', T_J_store_coord)
