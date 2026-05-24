from constants import BIALY, POCISK_PREDKOSC
from entities.game_object import GameObject
import pygame

class Bullet(GameObject):
    def __init__(self, x, y, kierunek, wlasciciel):
        super().__init__(x, y)
        self.kierunek = kierunek
        self.wlasciciel = wlasciciel
        self.predkosc = POCISK_PREDKOSC

        self.hitbox = pygame.Rect(self.x, self.y, 8, 8)
        self.aktywny = True

    def update(self):
        self.x += self.kierunek[0] * self.predkosc
        self.y += self.kierunek[1] * self.predkosc

        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def draw(self, okno):
        if self.aktywny:
            pygame.draw.rect(okno, BIALY, self.hitbox)