import requests
from bs4 import BeautifulSoup
import json
import csv
import lxml
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut 
from geopy.distance import distance
import time

"""Парсим сайт Trader Joe's"""

# url_tj = "https://locations.traderjoes.com/"

# response_tj = requests.get(url_tj)

# soup_tj = BeautifulSoup(response_tj.content, "lxml")

# locations_tj = soup_tj.findAll("a", class_="ga_w2gi_lp listitem")


# Находим все ссылки на штаты, записываем в список "url_tj_state"
# url_tj_state = []
# for link in locations_tj:
#     if link.has_attr('href'):
#         url_tj_state.append(link['href'])
# print("State done!")


# # Находим все города и записываем в список "url_tj_city"
# url_tj_city = []
# for state in url_tj_state:
#     response_tj_state = requests.get(state)
#     soup_tj_state = BeautifulSoup(response_tj_state.content, "lxml")
#     locations_tj_state = soup_tj_state.findAll("a", class_="ga_w2gi_lp listitem")
#     for link in locations_tj_state:
#         if link.has_attr('href'):
#             url_tj_city.append(link['href'])
# print("City done!")


# # Находим ссылку на каждый магазин в городе и записываем в список "url_tj_stores"
# url_tj_city_stores = []
# for store in url_tj_city:
#     response_tj_store = requests.get(store)
#     soup_tj_store = BeautifulSoup(response_tj_store.text, "lxml")
#     locations_tj_store = soup_tj_store.findAll("a", class_="ga_w2gi_lp directions")
#     for link_store in locations_tj_store:
#         if link_store.has_attr('href'):
#             url_tj_city_stores.append(link_store['href'])
# print("Store done!")


# # Создаём список с адресами магазинов
# store_tj_adress = []
# for store_info in url_tj_city_stores:
#     response_tj_store_info = requests.get(store_info)
#     soup_tj_store_info = BeautifulSoup(response_tj_store_info.text, 'lxml')
#     adress_tj_store = soup_tj_store_info.findAll('div', class_='addressline')

#     for item in adress_tj_store:
#         store_tj_adress.append(item.text.split())
# print('Parsing done!')

# # # Преобразуем адреса в читаемый формат
# adresses = []
# for i in range(len(store_tj_adress)):
#     adress = ' '.join(store_tj_adress[i])
#     adresses.append(adress)

# # # Сохраняем в файле, дабы не перегружать сайт частыми запросами

# with open("T_J_stores.json", "w", encoding="utf-8") as file:
#     json.dump(adresses, file)
#     print('OK')



#######################################################################################

# # Загружаем файл с адресами магазинов

# with open('T_J_stores.json', 'r') as file:
#     tj_stores = json.load(file)
#     print('Data T_J_stores.json is loaded')

# # # Убираем из списка номера телефонов (оставляем только адрес)
# adresses_TJ = []
# for i in range(len(tj_stores)):
#     adresses_TJ.append(tj_stores[i][:len(tj_stores[i])-26])

# Переводим адреса в координаты используя библиотеку 'geopy'

# T_J_store_coord = []
# T_J_coord = []
# longitude = [] 
# latitude = []

# print('start geocoding...')
# def findGeocode(city): 
#     try: 
#         geolocator = Nominatim(user_agent="Tester") 
#         return geolocator.geocode(city, exactly_one=True, timeout=60) 
#     except GeocoderTimedOut: 
#         return findGeocode(city)  
# cnt = 0
# for i in adresses_TJ: 
#     cnt += 1
#     print(cnt)
#     if findGeocode(i) != None: 
#         loc = findGeocode(i) 
#         latitude.append(loc.latitude) 
#         longitude.append(loc.longitude) 
#     else: 
#         latitude.append(None) 
#         longitude.append(None)
#         time.sleep(2)


# # Объединяем координаты в один список
# for i in range(len(adresses_TJ)):
#     T_J_store_coord.append([adresses_TJ[i], latitude[i], longitude[i]])


# # # Сохраняем файлы с адресами и координатами
# with open("T_J_stores_coord.json", "w", encoding="utf-8") as file:
#     json.dump(T_J_store_coord, file)
#     print('OK')


#############################################################################################

"""Парсим сайт Whole Foods Market"""

# На 'https://www.wholefoodsmarket.com/stores/' → нет магазинов США, поэтому воспользуемся Google-поиском

# 'https://www.google.com/maps/search/%22whole+foods+market%22/@39.3684851,-104.4275619,4.3z'

# Используя расширение Google Chrome 'Instant Data Scraper' находим все адреса магазинов и записываем в файл 'WFM_stores.csv'
# Редактируем файл 'WFM_stores.csv' так, чтобы в нём остался только столбец с адресами

# Достаём данные из файла 'WFM_stores.csv'

# with open('WFM_stores.csv') as file:
#     data_WFM_stores = list(csv.reader(file))
#     print('data_WFM_stores cvs is loaded')

# # # Приводим список адресов в читаемый вид
# WFM_stores = []
# for i in range(len(data_WFM_stores)):
#     WFM_stores.append(data_WFM_stores[i][0])


# # Переводим адреса в координаты используя библиотеку 'geopy'

# WFM_store_coord = []
# WFM_coord = []
# WFM_longitude = [] 
# WFM_latitude = []

