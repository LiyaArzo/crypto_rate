import requests
from PIL import Image, ImageTk
from io import BytesIO

logo,cur_price,max_price,max_date,min_price,min_date = ['-'] * 6
perc_day, perc_month,perc_year,amount_now,max_amount,market = ['-'] * 6


# Проверка, есть ли данные и округление при наличии
def exist_data_check(data):
    if data:
        if isinstance(data,float):
            return round(data,4)
        else:
            return data
    else:
        return '-'


# Проверка, есть ли данные в процентах и округление при наличии
def exist_data_percent_check(data):
    if data:
        if isinstance(data,float):
            return round(data,2)
        else:
            return data
    else:
        return '-'


# Проверка, есть ли дата
def exist_date_(data):
    if data:
        return data
    else:
        return ['-','-','-']


# Получение параметров криптовалюты
def about(data):
    global logo, cur_price,max_price,max_date,min_price, min_date
    global perc_day, perc_month,perc_year,amount_now,max_amount,market

    data_m = data['market_data']

    cur_price = exist_data_check(data_m['current_price']['usd'])  # текущий курс в $
    max_price = exist_data_check(data_m['ath']['usd'])  # исторический максимум по цене в $
    max_y,max_m,max_d = exist_date_(data_m['ath_date']['usd'][:10].split('-'))  # год, месяц, день
    max_date = f'{max_d}.{max_m}.{max_y}'  # дата исторического максимума
    min_price = exist_data_check(data_m['atl']['usd'])  # исторический минимум по цене в $
    min_y, min_m, min_d = exist_date_(data_m['atl_date']['usd'][:10].split('-'))  # год, месяц, день
    min_date = f'{min_d}.{min_m}.{min_y}'  # дата исторического минимума
    p_day = exist_data_percent_check(data_m['price_change_percentage_24h_in_currency'])
    p_month = exist_data_percent_check(data_m['price_change_percentage_30d_in_currency'])
    p_year = exist_data_percent_check(data_m['price_change_percentage_1y_in_currency'])
    perc_day = exist_data_percent_check(p_day['usd']) if p_day != '-' else '-'  # изменение цены в $ за день в %
    perc_month = exist_data_percent_check(p_month['usd']) if p_month != '-' else '-'   # изменение цены в $ за месяц в %
    perc_year = exist_data_percent_check(p_year['usd']) if p_year != '-' else '-'   # изменение цены в $ за год в %
    amount_now = exist_data_check(data_m['circulating_supply'])  # количество валюты в обращении
    max_amount = exist_data_check(data_m['max_supply'])  # максимально возможное количество валюты
    market = exist_data_check(data['tickers'][0]['market']['name'])  # наиболее популярная биржа
    logo_url = data['image']['thumb']  # адрес логотипа криптовалюты
    logo = load_image(logo_url) if logo_url else '-'  # логотип или '-'


# Загрузка логотипа
def load_image(logo_url):
    try:
        response = requests.get(logo_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        return ImageTk.PhotoImage(img)
    except Exception:
        return '-'
