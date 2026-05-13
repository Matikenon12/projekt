import pygame
from constants import ROZMIAR_KAFELKA
from entities.game_object import GameObject


class Base(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.hitbox=pygame.Rect(self.x,self.y,ROZMIAR_KAFELKA,ROZMIAR_KAFELKA)
        self.zniszczona=False

    def update(self):
        pass

    def draw(self,okno):
        kolor=(0,0,255) if not self.zniszczona else(50,50,50)
        pygame.draw.rect(okno,kolor,self.hitbox)
