try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame as pg
    from socket import *
    from pygame.locals import *
except ImportError:
    print(f"couldn't load module. {ImportError}")
    sys.exit(2)


#Siia tulevad mõned globaalsed muutujad, mida vajan ühes ja/või teises kohas:
suva_algus = 60
suva_lõpp = 200

def load_png(name): #Credit pygame tutorial 3.2
    """ Load image and return image object"""
    fullname = os.path.join(os.path.dirname(__file__),"data", name)
    #try:
    image = pg.image.load(fullname)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    #except FileNotFoundError:
       # print(f"Cannot load image: {fullname}")
        #raise SystemExit
    return image, image.get_rect()

def mängu_lõpp():
    mängu_lõpp= True
    while mängu_lõpp:
        for sündmus in pg.event.get():
            if sündmus.type == pg.KEYDOWN:
                if sündmus.key == pg.K_r:
                    mäng_käib=True
                    main()

class Lind():
    """
    siia tuleb linnuga seotud kood, mis paneb ta lendama ja ilus olema ja muud toredat.
    muutujad:
    funktsioonid: init, hüppa, uuenda, joonista
    muud tähtsat:
    """
    def __init__(self, x,y):
        try:
            self.pilt, self.lind = load_png("linnupilt.png") #ükspäev tuleb siia linnukesest pilt
            self.pilt=pg.transform.scale(self.pilt, (30,30))
            self.lind = pg.Rect((100,300),(30,30))
        except:
            self.lind = pg.Rect((100,300),(30,30))
            self.pilt= pg.Surface((30,30), pg.SRCALPHA)
            self.pilt.fill((255,255,0))
        self.lind.topleft = (x,y)
        self.kiirus_y=float(0)
        self.grav=0.1
        
    def hüppa(self): #paneb linnu tõusma
        self.kiirus_y=-3.5
    
    def uuenda(self, ala): #liigutab lindu ja kontrollib, et lind ei oleks laes/põrandas, kui on siis lükkab mängu kinni ;D
        self.kiirus_y+=self.grav
        self.lind.y+=self.kiirus_y
        self.lind.clamp_ip(ala)
        if self.lind.top==ala.top or self.lind.bottom==ala.bottom:
            self.kiirus_y=0
            self.grav=0
            return True
        return False
    
    def joonista(self, ekraan): #Joonistab linnukese iga kaader ekraanile ja ka tegeleb linnu pööramisega vastavalt vertikaalsele kiirusele
        nurk = max(-65,-self.kiirus_y*8)
        pööratud = pg.transform.rotate(self.pilt, nurk)
        pööratudRect=pööratud.get_rect(center = self.lind.center)
        ekraan.blit(pööratud, pööratudRect)



class torupaar():
    """
    Siia tuleb torudele omadele loogika jm siuke, Lisaks ka liigutamine jpt asjad
    funktsioonid: init, uuenda, joonista, põrkaja, loe 
    muutujad: ala, ekraan, self, vahe, suva_algus/lõpp
    muud tähtsat: 
    """
    def __init__(self, x, ala, vahe=120): #algne setup, pildiga sidumine (kui on)
        suvaline_kõrgus = random.randint(suva_algus,suva_lõpp)
        self.x= x
        self.lugeja = pg.Rect((x+25,0),(25,ala.height))
        self.loetud = False
        self.alumine = pg.Rect((x,300),(50,150))
        self.ülemine = pg.Rect((x,100),(50,100))
        self.alumine.height = suvaline_kõrgus
        self.alumine.bottom = ala.bottom
        self.ülemine.top = ala.top
        self.ülemine.height = self.alumine.top-vahe
        try:
            self.pilt1, _ = load_png("torupilt1.png")
            self.pilt2, _ = load_png("torupilt2.png")
            self.skaleeritud1=pg.transform.scale(self.pilt1, self.alumine.size)
            self.skaleeritud2=pg.transform.scale(self.pilt2, self.ülemine.size)
        except:
            self.pilt1 = None
            self.pilt2 = None
        
    
    def uuenda(self, kiirus, ala, vahe=120): #liigutamine j värki
        kiirus=float(kiirus)
        self.x -= float(kiirus)
        self.alumine.left = self.x
        self.ülemine.left = self.x
        self.lugeja.left = self.x + 25
        
        if (self.x + 50)< 0: #liigutame teisele poole ekraani ja määrame uue kõrguse
            self.x = ala.right
            self.alumine.height = random.randint(suva_algus,suva_lõpp)
            self.alumine.bottom = ala.bottom
            self.ülemine.top = ala.top
            self.ülemine.height = self.alumine.top-vahe
            self.loetud = False
            if self.pilt1 != None and self.pilt2 != None:
                self.skaleeritud1=pg.transform.scale(self.pilt1, self.alumine.size)
                self.skaleeritud2=pg.transform.scale(self.pilt2, self.ülemine.size)


            
    
    def joonista(self,ekraan): #Siin toimub püha blittimine ja muu joonistus
        if self.pilt1 == None:
            pg.draw.rect(ekraan, (0,255,0), self.alumine)
        else:
            ekraan.blit(self.skaleeritud1, self.alumine)
        if self.pilt2 == None:
            pg.draw.rect(ekraan, (0,255,0), self.ülemine)
        else:
            ekraan.blit(self.skaleeritud2, self.ülemine)
            
            
    
    def põrkaja(self, lind_rect): #kontrollime, et kas lind on 9/11 teinud
        return self.alumine.colliderect(lind_rect) or self.ülemine.colliderect(lind_rect)
    
    def loe(self,lind_rect): #loeme punkte ka!
        if self.lugeja.colliderect(lind_rect):
            if self.loetud == False:
                self.loetud = True
                return True
        return False
            


        

