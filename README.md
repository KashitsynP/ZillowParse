# ZillowParse

Приложение ZillowParse помогает находить недвижимость в США (с сайта https://www.zillow.com/) для покупки/аренды в заданном пользователем радиусе от магазинов здорового питания WholeFoodsMarket и Trader Joe's.

![](screen/screen_1.png "Сюда не тыкай")

> База данных содержит данные о магазинах (адрес и координаты), которые были спарсены. 
> Скрипты парсеров находятся в `ZPapp/ZillowParse/parse_stores/`

> Логика работы приложения:
> Пользователь вводит запрос на получение данных об объектах недвижимости с заданными параметрами и указывает максимальное расстояние до магазинов здорового питания. Посредством API находятся данные об объектах недвижимости и отображаются только те, которые удовлетворяют условию по расстоянию до магазинов.



## Инструкция по развертыванию приложения ZillowParse в docker  

1. Клонируем репозиторий в заранее подготовленную папку
```shell
git clone https://github.com/KashitsynP/ZillowParse.git
```

2. Переходим в корень проекта:
```shell
cd ZillowParse/
```

3. В корне проекта, на одном уровне с Dockerfile, создаем файл .env и заполняем его следующими данными:

```
DB_HOST=db
DB_PORT=5432
DB_USER=zp
DB_PASS=zp
DB_NAME=zpapp
ZILLOW_API_KEY=73f04596b6msh78f0ebf1b9d023ap1cdeb4jsn966df12f9a9b
```
> [!NOTE]
> Данный API-KEY является тестовым и необходим для корректной работы приложения с моковыми данными. 

4. Собираем docker-compose:
```shell
docker-compose up --build
```

5. Открываем второй терминал и в нем вводим команды:
   (Команды для восстановления БД)
```shell
docker exec -it zpapp_db bash
psql -U zp -d zpapp -f /docker-entrypoint-initdb.d/zpapp_dump_db.sql
exit
```
6. Далее необходимо перезагрузить docker-compose:
```shell
docker-compose restart
```
7. Переходим на [localhost:8000](http://localhost:8000/) и любуемся приложением :-)


> [!NOTE]
> Основная логика приложения находится в ZPapp/ZillowParse/router.py.
> В текущем виде приложение обрабатывает моковые данные, находящиеся в ZPapp/res.py. Для полноценной работы с реальными данными по API необходимо:
> 1. Зарегистрироваться на сайте https://rapidapi.com/apimaker/api/zillow-com1/, получить API-KEY и внести его в .env (ZILLOW_API_KEY)
> 2. В файле ZPapp/ZillowParse/router.py снять комментарий со строки 70 и закомментировать строки 73-74
