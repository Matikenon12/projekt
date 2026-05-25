import pygame
from entities.game_object import GameObject
from constants import ROZMIAR_KAFELKA, ZIELONY
from map.spritesheet import arkusz_grafik

#Klasa reprezentujaca baze gracza
class Base(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)  #Obszar kolizji bazy (32x32px)
        self.hp = 1
        self.image = None

        #Mapowanie grafik (Wspolrzednie z arkusza spitesheet)
        self.sprite_x_zywa = 304       #zywa baza
        self.sprite_y_zywa = 32
        
        self.sprite_x_zniszczona = 320 #zniszczona baza
        self.sprite_y_zniszczona = 32

        self.aktualizuj_grafike()

    #Metoda wybiera grafike bazy na podstawie jej stanu
    def aktualizuj_grafike(self):
        if self.hp > 0:
            spr_x = self.sprite_x_zywa
            spr_y = self.sprite_y_zywa
        else:
            spr_x = self.sprite_x_zniszczona
            spr_y = self.sprite_y_zniszczona

        #Pobieranie wycinka grafiki z arkusza i skalowanie do rozmiaru kafelka
        self.image = arkusz_grafik.pobierz_obrazek(
            x=spr_x,
            y=spr_y,
            szerokosc=16,
            wysokosc=16,
            rozmiar_docelowy=(ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        )

    #Statyczny obiekt nie wymaga aktualizacji
    def update(self):
        pass

    #Renderowanie grafiki bazy lub rysowanie prostokata
    def draw(self, okno):
        if hasattr(self, 'image') and self.image:
            okno.blit(self.image, (self.x, self.y))
        else:
            #Awaryjny kolor gdyby grafika nie by³a zaladowana
            kolor = ZIELONY if self.hp > 0 else (255, 0, 0)
            pygame.draw.rect(okno, kolor, self.hitbox)







