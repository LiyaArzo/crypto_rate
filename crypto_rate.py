from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import datetime
import time
import requests



def get_rate():
    pass


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


Label(text='Криптовалюта').pack(padx=10,pady=10)
crypto_combo = ttk.Combobox(values=list(crypto_names.keys()))
crypto_combo.pack(padx=10,pady=10)
crypto_combo.set('BTC (Bitcoin)')

Label(text='Целевая валюта').pack(padx=10,pady=10)
currency_combo = ttk.Combobox(values=list(currency_names.keys()))
currency_combo.pack(padx=10,pady=10)
currency_combo.set('USD (Доллар США)')



#crypto_combo.bind('<<ComboboxSelected>>',update_b_label)



btn = Button(text='Получить курс криптовалюты', command=get_rate)
btn.pack(padx=10,pady=10)

lbl = Label(text='')
lbl.pack(padx=10,pady=10)

window.mainloop()
