from constants import CZARNY, FPS, SZEROKOSC_OKNA, WYSOKOSC_OKNA
import pygame

from entities.enemy_tank import EnemyTank
from entities.player_tank import PlayerTank
from entities.base import Base

from map.levels import WSZYSTKIE_POZIOMY
from map.tile import BrickWall,SteelWall,Water,Bush
from constants import ROZMIAR_KAFELKA




class Environment:
    def __init__(self):
        pygame.init()
        
        self.okno=pygame.display.set_mode((SZEROKOSC_OKNA,WYSOKOSC_OKNA))
        pygame.display.set_caption("TANKS 1990 / BATTLE CITY")

        self.dziala=True
        self.zegar=pygame.time.Clock()

        self.obiekty_w_grze=[]
        self.sciany=[]

        self.aktualny_numer_poziomu=0
        self.wynik=0
        self.zaladuj_poziom(self.aktualny_numer_poziomu)


    def zaladuj_poziom(self,numer):

        self.obiekty_w_grze=[]
        self.sciany=[]
        self.przeciwnicy=[]

        dane_poziomu=WSZYSTKIE_POZIOMY[numer]
        mapa=dane_poziomu["mapa"]
        start_x ,start_y=dane_poziomu["start_gracza"]
        wrog_x, wrog_y=dane_poziomu["start_wroga"]

        for wiersz_idx, wiersz in enumerate(mapa):
            for kolumna_idx,wartosc in enumerate(wiersz):

                px=kolumna_idx*ROZMIAR_KAFELKA
                py=wiersz_idx*ROZMIAR_KAFELKA

                nowy_kafelek=None
                if wartosc == 1:
                    polowa=ROZMIAR_KAFELKA//2
                    male_cegly=[
                        BrickWall(px,py),
                        BrickWall(px+polowa,py),
                        BrickWall(px,py+polowa),
                        BrickWall(px+polowa,py+polowa),
                        ]
                    for cegla in male_cegly:
                        self.obiekty_w_grze.append(cegla)
                        if cegla.blokuje_czolgi:
                            self.sciany.append(cegla)
                elif wartosc == 2:
                    nowy_kafelek=SteelWall(px,py)
                elif wartosc == 3:
                    nowy_kafelek=Water(px,py)
                elif wartosc == 4:
                    nowy_kafelek=Bush(px,py)

                if nowy_kafelek:
                    self.obiekty_w_grze.append(nowy_kafelek)

                    if nowy_kafelek.blokuje_czolgi:
                        self.sciany.append(nowy_kafelek)
                
                    


        self.baza=Base(12*ROZMIAR_KAFELKA,12*ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.baza)

        self.gracz=PlayerTank(start_x*ROZMIAR_KAFELKA, start_y*ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.gracz)

        self.przeciwnik=EnemyTank(1*ROZMIAR_KAFELKA,1*ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.przeciwnik)
        self.przeciwnicy.append(self.przeciwnik)

    
    def nastepny_poziom(self):
        self.aktualny_numer_poziomu+=1
        if self.aktualny_numer_poziomu<len(WSZYSTKIE_POZIOMY):
            self.zaladuj_poziom(self.aktualny_numer_poziomu)
        else:
            print("GRATULACJE PRZESZEDLES GRE")
            self.dziala=False

    def obsluga_zdarzen(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.dziala=False

    def aktualizacja(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            nowy_pocisk=self.gracz.strzelaj()
            if nowy_pocisk:
                self.obiekty_w_grze.append(nowy_pocisk)

        for wrog in self.przeciwnicy:
            nowy_pocisk=wrog.strzelaj()
            if nowy_pocisk:
                self.obiekty_w_grze.append(nowy_pocisk)

        for obiekt in self.obiekty_w_grze:
            if obiekt==self.gracz or isinstance(obiekt,EnemyTank):
                obiekt.update(self.sciany)
            else:
                obiekt.update()


        for obj in self.obiekty_w_grze:
            if hasattr(obj,'kierunek') and hasattr(obj,'wlasciciel'):

                if obj.hitbox.colliderect(self.baza.hitbox) and not self.baza.zniszczona:
                    obj.aktywny=False
                    self.baza.zniszczona=True
                    print("KONIEC GRY - ZNISZCZONA BAZA")
                    self.dziala=False

                for sciana in self.sciany:
                    if obj.hitbox.colliderect(sciana.hitbox) and sciana.blokuje_pociski:
                        obj.aktywny=False

                        if getattr(sciana,'zniszczalny',False):
                            if sciana in self.obiekty_w_grze:
                                self.obiekty_w_grze.remove(sciana)
                            if sciana in self.sciany:
                                self.sciany.remove(sciana)
                        break

                if obj.wlasciciel=="wrog" and obj.hitbox.colliderect(self.gracz.hitbox) and obj.aktywny:
                    obj.aktywny=False
                    self.gracz.liczba_zyc-=1
                    print(f"OBERWALES Zostalo zyc: {self.gracz.liczba_zyc}")
                    if self.gracz.liczba_zyc<=0:
                        print("KONIEC GRY ZABITO GRACZA")
                        self.dziala=False

                if obj.wlasciciel=="gracz" and obj.aktywny:
                    for wrog in self.przeciwnicy:
                        if obj.hitbox.colliderect(wrog.hitbox):
                            obj.aktywny=False
                            wrog.hp-=1

                            if wrog.hp<=0:
                                self.przeciwnicy.remove(wrog)
                                self.obiekty_w_grze.remove(wrog)
                                self.wynik+=100
                            break


        nowa_lista=[]


        for obj in self.obiekty_w_grze:
            if hasattr(obj,'kierunek') and hasattr(obj,'wlasciciel'):
                if 0<=obj.x<=800 and 0<=obj.y<=600 and obj.aktywny:
                    nowa_lista.append(obj)
            else:
                nowa_lista.append(obj)

        self.obiekty_w_grze=nowa_lista

        if len(self.przeciwnicy)==0:
            print("ZABITO WSZYSTKICH NASTEPNY POZIOM")
            self.nastepny_poziom()



#WYGENEROWANE PRZEZ AI

    def rysuj_hud(self):
        czcionka = pygame.font.SysFont("Arial", 24, bold=True)
        
        # Generujemy teksty (tekst, wyg³adzanie, kolor RGB)
        tekst_zycia = czcionka.render(f"Zycia: {self.gracz.liczba_zyc}", True, (255, 255, 255))
        tekst_wynik = czcionka.render(f"Wynik: {self.wynik}", True, (255, 255, 255))
        tekst_poziom = czcionka.render(f"Poziom: {self.aktualny_numer_poziomu + 1}", True, (255, 255, 255))
        tekst_wrogowie = czcionka.render(f"Wrogowie: {len(self.przeciwnicy)}", True, (255, 255, 255))

        # Naklejamy teksty na okno gry w prawym lub lewym górnym rogu
        self.okno.blit(tekst_zycia, (10, 10))
        self.okno.blit(tekst_wynik, (150, 10))
        self.okno.blit(tekst_poziom, (350, 10))
        self.okno.blit(tekst_wrogowie, (500, 10))

    def rysowanie(self):
        self.okno.fill(CZARNY)

        for obiekt in self.obiekty_w_grze:
            if not isinstance(obiekt,Bush):
                obiekt.draw(self.okno)

        for obiekt in self.obiekty_w_grze:
            if isinstance(obiekt,Bush):
                obiekt.draw(self.okno)
        self.rysuj_hud()

        pygame.display.flip()


    def uruchom(self):
        while self.dziala:
            self.obsluga_zdarzen()
            self.aktualizacja()
            self.rysowanie()
            self.zegar.tick(FPS)

        pygame.quit()

