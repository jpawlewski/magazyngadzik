import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from tkinter import *
import datetime
import webbrowser


large_font = ('Verdana', 30)
normal_font = ('Verdena', 7)

"""Twozenie listy przepisow do przyciskow w Tkinter"""
mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

iloscPrzepisow = len(onlyfiles)-2

listaPrzepisow = []
for item in onlyfiles:
    item = item.strip('.xlsx')
    if item == 'magazyn' or item == 'program.py' or item == 'dostawa.py':
        pass
    else:
        listaPrzepisow.append(item)

uwagaBrakTekst = "Wprowadz ilosc zrobionych chlebow gamoniu(tylko liczby)"

pobranoMag = "Produkty pobrano z magazynu"


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x500+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self. geom = geom


def clickAbout(tekst, ileKal, bclink):
    toplevel = Toplevel()
    label1 = Label(toplevel, text=tekst, height=0, width=100)
    label1.pack()
    label2 = Label(toplevel, text="Wartosc do wpisania w BreadCalculator : " + str(ileKal), font=large_font, height=0, width=100)
    label2.pack()
    b = Button(toplevel, text="Ok zamknij", font=large_font, width=20, command=lambda: [toplevel.destroy(), webbrowser.open(str(bclink), new=2)])
    b.pack()


def listabrakow():
    braki = []
    btn = []
    magazyn = pd.read_excel("magazyn.xlsx")
    magazyn2 = magazyn.set_index("produkt", drop=True)
    dictMagazyn = dict(zip(magazyn['produkt'], magazyn['ilosc']))
    for item in dictMagazyn:
        if dictMagazyn[item] < magazyn2.loc[item, 'alarm'] and item not in braki:
            brak = item + ' zostalo ' + str(dictMagazyn[item])
            braki.append(brak)
    toplevel = Toplevel()
    for i in range(len(braki)):
        btn.append(Button(toplevel, text=braki[i], height=1, font=normal_font))
        btn[i].pack(fill=BOTH)
    b = Button(toplevel, text="Ok zamknij braki", font=large_font, width=20, command=toplevel.destroy)
    b.pack()


def uwagaBrak(tekst, ilosc):
    info = 'Konczy sie ' + str(tekst) + '! Zostalo ' + str(ilosc) + ' g'
    toplevel = Toplevel()
    label1 = Label(toplevel, text=info, font=normal_font, width=100)
    label1.pack()
    b = Button(toplevel, text="Ok zamknij", font=normal_font, command=toplevel.destroy)
    b.pack()
    toplevel.configure(background='red')

wyswietlone = []


def clicked(chlebek):
    magazyn = pd.read_excel("magazyn.xlsx")
    magazyn2 = magazyn.set_index("produkt", drop=True)
    dictMagazyn = dict(zip(magazyn['produkt'], magazyn['ilosc']))
    nazwa = chlebek +'.xlsx'
    df1 = pd.read_excel(nazwa, sheet_name='Sheet1')
    bclink = df1.loc[0, 'bclink']
    print(bclink)
    ilosci = dict(zip(df1['nazwa produktu'], df1['potrzebna ilosc w g']))
    ileChlebow = iloscChlebow.get()
    iloscChlebow.delete(0, END)
    for key in ilosci:
        if key in dictMagazyn:
            uzyto = float(ilosci.get(key)) * float(ileChlebow)
            zmiana = magazyn2.loc[key, 'ilosc'] - uzyto
            magazyn2.loc[key, 'ilosc'] = zmiana
            zapis = pd.ExcelWriter("magazyn.xlsx")
            magazyn2.to_excel(zapis, "magazyn.xlsx")
            zapis.save()
        #else:
            #print('Nie znalazlem w magazynie: ', key, 'z przepisu:', chlebek)
    #  wartos¢i grniczne alarmøw magazynowych

    for item in dictMagazyn:
        if dictMagazyn[item] < magazyn2.loc[item, 'alarm'] and item not in wyswietlone:
            wyswietlone.append(item)
            uwagaBrak(item, dictMagazyn[item])
    ileKal = int(df1.loc[0,'waga porcji']) * int(ileChlebow)
    clickAbout(pobranoMag, ileKal, bclink)

root = Tk()
root.geometry("700x700+10+150")
label1 = Label(root, text="Program magazynowy")
label1.pack()
L1 = Label(root, text="Ilosc chlebow")
L1.pack()
iloscChlebow = Entry(root, width=50, font=large_font)
iloscChlebow.pack()
iloscChlebow.focus()

files = sorted(listaPrzepisow, key=str.lower)
btn = []
'''Len i range wykozystac do zrobienia kolumn (dodac jeszcze jednen loop'''
for i in range(len(files)):
    btn.append(Button(root, text=files[i], height=1, font=normal_font, command=lambda c=i: clicked(btn[c].cget("text"))))
    #btn[i].bind('<Return>', (lambda event: clicked(btn[i].cget("text"))))
    btn[i].pack(fill=BOTH)
b = Button(root, text="Koniec pracy", font=normal_font, command=root.destroy)
b.pack()
b2 = Button(root, text="Konczace sie produkty", font=normal_font, command=lambda : listabrakow())
b2.pack()

app = FullScreenApp(root)

root.mainloop()
