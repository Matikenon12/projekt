import pygame
from constants import KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA
from entities.tank import Tank
from entities.bullet import Bullet

class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, kierunek=KIERUNEK_GORA, predkosc=2, cooldown_strzalu=500, poziom=1, liczba_zyc=3)
        self.hitbox = pygame.Rect(self.x + 2, self.y + 2, ROZMIAR_KAFELKA - 4, ROZMIAR_KAFELKA - 4)
        self.ostatni_strzal = 0
        
        self.tarcza_aktywna = False
        self.koniec_tarczy = 0
        self.koniec_rapid_fire = 0

    def update(self, sciany=None):
        obecny_czas = pygame.time.get_ticks()
        
        if self.tarcza_aktywna and obecny_czas > self.koniec_tarczy:
            self.tarcza_aktywna = False

        if obecny_czas > self.koniec_rapid_fire and getattr(self, 'koniec_rapid_fire', 0) != 0:
            self.cooldown_strzalu = 500
            self.koniec_rapid_fire = 0

        stary_x = self.x
        stary_y = self.y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.predkosc
            self.kierunek = KIERUNEK_GORA
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.predkosc
            self.kierunek = KIERUNEK_DOL
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.predkosc
            self.kierunek = KIERUNEK_LEWO
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.predkosc
            self.kierunek = KIERUNEK_PRAWO

        self.hitbox.x = self.x + 2
        self.hitbox.y = self.y + 2

        kolizja = False
        if sciany:
            for s in sciany:
                if self.hitbox.colliderect(s.hitbox):
                    kolizja = True
                    break

        if kolizja or self.x < 0 or self.x > 800 - ROZMIAR_KAFELKA or self.y < 0 or self.y > 600 - ROZMIAR_KAFELKA:
            self.x = stary_x
            self.y = stary_y
            self.hitbox.x = self.x + 2
            self.hitbox.y = self.y + 2

    def strzelaj(self):
        obecny_czas = pygame.time.get_ticks()
        if obecny_czas - self.ostatni_strzal >= self.cooldown_strzalu:
            self.ostatni_strzal = obecny_czas
            start_x = self.x + 12
            start_y = self.y + 12
            return Bullet(start_x, start_y, self.kierunek, "gracz")
        return None

    def draw(self, okno):
        # Rysujemy ¿ó³ty czo³g
        pygame.draw.rect(okno, (255, 255, 0), self.hitbox)
        
        # Ochronna ramka tarczy, jeœli jest aktywna
        if self.tarcza_aktywna:
            pygame.draw.rect(okno, (255, 255, 255), self.hitbox, 4)