import requests
import json
from geopy.distance import distance
from log import *

"""Собираем информацию с сайта zillow.com"""

# # Регистрируемся на сервисе "https://rapidapi.com/mashvisor-team/api/mashvisor/" и получаем API-KEY
# # Я использовал "https://rapidapi.com/apimaker/api/zillow-com1" (/propertyExtendedSearch (Extended search))

url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

# Задаём параметры поиска домов
location = "Chatham, IL" 
status_type = "ForSale"
home_type = "Houses"
minPrice = "10000"
maxPrice = "500000"
bathsMin = "2"
bathsMax = "3"
bedsMin = "2"
bedsMax = "4"
sqftMin = "600"
sqftMax = "4000"

querystring = {
               "location":location,
               "status_type":status_type,
               "home_type":home_type,
               "minPrice":minPrice,
               "maxPrice":maxPrice,
               "bathsMin":bathsMin,
               "bathsMax":bathsMax,
               "bedsMin":bedsMin,
               "bedsMax":bedsMax,
               "sqftMin":sqftMin,
               "sqftMax":sqftMax
               }

# Вводим полученный X-RapidAPI-Key и X-RapidAPI-Host
headers = {
	"X-RapidAPI-Key": "Your API key",
	"X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# Сохраняем полученные данные в файл 'zillow.json'
saveData('./DataStores/zillow.json', 'w', response.text)

# ########################################################################

# Выгружаем данные о магазинах
data_TJ = loadData('./DataStores/T_J_stores_coord.json')
data_WFM = loadData('./DataStores/WFM_stores_coord.json')

# Достаём данные из файла 'zillow.json'
data_zillow_json = loadData('./DataStores/zillow.json')

# Преобразуем строковые данные в словарь Python
data_zillow = json.loads(data_zillow_json)

# Задаём желаемое расстояние до магазина (в милях):
choice_miles = 80

# Формируем список данных в читаемом виде, рассчитываем дистанцию и определяем ближайщие магазины 
# Результат записываем в словарь
res_dict = {}

for home in data_zillow['props']:
    is_dist_to_WFM = False
    is_dist_to_TJ = False
    
    # Используем модуль библиотеки geopy.distance для определения расстояния между координатами 
    for item in data_WFM:
        dist_to_WFM = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
        if dist_to_WFM <= choice_miles:
            res_dict[f'Distance to wholefoodsmarkets ({item[0]})'] = f'{dist_to_WFM:.2f} miles'
            is_dist_to_WFM = True    

    for item in data_TJ:
        dist_to_TJ = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
        if dist_to_TJ <= choice_miles:
            res_dict[f"Distance to Trader Joe's ({item[0]})"] = f'{dist_to_TJ:.2f} miles'
            is_dist_to_TJ = True
    
    # Если магазины по расстоянию подходят, формируем словарь
    if is_dist_to_WFM or is_dist_to_TJ:
        res_dict['address'] = home['address']
        res_dict['country'] = home['country']
        res_dict['listingStatus'] = home['listingStatus']
        res_dict['zpid'] = home['zpid']
        res_dict['price'] = home['price']
        res_dict['livingArea'] = home['livingArea']
        res_dict['bedrooms'] = home['bedrooms']
        res_dict['bathrooms'] = home['bathrooms']

        # # Сохраняем полученные результаты в файл 'result.json'
        with open('result.json', 'a', encoding='utf-8') as file:
            json.dump(res_dict, file, indent=4)
print('Done!')
