from constants import CIEMNO_ZIELONY, NIEBIESKI, POMARANCZOWY, ROZMIAR_KAFELKA, SZARY
from entities.game_object import GameObject
import pygame
from map.spritesheet import arkusz_grafik

#Klasa bazowa dla wszystkich elementow na mapie, definiuje podstawowe wlasciwosci oraz parametry np. (hitbox,grafika)
class Tile(GameObject):
    def __init__(self, x, y, kolor, szerokosc=ROZMIAR_KAFELKA, wysokosc=ROZMIAR_KAFELKA):
        super().__init__(x, y)
        
        self.hitbox = pygame.Rect(self.x, self.y, szerokosc, wysokosc) 
        self.kolor = kolor

        self.zniszczalny = False
        self.blokuje_czolgi = True
        self.blokuje_pociski = True
        self.image = None
        self.rect = None

    def update(self):
        pass

    #Renderowanie tekstur kafelkow
    def draw(self, okno):
        if self.image:
            okno.blit(self.image, self.rect)

#Klasa BrickWall zniszczalny kafelek podzielony na 4 mniejsze kafelki
class BrickWall(Tile):
    def __init__(self, start_x, start_y):
        #Inicjalizacja rozmiaru ma³ej ceg³y (16x16)
        super().__init__(start_x, start_y, POMARANCZOWY, szerokosc=16, wysokosc=16)
        
        self.zniszczalny = True 
        
        #Pobieranie i skalowanie tekstury
        self.image = arkusz_grafik.pobierz_obrazek(
            x=256, 
            y=0, 
            szerokosc=16, 
            wysokosc=16,
            rozmiar_docelowy=(16, 16) 
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

#Klasa SteelWall niezniszczalna kafelek 32x32
class SteelWall(Tile):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, SZARY)
        self.image = arkusz_grafik.pobierz_obrazek(
            x=256, 
            y=16, 
            szerokosc=16, 
            wysokosc=16, 
            rozmiar_docelowy=(32, 32)
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

#Klasa Water nieprzejezdna wymusza zmiane kierunku czolgu, przepuszcza pociski
class Water(Tile):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, NIEBIESKI)
        self.image = arkusz_grafik.pobierz_obrazek(
            x=256, 
            y=48, 
            szerokosc=16, 
            wysokosc=16, 
            rozmiar_docelowy=(32, 32)
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.blokuje_pociski = False

#Klasa Bush pelni funkcje wizualnego kamuflazu pozwala na przenikanie pociskow jak i czolgow
class Bush(Tile):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, CIEMNO_ZIELONY)
        self.image = arkusz_grafik.pobierz_obrazek(
            x=272, 
            y=32, 
            szerokosc=16, 
            wysokosc=16, 
            rozmiar_docelowy=(32, 32)
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.blokuje_czolgi = False
        self.blokuje_pociski = False

#Klasa Ice nie blokuje jednostek, przepuszcza pociski
class Ice(Tile):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, (173, 216, 230))
        self.image = arkusz_grafik.pobierz_obrazek(
            x=288, 
            y=32, 
            szerokosc=16, 
            wysokosc=16, 
            rozmiar_docelowy=(32, 32)
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.blokuje_czolgi = False
        self.blokuje_pociski = False










