from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from datetime import datetime
import pandas as pd
import requests
import json
import os
import aboutcrypto as ac


exchange_rate = None # переменная для курса выбранной криптовалюты
crypto_combo2 = None
crypto_choose_win = None
counter = 0 # счетчик для количества запросов к api
coins_list_url = 'https://api.coingecko.com/api/v3/coins/list' # список всех криптовалют coingecko
crypto_rates_file = 'crypto_rates.txt' # файл для сохранения курсов валют
crypto_dict_file = 'crypto_dict.json' # файл для хранения библиотеки криптовалют
crypto_list_file = 'crypto_list.xlsx' # файл для сохранения списка криптовалют
crypto_names = {}
currency_names = {
    'CNY (Китайский юань)': 'cny',
    'EUR (Евро)': 'eur',
    'JPY (Японская йена)': 'jpy',
    'KRW (Южнокорейская вона': 'krw',
    'RUB (Российский рубль)': 'rub',
    'USD (Доллар США)': 'usd'
}


def get_crypto_dict(): # считываем из файла библиотеку с сокращенными и полными названиями криптовалют и их id для api
    global crypto_names
    if os.path.exists(crypto_dict_file):
        with open(crypto_dict_file,'r') as f:
            crypto_names = json.load(f)
    else:
        mb.showerror('Ошибка!','Проблема с библиотекой криптовалют,\nобратитесь к администратору')


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
    global crypto_combo2
    global crypto_choose_win
    crypto_choose_win = Toplevel(window)  # окно выбора криптовалюты
    crypto_choose_win.protocol('WM_DELETE_WINDOW',
                               hide_win)  # при нажатии на крестик, окно не закрывается, а скрывается
    crypto_choose_win.title('Выбор криптовалюты')
    crypto_choose_win.geometry('300x150+500+300')
    choose_lbl = Label(crypto_choose_win, text='Выберите криптовалюту', font='Arial 16 bold')
    choose_lbl.pack(pady=10)
    crypto_combo2 = ttk.Combobox(crypto_choose_win, values=list(crypto_names.keys()),
                                 state="readonly", font='Arial 10', justify='center', width=27)
    crypto_combo2.pack(pady=10)
    crypto_combo2.set('BTC (Bitcoin)')
    crypto_combo2.bind('<<ComboboxSelected>>', lambda event: show_info())
    btn1 = Button(crypto_choose_win, text='Показать инфо', font='Arial 10', command=show_info)
    btn1.pack()


