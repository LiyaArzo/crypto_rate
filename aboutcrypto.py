def exist_data_check(data): # Проверка, есть ли данные
    if data:
        return float(data)
    else:
        return '-'


def exist_date_(data): # Проверка, есть ли дата
    if data:
        return data
    else:
        return ['-','-','-']


def about(data):
    data_m = data['market_data']
    cur_price = exist_data_check(data_m['current_price']['usd']) # текущий курс в $

    max_price = exist_data_check(data_m['ath']['usd']) # исторический максимум по цене в $
    max_y,max_m,max_d = exist_date_(data_m['ath_date']['usd'][:10].split('-')) # год, месяц, день
    min_price = exist_data_check(data_m['atl']['usd']) # исторический минимум по цене в $
    min_y, min_m, min_d = exist_date_(data_m['atl_date']['usd'][:10].split('-')) # год, месяц, день

    high_day_price = exist_data_check(data_m['high_24h']['usd']) # максимальная цена в $ за день
    low_day_price = exist_data_check(data_m['low_24h']['usd']) # минимальная цена в $ за день

    perc_day = exist_data_check(data_m['price_change_percentage_24h_in_currency']['usd']) # изменение цены в $ за день в %
    perc_month = exist_data_check(data_m['price_change_percentage_30d_in_currency']['usd']) # изменение цены в $ за месяц в %
    perc_year = exist_data_check(data_m['price_change_percentage_1y_in_currency']['usd']) # изменение цены в $ за год в %

    amount_now = exist_data_check(data_m['circulating_supply']) # количество валюты в обращении
    max_amount = exist_data_check(data_m['max_supply']) # максимально возможное количество валюты

    market = exist_data_check(data['tickers'][0]['market']['name']) # наиболее популярная биржа

# data['image']['thumb'] - ссылка на картинку