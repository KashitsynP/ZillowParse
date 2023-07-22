import json
import aiofiles
import httpx
import asyncio
from geopy.distance import distance
from log import *


async def fetch_zillow_data(url, headers, querystring):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return response.text


async def main():
    # Получаем данные с сайта zillow.com
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    location = "Philadelphia, PA"
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
        "location": location,
        "status_type": status_type,
        "home_type": home_type,
        "minPrice": minPrice,
        "maxPrice": maxPrice,
        "bathsMin": bathsMin,
        "bathsMax": bathsMax,
        "bedsMin": bedsMin,
        "bedsMax": bedsMax,
        "sqftMin": sqftMin,
        "sqftMax": sqftMax
    }

    headers = {
        "X-RapidAPI-Key": "Your_API_key",
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response_text = await fetch_zillow_data(url, headers, querystring)

    # Сохраняем полученные данные в файл 'zillow.json'
    await save_data('./DataStores/zillow.json', 'w', response_text)

    # ########################################################################

    # Выгружаем данные о магазинах
    data_TJ = json.loads(await load_data('./DataStores/T_J_stores_coord.json'))
    data_WFM = json.loads(await load_data('./DataStores/WFM_stores_coord.json'))
    

    # Достаём данные из файла 'zillow.json'
    data_zillow = json.loads(await load_data('./DataStores/zillow.json'))


    # Задаём желаемое расстояние до магазина (в милях):
    choice_miles = 50

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

            # Сохраняем полученные результаты в файл 'result.json'
            async with aiofiles.open('result.json', 'a', encoding='utf-8') as file:
                await file.write(json.dumps(res_dict, indent=4))

    print('Done! Look at the zillow.json file')

if __name__ == "__main__":
    asyncio.run(main())
