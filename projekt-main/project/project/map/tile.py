from constants import CIEMNO_ZIELONY, NIEBIESKI, POMARANCZOWY, ROZMIAR_KAFELKA, SZARY
from entities.game_object import GameObject
import pygame
from map.spritesheet import arkusz_grafik

class Tile(GameObject):
    def __init__(self, x, y, kolor, szerokosc=ROZMIAR_KAFELKA, wysokosc=ROZMIAR_KAFELKA):
        super().__init__(x, y)
        # U¿ywamy zmiennych szerokosc i wysokosc, a nie sta³ej 32x32
        self.hitbox = pygame.Rect(self.x, self.y, szerokosc, wysokosc) 
        self.kolor = kolor

        self.zniszczalny = False
        self.blokuje_czolgi = True
        self.blokuje_pociski = True
        self.image = None
        self.rect = None

    def update(self):
        pass

    def draw(self, okno):
        if self.image:
            okno.blit(self.image, self.rect)


class BrickWall(Tile):
    def __init__(self, start_x, start_y):
        # Definiujemy rozmiar ma³ej ceg³y (16x16)
        super().__init__(start_x, start_y, POMARANCZOWY, szerokosc=16, wysokosc=16)
        
        # NAPRAWA 1: Ceg³y s¹ zniszczalne! (Zniknie dŸwiêk rykoszetu o metal)
        self.zniszczalny = True 
        
        self.image = arkusz_grafik.pobierz_obrazek(
            x=256, 
            y=0, 
            szerokosc=16, 
            wysokosc=16, 
            # NAPRAWA 2: Skalujemy do wymiarów 16x16 (wczeœniej by³o 32x32 i psu³o mapê)
            rozmiar_docelowy=(16, 16) 
        )
        self.rect = self.image.get_rect(topleft=(start_x, start_y))

# Poni¿ej zostawiasz swoje SteelWall, Water, Bush, Ice tak jak by³y!
# ... (reszta pliku bez zmian) ...


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










