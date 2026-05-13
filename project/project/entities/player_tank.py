import pygame
from entities.bullet import Bullet
from entities.tank import Tank
from constants import GRACZ_COOLDOWN_STRZALU, GRACZ_POCZATKOWE_ZYCIA, GRACZ_PREDKOSC, KIERUNEK_DOL,KIERUNEK_GORA, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA, ZIELONY  

class PlayerTank(Tank):
    def __init__(self,x,y):
        super().__init__(x,y,hp=1,predkosc=GRACZ_PREDKOSC,kierunek=KIERUNEK_GORA,cooldown_strzalu=GRACZ_COOLDOWN_STRZALU,poziom=1,liczba_zyc=GRACZ_POCZATKOWE_ZYCIA)

        self.hitbox=pygame.Rect(self.x+2,self.y+2,ROZMIAR_KAFELKA-4,ROZMIAR_KAFELKA-4)
        self.ostatni_strzal=0

    def update(self,sciany):
        if sciany is None:
            sciany=[]

        stary_x=self.x
        stary_y=self.y

        keys=pygame.key.get_pressed()
        

        if keys[pygame.K_UP] or keys[pygame.K_w]:       #ruch gora (W)
            self.y-=self.predkosc
            self.kierunek=KIERUNEK_GORA
           

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:   #ruch dol (S)
            self.y+=self.predkosc
            self.kierunek=KIERUNEK_DOL
           
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:   #ruch gora (A)
            self.x-=self.predkosc
            self.kierunek=KIERUNEK_LEWO
           
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  #ruch gora (D)
            self.x+=self.predkosc
            self.kierunek=KIERUNEK_PRAWO
            
        self.hitbox.x=self.x+2
        self.hitbox.y=self.y+2

        for sciana in sciany:
            if self.hitbox.colliderect(sciana.hitbox):
                self.x=stary_x
                self.y=stary_y
                self.hitbox.x=self.x+2
                self.hitbox.y=self.y+2



    def draw(self,okno):
        pygame.draw.rect(okno,ZIELONY,self.hitbox)

    def strzelaj(self):
        obecny_czas=pygame.time.get_ticks()

        if obecny_czas-self.ostatni_strzal >=self.cooldown_strzalu:
            self.ostatni_strzal=obecny_czas

            start_x=self.x+12
            start_y=self.y+12

            return Bullet(start_x,start_y,self.kierunek,"gracz")
        return None



