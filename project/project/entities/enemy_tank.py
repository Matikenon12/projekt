import pygame
import random
from entities.tank import Tank
from entities.bullet import Bullet
from constants import CZERWONY, KIERUNEK_DOL, KIERUNEK_GORA, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA  

class EnemyTank(Tank):
    def __init__(self,x,y,hp=1,predkosc=2):

        startowy_kierunek=random.choice([KIERUNEK_GORA,KIERUNEK_DOL,KIERUNEK_LEWO,KIERUNEK_PRAWO])

        super().__init__(x,y,hp=hp,kierunek=startowy_kierunek,predkosc=predkosc,cooldown_strzalu=1500,poziom=1,liczba_zyc=1)

        self.hitbox=pygame.Rect(self.x+2,self.y+2,ROZMIAR_KAFELKA-4,ROZMIAR_KAFELKA-4)
        self.ostatni_ruch=pygame.time.get_ticks()
        self.ostatni_strzal=pygame.time.get_ticks()

    def strzelaj(self):
        obecny_czas=pygame.time.get_ticks()
        
        if obecny_czas-self.ostatni_strzal>=self.cooldown_strzalu and random.randint(1,100)>95:
            self.ostatni_strzal=obecny_czas
            start_x=self.x+12
            start_y=self.y+12
            return Bullet(start_x,start_y,self.kierunek,"wrog")
        return None

    def update(self,sciany=None):
        stary_x=self.x 
        stary_y=self.y

        obecny_czas=pygame.time.get_ticks()
        if obecny_czas-self.ostatni_ruch>2000:
            self.ostatni_ruch=obecny_czas

            if random.randint(1,100)>50:
                self.kierunek=random.choice([KIERUNEK_GORA,KIERUNEK_DOL,KIERUNEK_LEWO,KIERUNEK_PRAWO])
               

        self.x+=self.kierunek[0]*self.predkosc
        self.y+=self.kierunek[1]*self.predkosc

        self.hitbox.x=self.x+2
        self.hitbox.y=self.y+2

        kolizja=False

        if sciany:
            for s in sciany:
                if self.hitbox.colliderect(s.hitbox):
                    kolizja=True
                    break


        if kolizja or self.x<0 or self.x>768 or self.y<0 or self.y>568:
            self.x=stary_x
            self.y=stary_y
            self.hitbox.x=self.x+2
            self.hitbox.y=self.y+2


            self.kierunek=random.choice([KIERUNEK_GORA,KIERUNEK_DOL,KIERUNEK_LEWO,KIERUNEK_PRAWO])
    

    def draw(self,okno):
        pygame.draw.rect(okno,CZERWONY,self.hitbox)


