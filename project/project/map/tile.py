from constants import CIEMNO_ZIELONY, NIEBIESKI, POMARANCZOWY, ROZMIAR_KAFELKA, SZARY
from entities.game_object import GameObject
import pygame

class Tile(GameObject):
    def __init__(self, x, y, kolor, szerokosc=ROZMIAR_KAFELKA, wysokosc=ROZMIAR_KAFELKA):
        super().__init__(x, y)
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        self.kolor = kolor

        self.zniszczalny = False
        self.blokuje_czolgi = True
        self.blokuje_pociski = True

    def update(self):
        pass

    def draw(self, okno):
        pygame.draw.rect(okno, self.kolor, self.hitbox)

class BrickWall(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, POMARANCZOWY)
        self.zniszczalny = True
        
        # Ceg³y s¹ o po³owê mniejsze
        rozmiar = ROZMIAR_KAFELKA // 2
        self.hitbox = pygame.Rect(self.x, self.y, rozmiar, rozmiar)

class SteelWall(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, SZARY)
        
class Water(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, NIEBIESKI)
        self.blokuje_pociski = False

class Bush(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, CIEMNO_ZIELONY)
        self.blokuje_czolgi = False
        self.blokuje_pociski = False

class Ice(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, (173, 216, 230))
        self.blokuje_czolgi = False
        self.blokuje_pociski = False