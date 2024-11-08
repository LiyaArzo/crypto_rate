import requests
from PIL import Image, ImageTk
from io import BytesIO #importoutput

logo,cur_price,max_price,max_date,min_price,min_date = ['-'] * 6
perc_day, perc_month,perc_year,amount_now,max_amount,market = ['-'] * 6


def exist_data_check(data): # Проверка, есть ли данные
    if data:
        if isinstance(data,float):
            return round(data,4)
        else:
            return data
    else:
        return '-'


def exist_data_percent_check(data): # Проверка, есть ли данные
    if data:
        return round(data,2)
    else:
        return '-'


def exist_date_(data): # Проверка, есть ли дата
    if data:
        return data
    else:
        return ['-','-','-']


def about(data):
    global logo, cur_price,max_price,max_date,min_price, min_date
    global perc_day, perc_month,perc_year,amount_now,max_amount,market
    data_m = data['market_data']
    cur_price = exist_data_check(data_m['current_price']['usd']) # текущий курс в $
    max_price = exist_data_check(data_m['ath']['usd']) # исторический максимум по цене в $
    max_y,max_m,max_d = exist_date_(data_m['ath_date']['usd'][:10].split('-')) # год, месяц, день
    max_date = f'{max_d}.{max_m}.{max_y}'
    min_price = exist_data_check(data_m['atl']['usd']) # исторический минимум по цене в $
    min_y, min_m, min_d = exist_date_(data_m['atl_date']['usd'][:10].split('-')) # год, месяц, день
    min_date = f'{min_d}.{min_m}.{min_y}'
    perc_day = exist_data_percent_check(data_m['price_change_percentage_24h_in_currency']['usd']) # изменение цены в $ за день в %
    perc_month = exist_data_percent_check(data_m['price_change_percentage_30d_in_currency']['usd']) # изменение цены в $ за месяц в %
    perc_year = exist_data_percent_check(data_m['price_change_percentage_1y_in_currency']['usd']) # изменение цены в $ за год в %
    amount_now = exist_data_check(data_m['circulating_supply']) # количество валюты в обращении
    max_amount = exist_data_check(data_m['max_supply']) # максимально возможное количество валюты
    market = exist_data_check(data['tickers'][0]['market']['name']) # наиболее популярная биржа
    logo_url = data['image']['thumb']
    logo = load_image(logo_url)


def load_image(logo_url):
    if logo_url:
        try:
            response = requests.get(logo_url)
            response.raise_for_status() # если будет ошибка, тут ее получим, для обработки исключения
            image_data = BytesIO(response.content) # байт символы
            img = Image.open(image_data)
            #img.thumbnail((600,480), Image.Resampling.LANCZOS) # корректировка размеров изображения, чтобы оно умещалось в окно
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f'Произошла ошибка {e}')
            return None
    else:
        return '-'
