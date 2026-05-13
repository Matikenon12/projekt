import pygame
import random
from entities.game_object import GameObject
from constants import ROZMIAR_KAFELKA

KOLORY_POWERUPOW={
    "Shield":(0,255,255),
    "SpeedBoost":(255,255,0),
    "RapidFire":(255,100,0),
    "ExtraLife":(0,255,255),
    "Bomb":(255,0,0)
    }

class PowerUp(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)

        self.typ=random.choice(["Shield","SpeedBoost","RapidFire","ExtraLife","Bomb"])
        self.kolor=KOLORY_POWERUPOW[self.typ]

        self.czas_powstania=pygame.time.get_ticks()
        self.aktywny=True

    def update(self):
        if pygame.time.get_ticks()-self.czas_powstania>10000:
            self.aktyny=False

    def draw(self,okno):
        if self.aktywny:
            pygame.draw.circle(okno,self.kolor,(self.x+16,self.y+16),10)