from AI.enemyai import wybierz_kierunek_ai
import pygame
import random
from entities.tank import Tank
from entities.bullet import Bullet
from entities.powerups import PowerUp
from constants import KIERUNEK_DOL, KIERUNEK_GORA, KIERUNEK_LEWO, KIERUNEK_PRAWO, ROZMIAR_KAFELKA
from map.spritesheet import arkusz_grafik # DODANY IMPORT ARKUSZA
from utils.collision import sprawdz_wszystkie_kolizje

class EnemyTank(Tank):
    def __init__(self, x, y, hp=1, predkosc=2, cooldown_strzalu=1500, kolor=(255, 0, 0)):
        super().__init__(x, y, hp=hp, kierunek=KIERUNEK_DOL, predkosc=predkosc, cooldown_strzalu=cooldown_strzalu, poziom=1, liczba_zyc=1)

        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        self.ostatni_ruch = pygame.time.get_ticks()
        self.ostatni_strzal = pygame.time.get_ticks()
        self.kolor = kolor
        
        self.czy_stoi = False
        self.koniec_postoju = 0
        self.cel_na_muszce = False
        
        # Domyœlne grafiki (nadpisywane przez konkretne typy czo³gów poni¿ej)
        self.sprite_y = 0 
        self.kierunki_x = {
            KIERUNEK_GORA: 0,
            KIERUNEK_LEWO: 32,
            KIERUNEK_DOL: 64,
            KIERUNEK_PRAWO: 96
        }
        self.image = None


    def otrzymaj_obrazenia(self, gra):
        from utils.collision import Explosion 
        from entities.powerups import PowerUp
        import random
        import pygame
        
        self.hp -= 1
        if self.hp <= 0:
            gra.obiekty_w_grze.append(Explosion(self.x, self.y, "duzy"))
            gra.audio.play_sound('zabicie')
            
            nazwa_typu = self.__class__.__name__
            if nazwa_typu in gra.zabite_czolgi: 
                gra.zabite_czolgi[nazwa_typu] += 1
            else: 
                gra.zabite_czolgi[nazwa_typu] = 1
            
            gra.przeciwnicy.remove(self)
            gra.obiekty_w_grze.remove(self)
            gra.wynik += 100
            
            if random.randint(1, 100) > 50:
                nowy_bonus = PowerUp(self.x, self.y)
                nowy_bonus.czas_wygasniecia = pygame.time.get_ticks() + 10000
                gra.obiekty_w_grze.append(nowy_bonus)


    def aktualizuj_grafike(self):
        # Pobieranie grafiki na podstawie ustawieñ klasy potomnej
        if hasattr(self, 'kierunki_x') and hasattr(self, 'sprite_y'):
            pozycja_x = self.kierunki_x.get(self.kierunek, 0)
            self.image = arkusz_grafik.pobierz_obrazek(
                x=pozycja_x,
                y=self.sprite_y,
                szerokosc=16,
                wysokosc=16,
                rozmiar_docelowy=(ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
            )

    def strzelaj(self):
        obecny_czas = pygame.time.get_ticks()
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
        stary_kierunek = self.kierunek
        obecny_czas = pygame.time.get_ticks()

        # SKANOWANIE CELU
        self.cel_na_muszce = False
        if gracz:
            if abs(self.x - gracz.x) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_DOL and gracz.y > self.y) or (self.kierunek == KIERUNEK_GORA and gracz.y < self.y)):
                self.cel_na_muszce = True
            if abs(self.y - gracz.y) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_PRAWO and gracz.x > self.x) or (self.kierunek == KIERUNEK_LEWO and gracz.x < self.x)):
                self.cel_na_muszce = True
                
        if baza:
            if abs(self.x - baza.x) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_DOL and baza.y > self.y) or (self.kierunek == KIERUNEK_GORA and baza.y < self.y)):
                self.cel_na_muszce = True
            if abs(self.y - baza.y) < ROZMIAR_KAFELKA and ((self.kierunek == KIERUNEK_PRAWO and baza.x > self.x) or (self.kierunek == KIERUNEK_LEWO and baza.x < self.x)):
                self.cel_na_muszce = True

        if obecny_czas - self.ostatni_ruch > 1500:
            self.ostatni_ruch = obecny_czas
            
            if random.randint(1, 100) > 75:
                self.czy_stoi = True
                self.koniec_postoju = obecny_czas + 1000 
            else:
                self.czy_stoi = False
            
            if baza and gracz and random.randint(1, 100) > 20:
                self.kierunek = wybierz_kierunek_ai(self.x, self.y, baza.x, baza.y, gracz.x, gracz.y)
            else:
                self.kierunek = random.choice([KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO])

        # --- AUTO-WYRÓWNANIE AI I AKTUALIZACJA GRAFIKI ---
        if self.kierunek != stary_kierunek:
            if stary_kierunek in [KIERUNEK_GORA, KIERUNEK_DOL] and self.kierunek in [KIERUNEK_LEWO, KIERUNEK_PRAWO]:
                reszta = self.y % 16
                if reszta <= 8: self.y -= reszta
                else: self.y += (16 - reszta)
            elif stary_kierunek in [KIERUNEK_LEWO, KIERUNEK_PRAWO] and self.kierunek in [KIERUNEK_GORA, KIERUNEK_DOL]:
                reszta = self.x % 16
                if reszta <= 8: self.x -= reszta
                else: self.x += (16 - reszta)
                
            # Kierunek siê zmieni³, odœwie¿amy obrazek
            self.aktualizuj_grafike()

        if not self.czy_stoi or obecny_czas > self.koniec_postoju:
            self.x += self.kierunek[0] * self.predkosc
            self.y += self.kierunek[1] * self.predkosc

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
            self.hitbox.x = self.x
            self.hitbox.y = self.y
            
            self.kierunek = random.choice([KIERUNEK_GORA, KIERUNEK_DOL, KIERUNEK_LEWO, KIERUNEK_PRAWO])
            self.aktualizuj_grafike() # Odœwie¿amy obrazek po uderzeniu w œcianê (nowy losowy kierunek)

    def draw(self, okno):
        if hasattr(self, 'image') and self.image:
            okno.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(okno, self.kolor, self.hitbox)