def main():
    pg.init()
    #muutujate ala
    font=pg.font.SysFont("Arial", 36)
    algusfont=pg.font.SysFont("Arial", 25)
    ekraan = pg.display.set_mode((600, 400))
    kell = pg.time.Clock()
    ala=ekraan.get_rect()
    linnuke = Lind(100,200)
    torud = []
    torud.append(torupaar(400, ala))
    torud.append(torupaar(617, ala))
    torud.append(torupaar(834, ala))
    
    mäng_käib= True
    kiirus_x=float(1.0)
    Skoor=0
    ootab= True
    
    #Startup screen
    
    ekraan.fill((135,206,235))
    linnuke.joonista(ekraan)
    for toru in torud:
        toru.joonista(ekraan)
    tekst=algusfont.render("Vajuta W, Space, või nool üles, et alustada!", True, "Red")
    tekstbox = tekst.get_rect(center=(300,40))
    ekraan.blit(tekst, tekstbox)
        
    pg.display.flip()
    #otsib vajutust
    while ootab:
        kell.tick(60)
        
        #tuvastuste ala
        
        for sündmus in pg.event.get():
            if sündmus.type==pg.KEYDOWN:
                if sündmus.key==pg.K_SPACE or sündmus.key==pg.K_w or   sündmus.key==pg.K_UP: 
                    linnuke.hüppa()
                    ootab = False
            if sündmus.type == pg.QUIT:
                mäng_käib=False
                ootab = False
    #game time
    while mäng_käib:
        #Ülesseadmise ala
        ekraan.fill((135,206,235))
        linnuke.joonista(ekraan)
        for toru in torud:
            toru.joonista(ekraan)
        tekst=font.render(str(Skoor), True, "Red")
        tekstbox = tekst.get_rect(center=(300,40))
        ekraan.blit(tekst, tekstbox)
        
        pg.display.flip()
        kell.tick(60)
        
        #tuvastuste ala
        
        for sündmus in pg.event.get():
            if sündmus.type==pg.KEYDOWN:
                if sündmus.key==pg.K_SPACE or sündmus.key==pg.K_w or   sündmus.key==pg.K_UP: 
                    linnuke.hüppa()
            if sündmus.type == pg.QUIT:
                mäng_käib=False
        for toru in torud:
            if toru.põrkaja(linnuke.lind):
                kiirus_x=0
                linnuke.kiirus_y=0
                linnuke.grav=0
                mäng_käib=False
        
        for toru in torud:
            if toru.loe(linnuke.lind):
                Skoor+=1
                kiirus_x=kiirus_x+0.1
        #liikumine
        for toru in torud:
            toru.uuenda(kiirus_x,ala)
        if linnuke.uuenda(ala):
            mäng_käib=False
    mängu_lõpp()
    pg.event.pump()
    pg.quit()
    return Skoor

if __name__== "__main__":
    print(main())
    sys.exit()

        