# print('start geolocation...')
# def WFM_findGeocode(city): 
#     try: 
#         geolocator = Nominatim(user_agent="Tester")
#         return geolocator.geocode(city, exactly_one=True, timeout=60) 
#     except GeocoderTimedOut: 
#         return WFM_findGeocode(city)  
    
# cnt = 0
# for adress in WFM_stores: 
#     cnt += 1
#     print(cnt)
#     if WFM_findGeocode(adress) != None: 
#         loc = WFM_findGeocode(adress) 
#         WFM_latitude.append(loc.latitude) 
#         WFM_longitude.append(loc.longitude) 
#     else: 
#         WFM_latitude.append(None) 
#         WFM_longitude.append(None)
#     time.sleep(2)


# # Объединяем координаты в один список

# for i in range(len(WFM_stores)):
#     WFM_store_coord.append([WFM_stores[i], WFM_latitude[i], WFM_longitude[i]])

# # # Сохраняем файлы с адресами и координатами

# with open("WFM_stores_coord.json", "w", encoding="utf-8") as file:
#     json.dump(WFM_store_coord, file)
#     print('OK')
############################################################################

"""Собираем информацию с сайта zillow.com"""

# # Регистрируемся на сервисе "https://rapidapi.com/mashvisor-team/api/mashvisor/" и получаем API-KEY
# # Я использовал "https://rapidapi.com/apimaker/api/zillow-com1" (/propertyExtendedSearch (Extended search))

# url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

# # Задаём параметры поиска домов
# location = "West Palm Beach, FL"
# status_type = "ForSale"
# home_type = "Houses"
# minPrice = "10000"
# maxPrice = "400000"
# bathsMin = "2"
# bathsMax = "3"
# bedsMin = "2"
# bedsMax = "4"
# sqftMin = "600"
# sqftMax = "2000"

# querystring = {"location":location,"status_type":status_type,"home_type":home_type,"minPrice":minPrice,"maxPrice":maxPrice,"bathsMin":bathsMin,"bathsMax":bathsMax,"bedsMin":bedsMin,"bedsMax":bedsMax,"sqftMin":sqftMin,"sqftMax":sqftMax}

# # Вводим полученный X-RapidAPI-Key и X-RapidAPI-Host
# headers = {
# 	"X-RapidAPI-Key": "YOUR API KEY",
# 	"X-RapidAPI-Host": "YOUR API-Host"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)


# # Сохраняем полученные данные в файл 'zillow.json'

# with open("zillow.json", "w", encoding="utf-8") as file:
#     json.dump(response.text, file)

# ########################################################################


# with open('T_J_stores_coord.json', 'r') as file:
#     data_TJ = json.load(file)

# with open('WFM_stores_coord.json', 'r') as file:
#     data_WFM = json.load(file)

# # Достаём данные из файла 'zillow.json'
# with open('zillow.json', 'r') as file:
#     data_zillow_json = json.load(file)

# # # Преобразуем строковые данные в словарь Python
# data_zillow = json.loads(data_zillow_json)


# Задаём желаемое расстояние до магазина (в милях):
# choise_miles = 20

# Формируем список данных в читаемом виде, рассчитываем дистанцию и определяем ближайщие магазины 
# Результат записываем в словарь
# res_dict = {}
# for home in data_zillow['props']:
#     print('address:', home['address'])
#     res_dict['address'] = home['address']
#     print('country:', home['country'])
#     res_dict['country'] = home['country']
#     print('listingStatus:', home['listingStatus'])
#     res_dict['listingStatus'] = home['listingStatus']
#     print('zpid:', home['zpid'])
#     res_dict['zpid'] = home['zpid']
#     print('price:', home['price'])
#     res_dict['price'] = home['price']
#     print('livingArea:', home['livingArea'])
#     res_dict['livingArea'] = home['livingArea']
#     print('bedrooms:', home['bedrooms'])
#     res_dict['bedrooms'] = home['bedrooms']
#     print('bathrooms:', home['bathrooms'])
#     res_dict['bathrooms'] = home['bathrooms']
#     print('longitude:', home['longitude'])
#     res_dict['longitude'] = home['longitude']
#     print('latitude:', home['latitude'])
#     res_dict['latitude'] = home['latitude']
    # # Используем модуль библиотеки geopy.distance для определения расстояния между координатами 
    # for item in data_WFM:
    #     dist = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
    #     if dist <= choise_miles:
    #         print(f'Distance to wholefoodsmarkets: ({item[0]}), {dist:.2f} miles')
    #         res_dict[f'Distance to wholefoodsmarkets ({item[0]})'] = f'{dist:.2f} miles'
    # for item in data_TJ:
    #     dist = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
    #     if dist <= choise_miles:
    #         print(f"Distance to Trader Joe's.: ({item[0]}), {dist:.2f} miles)")
    #         res_dict[f"Distance to Trader Joe's ({item[0]})"] = f'{dist:.2f} miles'
    # print(res_dict)
    # print('-------------------------------------------------------------')

    # # Сохраняем полученные результаты в файл 'result.json'
    # with open('result.json', 'a', encoding='utf-8') as file:
    #     json.dump(res_dict, file)

   