# ---------------------------------------------------------
# KLASY POTOMNE - TUTAJ WPISZ W£ASNE WSPÓ£RZÊDNE Z ARKUSZA
# ---------------------------------------------------------

class BasicTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=2, cooldown_strzalu=1500, kolor=(200, 0, 0))
        # Wpisz w³asne Y
        self.sprite_y = 0 
        # Wpisz w³asne X dla ka¿dego kierunku
        self.kierunki_x = {
            KIERUNEK_GORA: 128,
            KIERUNEK_LEWO: 160,
            KIERUNEK_DOL: 192,
            KIERUNEK_PRAWO: 224
        }
        self.aktualizuj_grafike()

class FastTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=3, cooldown_strzalu=1500, kolor=(255, 105, 180))
        # Wpisz w³asne Y
        self.sprite_y = 16
        # Wpisz w³asne X dla ka¿dego kierunku
        self.kierunki_x = {
            KIERUNEK_GORA: 128,
            KIERUNEK_LEWO: 160,
            KIERUNEK_DOL: 192,
            KIERUNEK_PRAWO: 224
        }
        self.aktualizuj_grafike()

class ArmoredTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=3, predkosc=1, cooldown_strzalu=2000, kolor=(100, 0, 0))
        # Wpisz w³asne Y
        self.sprite_y = 32
        # Wpisz w³asne X dla ka¿dego kierunku
        self.kierunki_x = {
            KIERUNEK_GORA: 128,
            KIERUNEK_LEWO: 160,
            KIERUNEK_DOL: 192,
            KIERUNEK_PRAWO: 224
        }
        self.aktualizuj_grafike()

class ShooterTank(EnemyTank):
    def __init__(self, x, y):
        super().__init__(x, y, hp=1, predkosc=2, cooldown_strzalu=500, kolor=(255, 140, 0))
        # Wpisz w³asne Y
        self.sprite_y = 48 
        # Wpisz w³asne X dla ka¿dego kierunku
        self.kierunki_x = {
            KIERUNEK_GORA: 128,
            KIERUNEK_LEWO: 160,
            KIERUNEK_DOL: 192,
            KIERUNEK_PRAWO: 224
        }
        self.aktualizuj_grafike()