import os
import json
import aiofiles
import httpx
from geopy.distance import distance
from fastapi import APIRouter, Form, Request, Response, Query # Response - ответ, который мы отправим серверу
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
# from ZPapp.ZillowParse.schemas import Property
# from ZPapp.dao import PropertyDAO
# from ZPapp.users.dependencies import Depends, get_current_user
# from ZPapp.users.schemas import Users
# from ZPapp.ZillowParse.dao import PropertyDAO
# from ZPapp.ZillowParse.models import Property
from ZPapp.ZillowParse.log import *
from ZPapp.postgresql import get_coord_store

router = APIRouter(
    prefix='', # данный префикс будет перед всеми эндпоинтами
    tags=['Характеристики'] # название этого роутера для объединения роутеров в группу в документации
)

BASE_DIR = Path(__file__).resolve().parent
# Создаем объект для работы с HTML-шаблонами
# templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'ZPapp/templates')))
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('ZPapp/templates')))
# templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/fetch_and_process_data", response_class=HTMLResponse)
# async def fetch_and_process_data(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

async def fetch_zillow_data(url, headers, querystring):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)
        return response.text

@router.post("/fetch_and_process_data", response_model=dict)
async def fetch_and_process_data(
                                request: Request,
                                location: str = Form(),
                                status_type: str = Form(),
                                home_type: str = Form(),
                                minPrice: int = Form(),
                                maxPrice: int = Form(),
                                bathsMin: int = Form(),
                                bathsMax: int = Form(),
                                bedsMin: int = Form(),
                                bedsMax: int = Form(),
                                sqftMin: int = Form(),
                                sqftMax: int = Form(),
                                ):
   
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    
    # location = "Philadelphia, PA"
    # status_type = "ForSale"
    # home_type = "Houses"
    # minPrice = "10000"
    # maxPrice = "500000"
    # bathsMin = "2"
    # bathsMax = "3"
    # bedsMin = "2"
    # bedsMax = "4"
    # sqftMin = "600"
    # sqftMax = "4000"

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
        "X-RapidAPI-Key": "YourRapidAPI-Key",
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    # response_text = await fetch_zillow_data(url, headers, querystring)

    # Сохраняем полученные данные в файл 'zillow.json'
    # await save_data('./ZPapp/DataStores/zillow.json', 'w', response_text)

    # ########################################################################

    # Выгружаем данные о магазинах
    # data_TJ = json.loads(await load_data('./ZPapp/DataStores/T_J_stores_coord.json'))
    data_WFM = get_coord_store('tj')
    # data_WFM = json.loads(await load_data('./ZPapp/DataStores/WFM_stores_coord.json'))
    data_TJ = get_coord_store('wfm')
    

    # Достаём данные из файла 'zillow.json'
    data_zillow = json.loads(await load_data('./ZPapp/DataStores/zillow.json'))


    # Задаём желаемое расстояние до магазина (в милях):
    choice_miles = 3

    # Формируем список данных в читаемом виде, рассчитываем дистанцию и определяем ближайщие магазины
    # Результат записываем в словарь
    list_res_dicts = []

    for home in data_zillow['props']:
        res_dict = {}
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
            # property_data = Property(
            #     address=home['address'],
            #     country=home['country'],
            #     listingStatus=home['listingStatus'],
            #     zpid=home['zpid'],
            #     price=home['price'],
            #     livingArea=home['livingArea'],
            #     bedrooms=home['bedrooms'],
            #     bathrooms=home['bathrooms']
            # )
            # print(property_data)
            # PropertyDAO.add(property_data)
            res_dict['address'] = home['address']
            res_dict['country'] = home['country']
            res_dict['listingStatus'] = home['listingStatus']
            res_dict['zpid'] = home['zpid']
            res_dict['price'] = home['price']
            res_dict['livingArea'] = home['livingArea']
            res_dict['bedrooms'] = home['bedrooms']
            res_dict['bathrooms'] = home['bathrooms']

            list_res_dicts.append(res_dict)

            # Сохраняем полученные результаты в файл 'result.json'
    try:
        async with aiofiles.open('result.json', 'w', encoding='utf-8') as file:
            await file.write(json.dumps(list_res_dicts, indent=4))
    except Exception as e:
        print(f'An error occurred while writing to the file: {e}')
    # print(res_dict)
    print('Done! Save in DB successfully')
    response_data = {"message": "Data fetched and processed successfully", "data": list_res_dicts}
    print(response_data)
    return response_data
    # return templates.TemplateResponse("index.html", {"request": request, 'message': list_res_dicts})