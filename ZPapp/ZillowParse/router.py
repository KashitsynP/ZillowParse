from geopy.distance import distance
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from pathlib import Path
import json

from ZPapp.config import settings
from ZPapp.postgresql import get_coord_store
from ZPapp.ZillowParse.log import *


router = APIRouter(
    prefix='', # данный префикс будет перед всеми эндпоинтами
    tags=['Характеристики'] # название этого роутера для объединения роутеров в группу в документации
)

BASE_DIR = Path(__file__).resolve().parent

# Создаем объект для работы с HTML-шаблонами
templates = Jinja2Templates(directory="ZPapp/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def fetch_zillow_data(url, headers, querystring):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=querystring)

        if response.status_code == 200:  # Проверяем, что запрос выполнен успешно (код статуса 200)
            response_data = response.json()
            return response_data

@router.post("/fetch_and_process_data")
async def fetch_and_process_data(
                                request: Request,
                                location: str = Form(),
                                status_type: str = Form(),
                                minPrice: int = Form(),
                                maxPrice: int = Form(),
                                bathsMin: int = Form(),
                                bathsMax: int = Form(),
                                bedsMin: int = Form(),
                                bedsMax: int = Form(),
                                sqftMin: int = Form(),
                                sqftMax: int = Form(),
                                distance_to_stores: int = Form(), 
                                ):
   
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    
    querystring = {
        "location": location,
        "status_type": status_type,
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
        "X-RapidAPI-Key": settings.ZILLOW_API_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    # response_text = await fetch_zillow_data(url, headers, querystring)
    from ZPapp.res import response_data
    response_text = response_data

    # Выгружаем данные о магазинах
    data_WFM = get_coord_store('tj')
    data_TJ = get_coord_store('wfm')
    
    # Формируем список данных в читаемом виде, рассчитываем дистанцию и определяем ближайщие магазины
    # Результат записываем в словарь
    list_res_dicts = []

    for home in response_text['props']:
        res_dict = {}
        stores_wfm = []
        stores_tj = []
        is_dist_to_WFM = False
        is_dist_to_TJ = False

        # Используем модуль библиотеки geopy.distance для определения расстояния между координатами
        for item in data_WFM:
            dist_to_WFM = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
            if dist_to_WFM <= distance_to_stores:
                stores_wfm.append(f'{item[0]} - {dist_to_WFM:.2f}')
                is_dist_to_WFM = True
        res_dict['wfm'] = stores_wfm

        for item in data_TJ:
            dist_to_TJ = distance((home['latitude'], home['longitude']), (item[1], item[2])).miles
            if dist_to_TJ <= distance_to_stores:
                stores_tj.append(f'{item[0]} - {dist_to_TJ:.2f}')
                is_dist_to_TJ = True
        res_dict['tj'] = stores_tj

        # Если магазины по расстоянию подходят, формируем словарь
        if is_dist_to_WFM or is_dist_to_TJ:
            res_dict['address']:str = home['address']
            res_dict['country']:str = home['country']
            res_dict['listingStatus']:str = home['listingStatus']
            res_dict['zpid']:int = home['zpid']
            res_dict['price']:int = home['price']
            res_dict['livingArea']:int = home['livingArea']
            res_dict['bedrooms']:int = home['bedrooms']
            res_dict['bathrooms']:int = home['bathrooms']
            res_dict['propertyType']:str = home['propertyType']
            res_dict['detailUrl']:str = home['detailUrl']
            res_dict['imgSrc']:str = home['imgSrc']

            list_res_dicts.append(res_dict)

    response_data = {"message": "Data fetched and processed successfully", "data": list_res_dicts}
    response_data=json.dumps(response_data)
    return response_data
