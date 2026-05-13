from AI.enemyai import wybierz_kierunek_ai
import pygame
import random
from entities.tank import Tank
from entities.bullet import Bullet
from constants import KIERUNEK_DOL, KIERUNEK_GORA, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA

class EnemyTank(Tank):
    def __init__(self, x, y, hp=1, predkosc=2, cooldown_strzalu=1500, kolor=(255, 0, 0)):
        super().__init__(x, y, hp=hp, kierunek=KIERUNEK_DOL, predkosc=predkosc, cooldown_strzalu=cooldown_strzalu, poziom=1, liczba_zyc=1)

        self.hitbox = pygame.Rect(self.x + 2, self.y + 2, ROZMIAR_KAFELKA - 4, ROZMIAR_KAFELKA - 4)
        self.ostatni_ruch = pygame.time.get_ticks()
        self.ostatni_strzal = pygame.time.get_ticks()
        self.kolor = kolor
        
        # --- NOWE FUNKCJE AI ---
        self.czy_stoi = False
        self.koniec_postoju = 0
        self.cel_na_muszce = False

    def strzelaj(self):
        obecny_czas = pygame.time.get_ticks()
        
        # Jeœli widzi gracza lub bazê przed luf¹, strzela jak szalony! W przeciwnym razie oszczêdza pociski.
        szansa_strzalu = 20 if self.cel_na_muszce else 98
        
        if obecny_czas - self.ostatni_strzal >= self.cooldown_strzalu and random.randint(1, 100) > szansa_strzalu:
            self.ostatni_strzal = obecny_czas
            start_x = self.x + 12
            start_y = self.y + 12
            return Bullet(start_x, start_y, self.kierunek, "wrog")
        return None

    def update(self, sciany=None, baza=None, gracz=None):
        stary_x = self.x 
        stary_y = self.y
        obecny_czas = pygame.time.get_ticks()

        # --- SKANOWANIE CELU (WIZJER CZO£GU) ---
        self.cel_na_muszce = False
        if gracz:
            # Gracz w tej samej kolumnie, czo³g patrzy w dó³/górê
            if abs(self.x - gracz.x) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_DOL and gracz.y > self.y) or (self.kierunek == KIERUNEK_GORA and gracz.y < self.y)):
                self.cel_na_muszce = True
            # Gracz w tym samym rzêdzie, czo³g patrzy w lewo/prawo
            if abs(self.y - gracz.y) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_PRAWO and gracz.x > self.x) or (self.kierunek == KIERUNEK_LEWO and gracz.x < self.x)):
                self.cel_na_muszce = True
                
        if baza:
            if abs(self.x - baza.x) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_DOL and baza.y > self.y) or (self.kierunek == KIERUNEK_GORA and baza.y < self.y)):
                self.cel_na_muszce = True
            if abs(self.y - baza.y) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_PRAWO and baza.x > self.x) or (self.kierunek == KIERUNEK_LEWO and baza.x < self.x)):
                self.cel_na_muszce = True
        # --------------------------------------

        # Zmiana decyzji co 1.5 sekundy
        if obecny_czas - self.ostatni_ruch > 1500:
            self.ostatni_ruch = obecny_czas
            
            # Wróg ma 25% szans, ¿eby siê na chwilê zatrzymaæ
            if random.randint(1, 100) > 75:
                self.czy_stoi = True
                self.koniec_postoju = obecny_czas + 1000 # stój przez 1 sekundê
            else:
                self.czy_stoi = False
            
            # Zmiana kierunku
            if baza and gracz and random.randint(1, 100) > 20:
                self.kierunek = wybierz_kierunek_ai(self.x, self.y, baza.x, baza.y, gracz.x, gracz.y)
            else:
                self.kierunek = random.choice([KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO])

        # Ruch fizyczny odbywa siê tylko wtedy, gdy czo³g "nie stoi"
        if not self.czy_stoi or obecny_czas > self.koniec_postoju:
            self.x += self.kierunek[0] * self.predkosc
            self.y += self.kierunek[1] * self.predkosc

        self.hitbox.x = self.x + 2
        self.hitbox.y = self.y + 2

        kolizja = False
        if sciany:
            for s in sciany:
                if self.hitbox.colliderect(s.hitbox):
                    kolizja = True
                    break

        if kolizja or self.x < 0 or self.x > 768 or self.y > 568 or self.y < -32:
            self.x = stary_x
            self.y = stary_y
            self.hitbox.x = self.x + 2
            self.hitbox.y = self.y + 2
            self.kierunek = random.choice([KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO])

    def draw(self, okno):
        pygame.draw.rect(okno, self.kolor, self.hitbox)

class BasicTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=2, cooldown_strzalu=1500, kolor=(200, 0, 0))

class FastTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=3, cooldown_strzalu=1500, kolor=(255, 105, 180))

class ArmoredTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=3, predkosc=1, cooldown_strzalu=2000, kolor=(100, 0, 0))

class ShooterTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=2, cooldown_strzalu=500, kolor=(255, 140, 0))