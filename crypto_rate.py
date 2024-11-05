from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


def get_rate():
    pass

window = Tk()
window.title('Курсы криптовалют')
window.geometry('300x200')

crypto_names = [
    'Bitcoin',
    'Etherium',
    'Ripple',
    'Litecoin',
    'Cardano'
]

crypto_combo = ttk.Combobox(values=crypto_names)
crypto_combo.pack(padx=10,pady=10)

btn = Button(text='Получить курс валюты к USD', command=get_rate)
btn.pack(padx=10,pady=10)

lbl = Label(text='')
lbl.pack(padx=10,pady=10)

window.mainloop()