def show_info(): # функция отображения информации о криптовалюте
    global counter
    crypto_name = crypto_combo2.get() # получение наименования выбранной криптовалюты
    hide_win() # скрывается окно выбора криптовалюты
    show_win = Toplevel() # создается новое окно
    show_win.title('Информация о криптовалюте')
    show_win.geometry('620x350')
    Label(show_win, text='Основная информация о криптовалюте', font='Arial 14 bold',bg='white').grid(row=0,column=0,columnspan=5,sticky='ew',pady=10, padx=10)
    Label(show_win,text='Название криптовалюты:',font='Arial 10', width=28).grid(row=1,column=0,padx=5)
    Label(show_win, text=f'{crypto_names[crypto_name][2]}',font='Arial 10 bold', bg='white',width=15,borderwidth=2,relief='ridge').grid(row=1,column=1,ipadx=5,ipady=2,padx=2)
    Label(show_win, text='Сокращённое название:',font='Arial 10').grid(row=2,column=0)
    Label(show_win, text=f'{crypto_names[crypto_name][1]}',font='Arial 10 bold', bg='white',width=15,borderwidth=2,relief='ridge').grid(row=2,column=1,ipadx=5,ipady=2,padx=2)
    cur_l = Label(show_win, text='Текущий курс в $:', font='Arial 14 bold')
    cur_l.grid(row=1, column=2, rowspan=2, columnspan=2, padx=(10, 0))
    logo_l = Label(show_win, text='Логотип:', font='Arial 10')
    logo_l.grid(row=1, column=4, rowspan=2)
    Label(show_win, text='Сейчас в обращении:', font='Arial 10').grid(row=3, column=0)
    amount_l = Label(show_win, text='', font='Arial 10 bold', bg='white',width=15,borderwidth=2,relief='ridge')
    amount_l.grid(row=3,column=1,ipadx=5,ipady=2,padx=2)
    Label(show_win, text='Макс. возможное количество:', font='Arial 10').grid(row=4, column=0)
    max_amount_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=15, borderwidth=2, relief='ridge')
    max_amount_l.grid(row=4,column=1,ipadx=5,ipady=2,padx=2)
    Label(show_win, text='Исторические значения', font='Arial 12 bold').grid(row=5, column=0,columnspan=2, sticky='ew',pady=(15,2))
    Label(show_win, text='Максимум:', font='Arial 10').grid(row=6, column=0, sticky='e')
    max_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=15, borderwidth=2, relief='ridge')
    max_l.grid(row=6,column=1,ipadx=5,ipady=2,padx=2)
    Label(show_win, text='Дата максимума:', font='Arial 10').grid(row=7, column=0, sticky='e')
    max_date_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=15, borderwidth=2, relief='ridge')
    max_date_l.grid(row=7, column=1, ipadx=5, ipady=2, padx=2)
    Label(show_win, text='Минимум:', font='Arial 10').grid(row=8, column=0, sticky='e')
    min_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=15, borderwidth=2, relief='ridge')
    min_l.grid(row=8, column=1, ipadx=5, ipady=2, padx=2)
    Label(show_win, text='Дата минимума:', font='Arial 10').grid(row=9, column=0, sticky='e')
    min_date_l =Label(show_win, text='', font='Arial 10 bold', bg='white', width=15, borderwidth=2, relief='ridge')
    min_date_l.grid(row=9, column=1, ipadx=5, ipady=2, padx=2)
    Label(show_win, text='24 часа', font='Arial 10',borderwidth=2, relief='ridge').grid(row=3, column=2, padx=(10, 0))
    day_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=5, borderwidth=2, relief='ridge')
    day_l.grid(row=4, column=2, ipadx=5, ipady=2, padx=(10, 0))
    Label(show_win, text='30 дней', font='Arial 10',borderwidth=2, relief='ridge').grid(row=3, column=3)
    month_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=5, borderwidth=2, relief='ridge')
    month_l.grid(row=4, column=3, ipadx=5, ipady=2)
    Label(show_win, text='1 год', font='Arial 10',borderwidth=2, relief='ridge').grid(row=3, column=4)
    year_l = Label(show_win, text='', font='Arial 10 bold', bg='white', width=6, borderwidth=2, relief='ridge')
    year_l.grid(row=4, column=4, ipadx=5, ipady=2)
    market_l = Label(show_win, text='Самая популярная биржа - ', font='Arial 10 bold')
    market_l.grid(row=10, column=0, columnspan=2, sticky='w', pady=(15, 2), padx=10)


    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{crypto_names[crypto_name][0]}')
        response.raise_for_status()
        counter += 1  # если не возникло исключение, счетчик увеличится на 1
        counter_lbl.config(text=f'Использовано запросов: {counter}')
        data = response.json()
        ac.about(data) # распределение данных, полученных от api, по переменным
        print('kz',ac.cur_price)
        cur_l.config(text=f'$ {ac.cur_price}')
        amount_l.config(text=ac.amount_now)
        max_amount_l.config(text=ac.max_amount)
        max_l.config(text=f'$ {ac.max_price}')
        max_date_l.config(text=ac.max_date)
        min_l.config(text=f'$ {ac.min_price}')
        min_date_l.config(text=ac.min_date)
        day_l.config(text=f' {ac.perc_day}%')
        day_l.config(foreground='green') if ac.perc_day !='-' and ac.perc_day > 0 else day_l.config(foreground='red')
        month_l.config(text=f' {ac.perc_month}%')
        month_l.config(foreground='green') if ac.perc_month !='-' and ac.perc_month > 0 else month_l.config(foreground='red')
        year_l.config(text=f' {ac.perc_year}%')
        year_l.config(foreground='green') if ac.perc_year !='-' and ac.perc_year > 0 else year_l.config(foreground='red')
        market_l.config(text=f'Самая популярная биржа - "{ac.market}"')
        if ac.logo != '-':
            logo_l.config(image=ac.logo)
            logo_l.image = ac.logo # чтобы сборщик мусора не убрал картинку






    except Exception as e:
        mb.showerror('Ошибка', f'Возникла ошибка: {e}')


def add_crypto():
    global crypto_names
    global counter
    found_cryptos = {}
    cryptos_id = [crypto_id for key, [crypto_id,short_n, name1] in crypto_names.items()] # список id криптовалют библиотеки crypto_names
    new_crypto = sd.askstring('Добавление', 'Введите полное или сокращённое название криптовалюты,\nнапример, "Bitcoin" или "BTC"')
    if new_crypto:
        new_crypto = new_crypto.strip().lower()
        try:
            response = requests.get(coins_list_url)
            response.raise_for_status()
            counter += 1
            counter_lbl.config(text=f'Использовано запросов: {counter}')
            data = response.json()
            for coin in data:
                if new_crypto in [coin['id'].lower(),coin['symbol'].lower(),coin['name'].lower()] and coin['id'] not in cryptos_id:
                    if coin['symbol'].lower() != coin['name'].lower():
                        name = f'{coin['symbol'].upper()} ({coin['name']})'
                    else:
                        name = coin['symbol'].upper()
                    found_cryptos[name] = [coin['id'], coin['symbol'].upper(), coin['name']]
            if len(found_cryptos) == 1:
                answer = mb.askyesno('Добавить?',f'Найдена новая криптовалюта "{name}", добавить?')
                if answer:
                    crypto_names.update(found_cryptos) # добавить данные о новой криптовалюте в словарь
                    update_crypto_dict_f() # обновить файл json
                    crypto_combo.config(values=list(crypto_names.keys())) # обновить выпадающий список с криптовалютами
                else:
                    return
            elif len(found_cryptos) == 0:
                mb.showerror('Ошибка',f'Криптовалюта "{new_crypto}" не найдена или уже добавлена, обратитесь к списку криптовалют')
            else:
                mb.showwarning('Внимание',f'Найдено несколько ({len(found_cryptos)}) криптовалют\n\n "Сокращение (Полное_название)":\n{'\n'.join([name for name in found_cryptos.keys()])},\n\n уточните название')
        except Exception as e:
            mb.showerror('Ошибка',f'Произошла ошибка {e}')
    else:
        mb.showerror('Ошибка добавления','Название криптовалюты не введено')


