import pygame
import os

#Klasa zarzadzajaca glownym arkuszem tekstur w grze, umozliwia wczytanie oraz wycinanie grafik
class SpriteSheet:
    def __init__(self, pelna_sciezka):
        self.pelna_sciezka = pelna_sciezka
        self.arkusz = None

    #Pobieranie obrazka
    #Funkcja pobiera arkusz do pamieci 
    def pobierz_obrazek(self, x, y, szerokosc, wysokosc, rozmiar_docelowy=None):
        if self.arkusz is None:
            if os.path.exists(self.pelna_sciezka):
                #Zaladowanie obrazu z zachowaniem kanalu alpha (przezroczystości) dla optymalizacji renderowania
                #
                self.arkusz = pygame.image.load(self.pelna_sciezka).convert_alpha()
            else:
                print(f"BLAD: Plik fizycznie nie istnieje pod sciezka: {self.pelna_sciezka}")
                self.arkusz = False

        #Zabezpieczenie przed proba operacji na nieistniejacym arkuszu
        if not self.arkusz:
            return None
            
        #Wycinanie sprite
        #Tworzenie czystej powierzchni o wymiarach pojedynczego kafelka
        obrazek = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
        #Kopiowanie i wycinanie konkretnego fragmentu z arkusza 
        obrazek.blit(self.arkusz, (0, 0), (x, y, szerokosc, wysokosc))
        
        #Skalowanie wycietej tekstury do zadanych wymiarow 
        if rozmiar_docelowy:
            obrazek = pygame.transform.scale(obrazek, (rozmiar_docelowy[0], rozmiar_docelowy[1]))
            
        return obrazek

#Singleton
#Utworzenie globalnej instancji dla calego projektu zeby arkusz byl wczytywany tylko raz
arkusz_grafik=SpriteSheet('sprites.png')









