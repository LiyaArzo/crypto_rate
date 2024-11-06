from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import datetime
import time
import requests



def get_rate():
    crypto = crypto_names[crypto_combo.get()]
    t_currency = currency_names[currency_combo.get()]
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={t_currency}&include_last_updated_at=true')
        response.raise_for_status()
        data = response.json()
        exchange_rate = data[crypto][t_currency]
        last_upd = data[crypto]['last_updated_at']
        print(exchange_rate, datetime.fromtimestamp(last_upd))
    except Exception as e:
        print(f'Возникла ошибка {e}')



window = Tk()
window.title('Курсы криптовалют')
window.geometry('360x420')

crypto_names = {
    'ADA (Cardano)':'cardano',
    'BBT (BabyBoomToken)': 'babyboomtoken',
    'BTC (Bitcoin)':'bitcoin',
    'CETUS (Cetus Protocol)': 'cetus-protocol',
    'COW (CoW Protocol)':'cow-protocol',
    'DOGE (Dogecoin)':'dogecoin',
    'ETH (Ethereum)': 'ethereum',
    'GRASS': 'grass',
    'LINK (Chainlink)':'chainlink',
    'NYM': 'nym',
    'PNUT (Peanut the Squirrel)': 'peanut-the-squirrel',
    'TRUMP (MAGA)': 'maga',
    'TRX (TRON)':'tron',
    'VISTA (Ethervista)': 'ethervista',
    'XMR (Monero)':'monero',
    'XRP (Ripple)':'ripple'
}


currency_names = {
    'CNY (Китайский юань)': 'cny',
    'EUR (Евро)': 'eur',
    'JPY (Японская йена)': 'jpy',
    'KRW (Южнокорейская вона': 'krw',
    'RUB (Российский рубль)': 'rub',
    'USD (Доллар США)': 'usd'
}



url_list='https://api.coingecko.com/api/v3/coins/list'


Label(text='Криптовалюта').grid(row=0,column=0,columnspan=2,sticky='ew')

crypto_emount = ttk.Entry()
crypto_emount.grid(row=1,column=0)
crypto_combo = ttk.Combobox(values=list(crypto_names.keys()),state="readonly")
crypto_combo.grid(row=1,column=1)
crypto_combo.set('BTC (Bitcoin)')

Label(text='Целевая валюта').grid(row=2,column=0,columnspan=2,sticky='ew')
lbl = Label(text='')
lbl.grid(row=3,column=0)
currency_combo = ttk.Combobox(values=list(currency_names.keys()),state="readonly")
currency_combo.grid(row=3,column=1)
currency_combo.set('USD (Доллар США)')

#crypto_combo.bind('<<ComboboxSelected>>',update_b_label)

btn = ttk.Button(text='Получить курс криптовалюты', command=get_rate)
btn.grid(row=4,column=0,columnspan=2)



window.mainloop()
