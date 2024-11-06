from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from datetime import datetime
import requests

exchange_rate = None # переменная для курса выбранной криптовалюты
counter = 0 # счетчик для количества запросов к api


def get_rate(): #функция получения курса криптовалют
    global exchange_rate
    global counter
    crypto = crypto_combo.get() # название криптовалюты
    t_currency = currency_combo.get() # название целевой валюты
    crypto_id = crypto_names[crypto][0] # id криптовалюты для api
    t_currency_id = currency_names[t_currency] # id валюты для api
    amount_text = crypto_amount.get() # количество криптовалюты
    if amount_text == '': # если в поле ничего нет, по умолчанию считаем за единицу
        amount_text = '1.00'
        crypto_amount.insert(0,amount_text)
        mb.showwarning('Внимание!',f'Курс рассчитан за 1 единицу {crypto}')
    if amount_text.replace('.','',1).isalnum(): # если в поле максимум 1 точка
        amount_ = float(amount_text)
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={t_currency_id}&include_last_updated_at=true')
            response.raise_for_status()
            counter += 1 # если не возникло исключение, счетчик увеличится на 1
            counter_lbl.config(text=f'Использовано запросов: {counter}')
            data = response.json()
            exchange_rate = data[crypto_id][t_currency_id] # получаем курс криптовалюты
            crypto_cur_lbl.config(text=f'Курс криптовалюты: 1 {crypto_names[crypto][1]} = {exchange_rate} {t_currency_id.upper():.5f}')
            last_upd_t = data[crypto_id]['last_updated_at'] # время последнего обновления
            last_upd = datetime.fromtimestamp(last_upd_t).strftime('%d.%m.%Y')
            result = exchange_rate*amount_
            rate_entry.delete(0,END)
            rate_entry.insert(0,f'{result:.4f}')
            last_upd_lbl.config(text=f'Данные обновлены {last_upd}')
        except Exception as e:
            mb.showerror('Ошибка', f'Возникла ошибка с соединением {e}')
    else:
        mb.showerror('Ошибка',f'Вы ввели неверное количество {crypto} - {amount_text}')



def update_rate():
    get_rate()


def validate_entry(entry):
    e = entry.get()
    txt = ''.join(b for b in e if b in '0123456789.')
    if e != txt:
        entry.delete(0,END)
        entry.insert(0,txt)


def recalc_cur(event):
    amount = float(crypto_amount.get())
    currency = amount*exchange_rate
    rate_entry.delete(0, END)
    rate_entry.insert(0,str(currency))

def recalc_crypto(event):
    amount = float(rate_entry.get())
    crypto = amount/exchange_rate
    crypto_amount.delete(0, END)
    crypto_amount.insert(0, f'{crypto:.4f}')


window = Tk()
window.title('Курсы криптовалют')
window.geometry('400x420')
window.iconbitmap('crypto.ico')

crypto_names = {
    'ADA (Cardano)':['cardano','ADA'],
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


Label(text='Криптовалюта',font='Arial 16 bold').grid(row=0,column=0,columnspan=2,sticky='ew',ipady=10)

# Поле ввода количества криптовалюты, по умолчанию 1.00
crypto_amount = ttk.Entry(font='Arial 10', justify='center')
crypto_amount.insert(0,'1.00')
crypto_amount.grid(row=1,column=0,ipady=2,padx=10)
crypto_amount.bind('<KeyRelease>', lambda event:validate_entry(crypto_amount))
crypto_amount.bind('<Tab>',recalc_cur)

# Выпадающий список криптовалют
crypto_combo = ttk.Combobox(values=list(crypto_names.keys()),
                            state="readonly",font='Arial 10', justify='center', width=27)
crypto_combo.grid(row=1,column=1, ipady=2)
crypto_combo.set('BTC (Bitcoin)')
crypto_combo.bind('<<ComboboxSelected>>',lambda event:get_rate())

Label(text='Целевая валюта', font='Arial 10 bold').grid(row=2,column=0,columnspan=2,sticky='ew',ipady=10)

# Поле для отображения стоимости криптовалюты в выбранной валюте, а также для ввода количества валюты
rate_entry = ttk.Entry(font='Arial 10', justify='center')
rate_entry.grid(row=3,column=0,ipady=2,padx=10)
rate_entry.bind('<KeyRelease>', lambda event:validate_entry(rate_entry))
rate_entry.bind('<Tab>',recalc_crypto)

# Выпадающий список валют
currency_combo = ttk.Combobox(values=list(currency_names.keys()),
                              state="readonly", font='Arial 10', justify='center', width=27)
currency_combo.grid(row=3,column=1, ipady=2)
currency_combo.set('USD (Доллар США)')
currency_combo.bind('<<ComboboxSelected>>',lambda event:get_rate())

# Кнопка для обновления курса криптовалюты
btn = ttk.Button(text='Обновить', command=update_rate)
btn.grid(row=4,column=0,columnspan=2,pady=20)

# Метка для отображения информации о курсе криптовалюты
crypto_cur_lbl = Label(text='',font='Arial 10')
crypto_cur_lbl.grid(row=5,column=0,columnspan=2,pady=20)

# Метка для отображения времени последнего обновления данных о курсе валюты
last_upd_lbl = Label(text='',font='Arial 10')
last_upd_lbl.grid(row=6,column=0,columnspan=2,pady=20)

# Метка для отображения счетчика
counter_lbl = Label(text='',font='Arial 10')
counter_lbl.grid(row=7,column=0,columnspan=2,pady=20)

#get_rate()

window.mainloop()
