import pygame
import random
from constants import ROZMIAR_KAFELKA
from map.spritesheet import arkusz_grafik
from entities.powerups import PowerUp

#Klasa odpowiada za efekty wizualne wybuchow
class Explosion:
    def __init__(self, x, y, typ="maly"):
        self.x = x
        self.y = y
        self.typ = typ
        self.aktywny = True
        
        #Pusty hitbox, ¿eby gra nie wywala³a b³êdu przy szukaniu pustego miejsca na powerupy na mapie
        self.hitbox = pygame.Rect(self.x, self.y, 0, 0)
        
        self.czas_powstania = pygame.time.get_ticks()
        self.klatka = 0
        self.czas_klatki = 60  
        
        self.obrazki = []
        
        #Ladowanie klatek animacji
        # Wybór odpowiednich wspó³rzêdnych z arkusza w zale¿noœci od typu (rozmiaru) wybuchu
        if self.typ == "maly":
            koordynaty = [(256, 128), (272, 128), (288, 128)]
            rozmiar = 16
            rozmiar_docelowy = (ROZMIAR_KAFELKA, ROZMIAR_KAFELKA) 
            self.x -= 12
            self.y -= 12
            
        elif self.typ == "duzy":
            koordynaty = [(304, 128), (336, 128)]
            rozmiar = 32
            rozmiar_docelowy = (ROZMIAR_KAFELKA * 2, ROZMIAR_KAFELKA * 2) 
            self.x -= 16
            self.y -= 16

        #Petla pobierajaca klatki wybuchu i dodajaca je do tablicy obrazkow
        for cx, cy in koordynaty:
            img = arkusz_grafik.pobierz_obrazek(
                x=cx, y=cy, szerokosc=rozmiar, wysokosc=rozmiar, rozmiar_docelowy=rozmiar_docelowy
            )
            self.obrazki.append(img)
            
        # Aktualizacja pozycji pustego hitboxa za grafik¹
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    #Obsluga animacji
    #Funkcja zmienia klatki wybuchu co okreslony czas, po ostatniej klatce obiekt znika z mapy
    def update(self):
        obecny_czas = pygame.time.get_ticks()
        if obecny_czas - self.czas_powstania > self.czas_klatki:
            self.czas_powstania = obecny_czas
            self.klatka += 1
            if self.klatka >= len(self.obrazki):
                self.aktywny = False

    def draw(self, okno):
        if self.aktywny and self.klatka < len(self.obrazki):
            okno.blit(self.obrazki[self.klatka], (self.x, self.y))

