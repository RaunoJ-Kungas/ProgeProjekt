from tkinter import *
from tkinter import ttk
"""

See on programmi internal readme sektsioon. 
Siin on aktuaalsed seletused kuidas programm toimib, 
et collaboration sujuks tõhusamalt.

paths.txt failis on kõik tekstid ja valikud, mis kuvatakse kasutajale.
Selle faili ülesehitus on igal real selline:
indeks;tekst;valik1;indeks1;valik2;indeks2;valik3;indeks3

Seletan nüüd täpsemalt:
indeks - nagu nimigi ütleb, on see indeks. Indeks on tekst ("1").
tekst - see on tekst, mis kuvatakse kasutajale.
valikx - see on esimene valik, mis kuvatakse kasutajale.
indeksx - see on indeks, kuhu kasutaja suunatakse, kui ta valib valikx.

Seega, indeks -> tekst -> valik1 -> indeks1 -> tekst1 jne.

Põhjus miks ma kasutan indeksit (ja sellega sõnastikku - **read 2 paragraafi hiljem**), on see, 
et see võimaldab meil muuta paths.txt faili sisu ilma, et peaksin muutma ridade järjestust.

loe_failist() töö põhimõte on lugeda paths.txt faili sisu ja salvestada see sõnastikku.
Sõnastiku võtmed on indeksid ja väärtused on listid, kus esimene element on tekst ja teine element on valikud.

Loodan, et oled tutvunud varem sõnastike põhimõttega, kui mitte, siis siin on link:
https://progeopik.cs.ut.ee/10_andmestruktuurid.html


P.S. Kommenteerin ka koodi vahele väikeseid tid-bit'e.
"""
# Sätted mida olen hetkel viitsinud teha:

tekstFont = "Helvetica"
tekstFontSize = 14

nuppFont = "Comic Sans MS"
nuppFontSize = 12

def loe_failist():
    lood = {}
    fail = open("paths.txt", encoding="UTF-8")
    for rida in fail:
        rida = rida.strip()
        if rida == "":
            continue
        osad = rida.split(";")
        indeks = osad[0]
        tekst = osad[1].replace("_", "\n")              # Tekstis asendatakse kõik "_" sümbolid reavahetusega, et saaks paragraafe teha.
        valikud = []
        for i in range(2, len(osad)-1, 2):              # TIL: range() saab kasutada sedasi: range(indeks kust alustad, indeks kus lõpetad, *samm*).
            if osad[i] != "":
                valikud.append([osad[i], osad[i + 1]])  # Salvestab valikud listi, kus iga valik on list, mis sisaldab valiku teksti ja indeksi. [0] on tekst, [1] on indeks.
        lood[indeks] = [tekst, valikud]                 # Seega lood[indeks] = [tekst, [[tekst, indeks][tekst, indeks][tekst, indeks]]]
    fail.close()
    return lood                                         # NB! Tagastab siis kogu sõnastiku.



def naita(indeks):
    global valikud
    if indeks not in lood:
        print("Indeksit", indeks, "ei leitud failist paths.txt")
        return
    tekst = lood[indeks][0]
    valikud = lood[indeks][1]
# Hetkel viib otse tagasi esimesele indeksile kui valesti oled midagi teinud, 
# kuid ma tahaks teha menüü kus saab valida "New Game", "Load Game", "Achievements" või "Exit". 
# Oleneb mis suunas me minna tahame mänguga.
    if len(valikud) == 0:
        valikud = [["Lõpp - alusta uuesti", "1"]]
    tekstikast.config(state=NORMAL)
    tekstikast.delete("1.0", END)
    tekstikast.insert("1.0", tekst)
    tekstikast.config(state=DISABLED)
# Siin liidame nuppudele teksti juurde ja aktiveerime/deaktiveerime neid, kui valikuid on vähem kui 3.
    for i in range(len(nupud)):
        if i < len(valikud):
            nupud[i].config(text=valikud[i][0], state=NORMAL)
        else:
            nupud[i].config(text="", state=DISABLED)

# nuppx jaoks tegin eraldi funktsioonid, mis toimivad nupu vajutusel.
# naita(valikud[x][1]) on siis tulevase teksti indeksi järgi uue teksti kuvamine, /if that makes sense/.

def valik1():
    naita(valikud[0][1])

def valik2():
    naita(valikud[1][1])

def valik3():
    naita(valikud[2][1])

# Okei siin nüüd praktiliselt algab programm peale pikka 'eelmängu'.

lood = loe_failist()
valikud = []

aken = Tk()
aken.title("Survive the weekend at Pērnava")
aken.geometry("1000x600")

# Jaotan selle akna (GUI) n-õ kolmeks veeruks (weight 2+1 = 3), aga suurem weight = suurem osakaal. Sel juhul on 2/3 ja 1/3.
# See uniform="a" on selleks, et need kaks veergu jagaksid ruumi vastavalt weight väärtusele. 
# See "a" on põhimõtteliselt klass.

aken.columnconfigure(0, weight=2, uniform="a")
aken.columnconfigure(1, weight=1, uniform="a")
aken.rowconfigure(0, weight=1)

tekstikast = Text(aken, wrap=WORD, font=(tekstFont, tekstFontSize), state=DISABLED)
tekstikast.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

parem = Frame(aken)
parem.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
parem.columnconfigure(0, weight=1)
for i in range(3):
    parem.rowconfigure(i, weight=1, uniform="b")

# Siin seadistab mis nupud on ja kus asuvad, olulisemaks muutub see def näita() funktsioonis kus liidame neile teksti juurde.

nupp1 = Button(parem, font=(nuppFont, nuppFontSize), wraplength=250, command=valik1)
nupp2 = Button(parem, font=(nuppFont, nuppFontSize), wraplength=250, command=valik2)
nupp3 = Button(parem, font=(nuppFont, nuppFontSize), wraplength=250, command=valik3)
nupp1.grid(row=0, column=0, sticky="nsew", pady=5)
nupp2.grid(row=1, column=0, sticky="nsew", pady=5)
nupp3.grid(row=2, column=0, sticky="nsew", pady=5)
nupud = [nupp1, nupp2, nupp3]

#Lisasin nuppudele hover efekti, sest lugesin selle kohta just ja tahtsin seda teha. vb tuleb veic seda sättida prst aga jaa.
nupp1.bind("<Enter>", lambda event: nupp1.config(borderwidth=3, relief='sunken', bg='lightgray'))
nupp1.bind("<Leave>", lambda event: nupp1.config(borderwidth=0, relief='raised', bg='SystemButtonFace'))
nupp2.bind("<Enter>", lambda event: nupp2.config(borderwidth=3, relief='sunken', bg='lightgray'))
nupp2.bind("<Leave>", lambda event: nupp2.config(borderwidth=0, relief='raised', bg='SystemButtonFace'))
nupp3.bind("<Enter>", lambda event: nupp3.config(borderwidth=3, relief='sunken', bg='lightgray'))
nupp3.bind("<Leave>", lambda event: nupp3.config(borderwidth=0, relief='raised', bg='SystemButtonFace'))



naita("1")
aken.mainloop()