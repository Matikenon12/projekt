import pygame
import os

class SpriteSheet:
    def __init__(self, pelna_sciezka):
        self.pelna_sciezka = pelna_sciezka
        self.arkusz = None

    def pobierz_obrazek(self, x, y, szerokosc, wysokosc, rozmiar_docelowy=None):
        if self.arkusz is None:
            if os.path.exists(self.pelna_sciezka):
                self.arkusz = pygame.image.load(self.pelna_sciezka).convert_alpha()
            else:
                print(f"BLAD: Plik fizycznie nie istnieje pod sciezka: {self.pelna_sciezka}")
                self.arkusz = False

        if not self.arkusz:
            return None
            
        obrazek = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
        obrazek.blit(self.arkusz, (0, 0), (x, y, szerokosc, wysokosc))
        
        if rozmiar_docelowy:
            obrazek = pygame.transform.scale(obrazek, (rozmiar_docelowy[0], rozmiar_docelowy[1]))
            
        return obrazek

    #singleton
arkusz_grafik=SpriteSheet('sprites.png')