import httpx
import asyncio
import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from ZPapp.ZillowParse.log import *


async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content


async def parse_tj_stores(url_list, teg, class_):
    data = []
    for url in url_list:
        response = await fetch_data(url)
        soup = BeautifulSoup(response, "lxml")
        locations = soup.findAll(teg, class_)
        for link in locations:
            if link.has_attr('href'):
                data.append(link['href'])
    return data


async def geocode_address(addresses):
    geolocator = Nominatim(user_agent="Tester")
    store_coords = []
    cnt = 0
    total_addresses = len(addresses)
    for address in addresses:
        cnt += 1
        print(f'Обработано: {cnt} из {total_addresses}')
        try:
            loop = asyncio.get_event_loop()
            loc = await loop.run_in_executor(None, geolocator.geocode, address)
            if loc:
                store_coords.append([address, loc.latitude, loc.longitude])
            else:
                store_coords.append([address, None, None])
        except GeocoderTimedOut:
            print(f"Тайм-аут геокодирования для адреса: {address}. Повторная попытка...")
        except GeocoderUnavailable:
                print(f"Сервер геокодирования недоступен. Повторная попытка...")
                await asyncio.sleep(5)  # Ждем 5 секунд перед повторной попыткой

    return store_coords


async def main():
    url_tj = "https://locations.traderjoes.com/"

    response_tj = await fetch_data(url_tj)
    soup_tj = BeautifulSoup(response_tj, "lxml")
    locations_tj = soup_tj.findAll("a", class_="ga_w2gi_lp listitem")

    url_tj_state = [link['href'] for link in locations_tj if link.has_attr('href')]
    print("State done!")

    url_tj_city = await parse_tj_stores(url_tj_state, "a", "ga_w2gi_lp listitem")
    print("City done!")

    url_tj_city_stores = await parse_tj_stores(url_tj_city, "a", "ga_w2gi_lp directions")
    print("Store done!")

    store_tj_address = []
    for store_info in url_tj_city_stores:
        response_tj_store_info = await fetch_data(store_info)
        soup_tj_store_info = BeautifulSoup(response_tj_store_info, 'lxml')
        address_tj_store = soup_tj_store_info.findAll('div', class_='addressline')
        for item in address_tj_store:
            store_tj_address.append(item.text.split())

    store_tj_address = parse_tj_stores(url_tj_city_stores, 'div', class_='addressline')

    print('Parsing done!')

    addresses = [' '.join(store_tj_address[i]) for i in range(len(store_tj_address))]

    await save_data('./ZPapp/DataStores/T_J_stores.json', 'w', '\n'.join(addresses))

    tj_stores = await load_data('./ZPapp/DataStores/T_J_stores.json')
    adresses_TJ = [store[:len(store) - 26] for store in tj_stores.split('\n')]

    T_J_store_coord = await geocode_address(adresses_TJ)

    await save_data('./ZPapp/DataStores/T_J_stores_coord.json', 'w', json.dumps(T_J_store_coord))

if __name__ == "__main__":
    asyncio.run(main())
