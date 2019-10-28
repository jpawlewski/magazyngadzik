
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from tkinter import *
import tkinter as Tk
import datetime
from selenium import webdriver


class VerticalScrolledFrame(Tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Tk.Scrollbar(self, orient=Tk.VERTICAL)
        vscrollbar.pack(fill=Tk.Y, side=Tk.RIGHT, expand=Tk.TRUE)
        canvas = Tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=Tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                        anchor=Tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


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


sesja = 0


def clickAbout(tekst, ileKal, bclink):    
    print(ileKal)
    global sesja
    print(sesja)
    driver = webdriver.Chrome(executable_path=r'/home/pedrak/anaconda3/lib/python3.6/site-packages/selenium/webdriver/chrome/chromedriver')
    sesja = driver
    webpage = r"{}".format(str(bclink))
    sesja.get(webpage)
    # sesja.execute_script("window.open('{}', 'new_window')".format(str(bclink)))
    sesja.maximize_window()  # For maximizing window
    sesja.implicitly_wait(40)  # gives an implicit wait for 20 seconds
    sbox1 = sesja.find_element_by_css_selector(".fbbc_total_weight")
    sbox1.click()
    sbox2 = sesja.find_element_by_css_selector(".fbbc_input_value")
    sbox2.click()
    sbox2.clear()
    sbox2.send_keys(str(ileKal))
    submit = sesja.find_element_by_css_selector("button.ui-button:nth-child(1)")
    submit.click()
    sbox4 = sesja.find_element_by_css_selector("span.gdpr-close:nth-child(3)")
    sbox4.click()
    sesja+=1
    # toplevel = Tk.Toplevel()
    # label1 = Tk.Label(toplevel, text=tekst, height=0, width=100)
    # label1.pack()
    # label2 = Tk.Label(toplevel, text="Wartosc do wpisania w BreadCalculator : " + str(ileKal), font=large_font, height=0, width=100)
    # label2.pack()
    # b = Tk.Button(toplevel, text="Ok zamknij", font=large_font, width=20, command=lambda: [toplevel.destroy()])
    # b.pack()


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
    toplevel = Tk.Toplevel()
    for i in range(len(braki)):
        btn.append(Tk.Button(toplevel, text=braki[i], height=1, font=normal_font))
        btn[i].pack(fill=BOTH)
    b = Tk.Button(toplevel, text="Ok zamknij braki", font=large_font, width=20, command=toplevel.destroy)
    b.pack()


def uwagaBrak(tekst, ilosc):
    info = 'Konczy sie ' + str(tekst) + '! Zostalo ' + str(ilosc) + ' g'
    toplevel = Tk.Toplevel()
    label1 = Tk.Label(toplevel, text=info, font=normal_font, width=100)
    label1.pack()
    b = Tk.Button(toplevel, text="Ok zamknij", font=normal_font, command=toplevel.destroy)
    b.pack()
    toplevel.configure(background='red')


wyswietlone = []


def clicked(chlebek):
    magazyn = pd.read_excel("magazyn.xlsx")
    magazyn2 = magazyn.set_index("produkt", drop=True)
    dictMagazyn = dict(zip(magazyn['produkt'], magazyn['ilosc']))
    nazwa = chlebek + '.xlsx'
    df1 = pd.read_excel(nazwa, sheet_name='Sheet1')
    bclink = df1.loc[0, 'bclink']
    ilosci = dict(zip(df1['nazwa produktu'], df1['potrzebna ilosc w g']))
    ileChlebow = iloscChlebow.get()
    iloscChlebow.delete(0, Tk.END)
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
    czas = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('wybierane.txt', 'a' ) as plik:
        plik.write(str(czas) + ' ' + nazwa + ' ilosc wybranych: ' + ileChlebow + ' pobrano z magazynu: ' + str(ilosci) + '\n')
    clickAbout(pobranoMag, ileKal, bclink)


def pobierzDodatki(wybor):
    magazyn = pd.read_excel("magazyn.xlsx")
    magazyn2 = magazyn.set_index("produkt", drop=True)
    dictMagazyn = dict(zip(magazyn['produkt'], magazyn['ilosc']))
    for key in dictMagazyn:
        if key == wybor:
            print("znaleziony")
            uzyto = float(iloscDodatkow.get())
            zmiana = magazyn2.loc[wybor, 'ilosc'] - uzyto
            magazyn2.loc[wybor, 'ilosc'] = zmiana
            zapis = pd.ExcelWriter("magazyn.xlsx")
            magazyn2.to_excel(zapis, "magazyn.xlsx")
            zapis.save()
    iloscDodatkow.delete(0, Tk.END)
    toplevel = Tk.Toplevel()
    label2 = Tk.Label(toplevel, text="Pobrano z magazynu %i g. %s" % (uzyto, wybor), font=large_font, height=0, width=100)
    label2.pack()
    b = Tk.Button(toplevel, text="Ok zamknij", font=large_font, width=20, command=lambda: [toplevel.destroy()])
    b.pack()


root = Tk.Tk()
root.geometry("700x700+10+150")
label1 = Tk.Label(root, text="Program magazynowy")
label1.pack()
L1 = Tk.Label(root, text="Ilosc chlebow")
L1.pack()
iloscChlebow = Tk.Entry(root, width=50, font=large_font)
iloscChlebow.pack()
iloscChlebow.focus()

scframe = VerticalScrolledFrame(root)
scframe.pack()

files = sorted(listaPrzepisow, key=str.lower)
btn = []
'''Len i range wykozystac do zrobienia kolumn (dodac jeszcze jednen loop'''
for i in range(len(files)):
    btn.append(Tk.Button(scframe.interior, text=files[i], width=50, height=1, font=normal_font, command=lambda c=i: clicked(btn[c].cget("text"))))
    # btn[i].bind('<Return>', (lambda event: clicked(btn[i].cget("text"))))
    btn[i].pack()

b = Tk.Button(root, text="Koniec pracy", font=normal_font, command=root.destroy)
b.pack()
b2 = Tk.Button(root, text="Konczace sie produkty", font=normal_font, command=lambda : listabrakow())
b2.pack()

skladniki = ['sol','mleko','chia','woda']
dodatframe = Frame(root)
dodatframe.pack()
variable = StringVar(dodatframe)
variable.set(skladniki[0]) # default value

w = OptionMenu(dodatframe, variable, *skladniki)
w.grid(row=0, column=0)
iloscDodatkow = Tk.Entry(dodatframe, width=20, font=normal_font)
iloscDodatkow.grid(row=0, column=1)
b3 = Tk.Button(dodatframe, text="Pobierz", font=normal_font, command=lambda : pobierzDodatki(variable.get()))
b3.grid(row=0, column=2)

app = FullScreenApp(root)

root.mainloop()
