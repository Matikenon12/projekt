from constants import BIALY, POCISK_PREDKOSC
from entities.game_object import GameObject
import pygame

#Klasa Bullet reprezentujaca wyz=strzelony pocisk, odpowiada za ruch pocisku oraz logike trafienia
class Bullet(GameObject):
    def __init__(self, x, y, kierunek, wlasciciel):
        super().__init__(x, y)
        self.kierunek = kierunek
        self.wlasciciel = wlasciciel        #Informacja czy strzelil wrog cz gracz (zapobiega friendly-fire)
        self.predkosc = POCISK_PREDKOSC

        #Hitbox 8x8px wykrywa kolizje z przeszkodami lub innymi czolgami
        self.hitbox = pygame.Rect(self.x, self.y, 8, 8)
        self.aktywny = True     #Sluzy do usuwania pocisku gdy w cos uderzy

    #Logika ruchu
    #Aktualizacja pozycji na podstawie kierunku pomnozona przez predkosc
    def update(self):
        self.x += self.kierunek[0] * self.predkosc
        self.y += self.kierunek[1] * self.predkosc

        self.hitbox.x = self.x
        self.hitbox.y = self.y

    #Renderowanie pocisku na ekranie
    def draw(self, okno):
        if self.aktywny:
            pygame.draw.rect(okno, BIALY, self.hitbox)




