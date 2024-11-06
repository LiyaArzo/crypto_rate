from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
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
            crypto_cur_lbl.config(text=f'Курс криптовалюты: 1 {crypto_names[crypto][1]} = {exchange_rate:.5f} {t_currency_id.upper()}')
            last_upd_t = data[crypto_id]['last_updated_at'] # время последнего обновления
            last_upd = datetime.fromtimestamp(last_upd_t).strftime('%d.%m.%Y в %H:%M')
            result = exchange_rate * amount_
            rate_entry.delete(0,END) # очищение стоимости криптовалюты
            rate_entry.insert(0,f'{result:.4f}')
            last_upd_lbl.config(text=f'Данные обновлены {last_upd}')
        except Exception as e:
            mb.showerror('Ошибка', f'Возникла ошибка {e}')
    else:
        mb.showerror('Ошибка',f'Вы ввели неверное количество {crypto} - {amount_text}')


def update_rate():
    if exchange_rate:
        answer = sd.askinteger('Уточните,',
                               f'что нужно пересчитать:\n\n 1 - курс криптовалюты в выбранной валюте\n 2 - количество криптовалюты, которое можно приобрести за указанную сумму')
        if answer == 1:
            recalc_cur()
        elif answer == 2:
            recalc_crypto()
        else:
            return None
    else:
        get_rate()


def validate_entry(entry):
    e = entry.get()
    txt = ''.join(b for b in e if b in '0123456789.')
    if e != txt:
        entry.delete(0,END)
        entry.insert(0,txt)


def recalc_cur():
    cry_amount = crypto_amount.get()
    if cry_amount and exchange_rate:
        if cry_amount.replace('.','',1).isalnum():
            amount = float(cry_amount)
            currency = amount * exchange_rate
            rate_entry.delete(0, END)
            rate_entry.insert(0,str(currency))
        else:
            mb.showerror('Ошибка', f'Вы ввели неверное значение - {cry_amount}')
            crypto_amount.delete(0, END)
    else:
        return None


def recalc_crypto():
    rate_amount = rate_entry.get()
    if rate_amount and exchange_rate:
        if rate_amount.replace('.','',1).isalnum():
            amount = float(rate_amount)
            crypto = amount / exchange_rate
            crypto_amount.delete(0, END)
            crypto_amount.insert(0, f'{crypto:.4f}')
        else:
            mb.showerror('Ошибка', f'Вы ввели неверное значение - {rate_amount}')
            rate_entry.delete(0, END)
    else:
        return None


def choose_crypto():
    crypto_choose_win.iconify()
    crypto_choose_win.focus()
    choose_lbl.pack(pady=10)
    crypto_combo2.pack(pady=10)
    crypto_combo2.set('BTC (Bitcoin)')
    crypto_combo2.bind('<<ComboboxSelected>>', lambda event: show_info())
    btn1.pack()




def show_info():

    b = crypto_combo2.get()
    print(b)

def exit_win():
    crypto_choose_win.withdraw()


window = Tk()
window.title('Курсы криптовалют')
window.geometry('400x420')
window.iconbitmap(default='crypto.ico')

mainmenu = Menu(window)
window.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Криптовалюта", menu=filemenu)
filemenu.add_command(label="Инфо", command=choose_crypto)



crypto_names = {
    'ADA (Cardano)':['cardano','ADA'],
    'BBT (BabyBoomToken)': ['babyboomtoken','BBT'],
    'BTC (Bitcoin)':['bitcoin','BTC'],
    'CETUS (Cetus Protocol)': ['cetus-protocol','CETUS'],
    'COW (CoW Protocol)':['cow-protocol','COW'],
    'DOGE (Dogecoin)':['dogecoin','DOGE'],
    'ETH (Ethereum)': ['ethereum','ETH'],
    'GRASS': ['grass','GRASS'],
    'LINK (Chainlink)':['chainlink','LINK'],
    'NYM': ['nym','NYM'],
    'PNUT (Peanut the Squirrel)': ['peanut-the-squirrel','PNUT'],
    'TRUMP (MAGA)': ['maga','TRUMP'],
    'TRX (TRON)':['tron','TRX'],
    'VISTA (Ethervista)': ['ethervista','VISTA'],
    'XMR (Monero)':['monero','XMR'],
    'XRP (Ripple)':['ripple','XRP']
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
crypto_amount.bind('<Tab>',lambda event: recalc_cur())

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
rate_entry.bind('<Tab>',lambda event: recalc_crypto())

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

get_rate()

crypto_choose_win = Toplevel() # окно выбора криптовалюты
crypto_choose_win.withdraw()
crypto_choose_win.protocol('WM_DELETE_WINDOW', exit_win)
crypto_choose_win.title('Выбор криптовалюты')
crypto_choose_win.geometry('300x150+500+300')
choose_lbl = Label(crypto_choose_win, text='Выберите криптовалюту', font='Arial 16 bold')
crypto_combo2 = ttk.Combobox(crypto_choose_win, values=list(crypto_names.keys()),
                                state="readonly", font='Arial 10', justify='center', width=27)
btn1 = Button(crypto_choose_win, text='Закрыть', command=exit_win)

window.mainloop()
