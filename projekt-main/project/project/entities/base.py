import pygame
from entities.game_object import GameObject
from constants import ROZMIAR_KAFELKA
from map.spritesheet import arkusz_grafik

class Base(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Hitbox bazy na pe³ny kafelek 32x32
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        self.hp = 1
        self.image = None

        # ---------------------------------------------------------
        # WSPÓ£RZÊDNE BAZY Z ARKUSZA (X, Y)
        # ---------------------------------------------------------
        self.sprite_x_zywa = 304       # Klasyczny ¿ywy orze³ek
        self.sprite_y_zywa = 32
        
        self.sprite_x_zniszczona = 320 # Klasyczny zniszczony orze³ek
        self.sprite_y_zniszczona = 32

        self.aktualizuj_grafike()

    def aktualizuj_grafike(self):
        # Wybieramy odpowiednie koordynaty w zale¿noœci od tego, czy baza ¿yje
        if self.hp > 0:
            spr_x = self.sprite_x_zywa
            spr_y = self.sprite_y_zywa
        else:
            spr_x = self.sprite_x_zniszczona
            spr_y = self.sprite_y_zniszczona

        self.image = arkusz_grafik.pobierz_obrazek(
            x=spr_x,
            y=spr_y,
            szerokosc=16,
            wysokosc=16,
            rozmiar_docelowy=(ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        )

    def update(self):
        pass

    def draw(self, okno):
        if hasattr(self, 'image') and self.image:
            okno.blit(self.image, (self.x, self.y))
        else:
            # Awaryjny kolor, gdyby grafika nie by³a za³adowana
            kolor = (0, 255, 0) if self.hp > 0 else (255, 0, 0)
            pygame.draw.rect(okno, kolor, self.hitbox)