#Zewnetrzny system kolizjii
#Funkcja sprawdzajaca kolizje           
def sprawdz_wszystkie_kolizje(gra):
    obecny_czas = pygame.time.get_ticks()

    #tworzenie listy aktywnych pociskow 
    pociski = [obj for obj in gra.obiekty_w_grze if hasattr(obj, 'kierunek') and hasattr(obj, 'wlasciciel') and obj.aktywny]
    
    #1.Zderzenia pocisków miêdzy sob¹
    for i in range(len(pociski)):
        for j in range(i + 1, len(pociski)):
            p1 = pociski[i]
            p2 = pociski[j]
            if p1.hitbox.colliderect(p2.hitbox) and p1.aktywny and p2.aktywny:
                if p1.wlasciciel != p2.wlasciciel:
                    p1.aktywny = False
                    p2.aktywny = False
                    gra.obiekty_w_grze.append(Explosion(p1.x, p1.y, "maly"))

    #2.Zderzenia pocisków z map¹ i czo³gami
    for pocisk in pociski:
        if not pocisk.aktywny: 
            continue

        # Poza map¹ -> MA£Y WYBUCH
        if not (0 <= pocisk.x <= 800 and 0 <= pocisk.y <= 600):
            pocisk.aktywny = False
            gra.audio.play_sound('obramowanie')
            gra.obiekty_w_grze.append(Explosion(pocisk.x, pocisk.y, "maly"))
            continue 

        # Kolizja z baz¹ -> DU¯Y WYBUCH (GAME OVER koniec gry)
        if pocisk.hitbox.colliderect(gra.baza.hitbox) and not getattr(gra.baza, 'zniszczona', False):
            pocisk.aktywny = False
            gra.baza.zniszczona = True
            if hasattr(gra.baza, 'hp'): gra.baza.hp = 0
            if hasattr(gra.baza, 'aktualizuj_grafike'): gra.baza.aktualizuj_grafike()
            
            gra.kurtyna_aktywna = True
            gra.stan_konca_gry = "PRZEGRANA"
            gra.audio.play_sound('wybuch') 
            gra.obiekty_w_grze.append(Explosion(gra.baza.x, gra.baza.y, "duzy"))
            continue

        #Kolizja ze œcianami
        kolizja_ze_sciana = False
        for sciana in gra.sciany:
            if pocisk.hitbox.colliderect(sciana.hitbox) and sciana.blokuje_pociski:
                pocisk.aktywny = False
                kolizja_ze_sciana = True
                if getattr(sciana, 'zniszczalny', False):
                    if sciana in gra.obiekty_w_grze: gra.obiekty_w_grze.remove(sciana)
                    if sciana in gra.sciany: gra.sciany.remove(sciana)
                    gra.audio.play_sound('wybuch')
                    
                    #Niszczenie ceg³y wygeneruje teraz MA£Y wybuch
                    gra.obiekty_w_grze.append(Explosion(sciana.x, sciana.y, "maly"))
                else:
                    gra.audio.play_sound('metal')
                    gra.obiekty_w_grze.append(Explosion(pocisk.x, pocisk.y, "maly"))
                break 
        if kolizja_ze_sciana:
            continue

        #Trafienie gracza przez wrogi pocisk
        if pocisk.wlasciciel == "wrog" and pocisk.hitbox.colliderect(gra.gracz.hitbox):
            pocisk.aktywny = False
            if not getattr(gra.gracz, 'tarcza_aktywna', False):
                gra.gracz.liczba_zyc -= 1
                if gra.gracz.liczba_zyc <= 0: 
                    gra.kurtyna_aktywna = True
                    gra.stan_konca_gry = "PRZEGRANA"
                gra.audio.play_sound('wybuch') 

                #Gracz obrywa i traci zycie -> DUZY WYBUCH
                gra.obiekty_w_grze.append(Explosion(gra.gracz.x, gra.gracz.y, "duzy"))
            else:
                #Aktywna tarcza gracz nie traci zycia
                gra.obiekty_w_grze.append(Explosion(pocisk.x, pocisk.y, "maly"))
            continue

        #Trafienie wroga przez pocisk gracza
        if pocisk.wlasciciel == "gracz":
            for wrog in gra.przeciwnicy:
                if pocisk.hitbox.colliderect(wrog.hitbox):
                    pocisk.aktywny = False
                    wrog.otrzymaj_obrazenia(gra)
                    #Jesli wrog przezyl(ArmoredTank) MALY WYBYCH
                    if wrog.hp > 0:  
                        gra.obiekty_w_grze.append(Explosion(pocisk.x, pocisk.y, "maly"))
                    break

    #3.Zbieranie PowerUpów
    for p_up in gra.obiekty_w_grze:
        #Usuniecie powerupa po czasie 
        if isinstance(p_up, PowerUp) and p_up.aktywny:
            if hasattr(p_up, 'czas_wygasniecia') and obecny_czas > p_up.czas_wygasniecia:
                p_up.aktywny = False
                continue 
            
            #Zebranie powerupa przez gracza
            if gra.gracz.hitbox.colliderect(p_up.hitbox):
                p_up.aktywny = False
                p_up.zastosuj(gra)

            #Przez wroga
            if p_up.aktywny:
                for wrog in gra.przeciwnicy:
                    if wrog.hitbox.colliderect(p_up.hitbox):
                        p_up.aktywny = False 
                        p_up.zastosuj_dla_wroga(wrog, gra)
                        break














