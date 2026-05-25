import pygame
from constants import KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA
from entities.tank import Tank
from entities.bullet import Bullet
from map.spritesheet import arkusz_grafik

class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, kierunek=KIERUNEK_GORA, predkosc=2, cooldown_strzalu=500, poziom=1, liczba_zyc=3)
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        self.ostatni_strzal = 0
        
        self.bazowa_predkosc = 2
        self.koniec_speed = 0
        self.tarcza_aktywna = False
        self.koniec_tarczy = 0
        self.koniec_rapid_fire = 0

        self.kierunki_x = {
            KIERUNEK_GORA: 0,
            KIERUNEK_LEWO: 32,
            KIERUNEK_DOL: 64,
            KIERUNEK_PRAWO: 96
        }

        self.aktualizuj_grafike()

    def aktualizuj_grafike(self):
        pozycja_x = self.kierunki_x[self.kierunek]
        self.image = arkusz_grafik.pobierz_obrazek(
            x=pozycja_x,
            y=0,
            szerokosc=16,
            wysokosc=16,
            rozmiar_docelowy=(ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        )

    def update(self, sciany=None):
        obecny_czas = pygame.time.get_ticks()
        
        if self.tarcza_aktywna and obecny_czas > self.koniec_tarczy:
            self.tarcza_aktywna = False

        if obecny_czas > self.koniec_rapid_fire and getattr(self, 'koniec_rapid_fire', 0) != 0:
            self.cooldown_strzalu = 500
            self.koniec_rapid_fire = 0

        if self.koniec_speed > 0 and obecny_czas > self.koniec_speed:
            self.predkosc = self.bazowa_predkosc
            self.koniec_speed = 0

        stary_x = self.x
        stary_y = self.y
        stary_kierunek = self.kierunek

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

        # --- AUTO-WYRÓWNANIE (Corner-cutting) ---
        if self.kierunek != stary_kierunek:
            if stary_kierunek in [KIERUNEK_GORA, KIERUNEK_DOL] and self.kierunek in [KIERUNEK_LEWO, KIERUNEK_PRAWO]:
                reszta = self.y % 16
                if reszta <= 8: self.y -= reszta
                else: self.y += (16 - reszta)
            elif stary_kierunek in [KIERUNEK_LEWO, KIERUNEK_PRAWO] and self.kierunek in [KIERUNEK_GORA, KIERUNEK_DOL]:
                reszta = self.x % 16
                if reszta <= 8: self.x -= reszta
                else: self.x += (16 - reszta)
            
            self.aktualizuj_grafike()

        self.hitbox.x = self.x
        self.hitbox.y = self.y

        kolizja = False
        if sciany:
            for s in sciany:
                if self.hitbox.colliderect(s.hitbox):
                    kolizja = True
                    break

        if kolizja or self.x < 0 or self.x > 800 - ROZMIAR_KAFELKA or self.y < 0 or self.y > 600 - ROZMIAR_KAFELKA:
            self.x = stary_x
            self.y = stary_y
            
            # Wa¿ne: Jeœli skrêci³ za wczeœnie i uderzy³ w œcianê, wraca do poprzedniego kierunku.
            # Pozwala to "œlizgaæ siê" po œcianie a¿ do momentu, w którym otwór bêdzie dostêpny.
            if self.kierunek != stary_kierunek:
                self.kierunek = stary_kierunek
                self.aktualizuj_grafike()
                
            self.hitbox.x = self.x
            self.hitbox.y = self.y

    def strzelaj(self):
        obecny_czas = pygame.time.get_ticks()
        if obecny_czas - self.ostatni_strzal >= self.cooldown_strzalu:
            self.ostatni_strzal = obecny_czas
            start_x = self.x + 12
            start_y = self.y + 12
            return Bullet(start_x, start_y, self.kierunek, "gracz")
        return None

    def draw(self, okno):
        if hasattr(self, 'image') and self.image:
            okno.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(okno, (255, 255, 0), self.hitbox)

        if self.tarcza_aktywna:
            pygame.draw.rect(okno, (255, 255, 255), self.hitbox, 4)