def update_crypto_dict_f(): # функция обновления файла json
     with open(crypto_dict_file,'w') as f:
        json.dump(crypto_names, f, indent=4)


def save_rate(): # функция сохранения курса криптовалюты
    rate = crypto_cur_lbl['text']
    last_update = last_upd_lbl['text']
    res = f'\n{rate[19:]} ({last_update[18:28]} {last_update[-5:]})'
    answer = mb.askyesno('Сохранение курса',f'{res}\n\n - сохранить данные?')
    if answer:
        with open(crypto_rates_file,'a+', encoding='utf-8') as f:
            f.write(res)
        mb.showinfo('Успешно', 'Данные успешно сохранены')
    else:
        mb.showwarning('Внимание','Данные не сохранены')


def show_history(): # Функция отображения сохраненных курсов криптовалют
    if not os.path.exists(crypto_rates_file):
        mb.showerror('Ошибка', 'Нет сохранённых данных')
        return
    history_window = Toplevel()
    history_window.title('Сохраненные курсы криптовалюты')
    history_window.geometry('500x300')
    history_text = Text(history_window, width=59, height=18)
    history_text.pack(side=LEFT)
    scroll = Scrollbar(history_window, command=history_text.yview)
    scroll.pack(side=LEFT, fill=Y)
    history_text.config(yscrollcommand=scroll.set)
    with open(crypto_rates_file, 'r', encoding='utf-8') as f:
        history = f.read()
        for item in history:
            res_text = item
            history_text.insert(END, res_text)
    history_text.config(state='disabled')


def save_crypto_list(): # Функция сохранения полного списка криптовалют в файл
    global counter
    coin_names, coin_symbols = [], []
    if os.path.exists(crypto_list_file):
        answer = mb.askyesno('Файл уже существует','Перезаписать?')
        if not answer:
            return
    try:
        response = requests.get(coins_list_url)
        response.raise_for_status()
        counter += 1
        counter_lbl.config(text=f'Использовано запросов: {counter}')
        data = response.json()
        for coin in data:
            coin_symbols.append(coin['symbol'])
            coin_names.append(coin['name'])
        df = pd.DataFrame({
            'Сокращение': coin_symbols,
            'Наименование': coin_names
        })
        df.to_excel(crypto_list_file)
        mb.showinfo('Успех','Список криптовалют сохранён')
    except Exception as e:
        mb.showerror('Ошибка', f'Произошла ошибка {e}')


def hide_win(): # функция сокрытия дочернего окна
    crypto_choose_win.withdraw()


def exit(): # функция закрытия главного окна
    window.destroy()


get_crypto_dict() # Получить из файла json библиотеку имён криптовалют

window = Tk()
window.title('Конвертер криптовалют')
window.geometry('400x380')
window.iconbitmap(default='crypto.ico')

mainmenu = Menu(window)
window.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Файл", menu=filemenu)
filemenu.add_command(label="Сохранить курс", command=save_rate)
filemenu.add_command(label="История сохранений", command=show_history)
filemenu.add_separator()
filemenu.add_command(label="Закрыть", command=exit)

cryptomenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Криптовалюты", menu=cryptomenu)
cryptomenu.add_command(label="Добавить новую криптовалюту", command=add_crypto)
cryptomenu.add_command(label="Инфо о криптовалюте", command=choose_crypto)
cryptomenu.add_command(label="Скачать список криптовалют", command=save_crypto_list)

Label(text='Криптовалюта',font='Arial 14 bold').grid(row=0,column=0,columnspan=2,sticky='ew',ipady=10)

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

Label(text='Целевая валюта', font='Arial 14 bold').grid(row=2,column=0,columnspan=2,sticky='ew',ipady=10)

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
crypto_cur_lbl = Label(text='',font='Arial 10 bold')
crypto_cur_lbl.grid(row=5,column=0,columnspan=2,pady=(20,0))

# Метка для отображения времени последнего обновления данных о курсе валюты
last_upd_lbl = Label(text='',font='Arial 10')
last_upd_lbl.grid(row=6,column=0,columnspan=2,pady=(10,20))

# Метка для отображения счетчика
counter_lbl = Label(text='',font='Arial 10 italic', fg='orchid4')
counter_lbl.grid(row=7,column=0,columnspan=2,pady=(20,10))

if crypto_names:
    get_rate() # отобразить на экране значение курса криптовалюты, по умолчанию Биткоин к доллару США
else:
    crypto_cur_lbl.config(text='Ошибка получения данных!')



window.mainloop()
