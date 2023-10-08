import csv
import asyncio
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable 
import time
from log import *

"""Парсим сайт Whole Foods Market"""

# На 'https://www.wholefoodsmarket.com/stores/' → нет магазинов США, поэтому воспользуемся Google-поиском

# 'https://www.google.com/maps/search/%22whole+foods+market%22/@39.3684851,-104.4275619,4.3z'

# Используя расширение Google Chrome 'Instant Data Scraper' находим все адреса магазинов и записываем в файл 'WFM_stores.csv'
# Редактируем файл 'WFM_stores.csv' так, чтобы в нём остался только столбец с адресами


async def WFM_findGeocode(address): 
    geolocator = Nominatim(user_agent="Tester")
    try: 
        loop = asyncio.get_event_loop()
        loc = await loop.run_in_executor(None, geolocator.geocode, address)
        if loc:
            return loc
    except GeocoderTimedOut:
        print(f"Тайм-аут геокодирования для адреса: {address}. Повторная попытка...")
    except GeocoderUnavailable:
            print(f"Сервер геокодирования недоступен. Повторная попытка...")
            await asyncio.sleep(5)  # Ждем 5 секунд перед повторной попыткой

async def main():

    # Достаём данные из файла 'WFM_stores.csv'
    with open('./ZPapp/DataStores/WFM_stores.csv') as file:
        data_WFM_stores = list(csv.reader(file))
        print('Data_WFM_stores cvs is loaded')

    # Приводим список адресов в читаемый вид
    WFM_stores = []
    for i in range(len(data_WFM_stores)):
        WFM_stores.append(data_WFM_stores[i][0])

    # Переводим адреса в координаты используя библиотеку 'geopy'
    WFM_store_coord = []
    WFM_longitude = [] 
    WFM_latitude = []

    print('start geolocation...')
        
    total_addresses = len(WFM_stores)
    cnt = 0
    for address in WFM_stores: 
        cnt += 1
        print(f'Обработано: {cnt} из {total_addresses}')
        if await WFM_findGeocode(address) != None: 
            loc = await WFM_findGeocode(address) 
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
    await save_data('./ZPapp/DataStores/WFM_stores_coord.json', 'w', WFM_store_coord)

if __name__ == "__main__":
    asyncio.run(main())
    