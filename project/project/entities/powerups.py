import pygame
import random
from entities.game_object import GameObject
from constants import BIALY, JASNY_CZERWONY, ROZMIAR_KAFELKA, ZOLTY
from map.spritesheet import arkusz_grafik
from map.tile import NIEBIESKI, POMARANCZOWY 

# Kolory awaryjne (jeœli obrazek by siê nie wczyta³)
KOLORY_POWERUPOW={
    "Shield": NIEBIESKI,
    "SpeedBoost":ZOLTY,
    "RapidFire": POMARANCZOWY,
    "ExtraLife": BIALY,
    "Bomb": JASNY_CZERWONY
}

#Klasa obslugujaca obiekty powerupow, zarzadza czasem ich zycia detekcja kolizji oraz modyfikacja atrybutow 
class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

        #Losowanie typu powerupu
        self.typ = random.choice(["Shield", "SpeedBoost", "RapidFire", "ExtraLife", "Bomb"])
        self.kolor = KOLORY_POWERUPOW[self.typ]

        #Optymalizacja hirboxa
        #Mniejszy hitbox wyœrodkowany w kafelku (¿eby nie zbieraæ bonusów rogiem)
        self.hitbox = pygame.Rect(int(self.x) + 8, int(self.y) + 8, 16, 16)

        self.czas_powstania = pygame.time.get_ticks()
        self.aktywny = True
        self.image = None

        #Przypisanie tekstur,grafik z arkusza
        if self.typ == "Shield":       # He³m (ochrona)
            self.sprite_x = 256
            self.sprite_y = 112
            
        elif self.typ == "SpeedBoost": # Zegarek (przyspieszenie)
            self.sprite_x = 272
            self.sprite_y = 112
            
        elif self.typ == "RapidFire":  # Gwiazdka (zmiejszenie cooldownu strzalu)
            self.sprite_x = 304
            self.sprite_y = 112
            
        elif self.typ == "ExtraLife":  # Czolg (dodatkowe zycie)
            self.sprite_x = 336
            self.sprite_y = 112
            
        elif self.typ == "Bomb":       # Granat (wysadza wszystkich)
            self.sprite_x = 320
            self.sprite_y = 112
            
        else:
            self.sprite_x = 0
            self.sprite_y = 0

        #Inicjalizacja tekstur po ustaleniu wspolrzednych
        self.aktualizuj_grafike()

        #Funkcja pobiera wycinek z obiektu klasy SpriteSheet i skaluje go do wielkosci kafelka
    def aktualizuj_grafike(self):
        self.image = arkusz_grafik.pobierz_obrazek(
            x=self.sprite_x,
            y=self.sprite_y,
            szerokosc=16,
            wysokosc=16,
            rozmiar_docelowy=(ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
        )

    #Funkcja zarzadza czasem zycia powerupu (10s)
    def update(self):
        if pygame.time.get_ticks() - self.czas_powstania > 10000:
            self.aktywny = False

    #Funkcja renderuje grafiki obiektu na planszy
    def draw(self, okno):
        if self.aktywny:
            if hasattr(self, 'image') and self.image:
                okno.blit(self.image, (self.x, self.y))
            else:
                #Awaryjne ko³o, jeœli grafika siê nie za³aduje
                pygame.draw.circle(okno, self.kolor, (int(self.x) + 16, int(self.y) + 16), 10)

    #Funkcja logiczna podniesienia powerupu przez gracza
    def zastosuj(self, gra):
        gra.audio.play_sound('powerup') 
        gra.wynik += 500
        obecny_czas = pygame.time.get_ticks()
      
        #Wyswietlanie powiadomienia w interfejsie w grze (HUD)
        if self.typ in ["ExtraLife", "Bomb"]:
            gra.powiadomienie_bonus = "1-UP" if self.typ == "ExtraLife" else "BOMB"
            gra.koniec_powiadomienia = obecny_czas + 3000

        #Zmodyfikowanie atrybutu gracza (dodanie punktu zycia)
        if self.typ == "ExtraLife": 
            gra.gracz.liczba_zyc += 1
    
        #Wyczyszczenie wszystkich jednostek wroga z planszy
        elif self.typ == "Bomb":
            gra.audio.play_sound('wybuch')
            for w in gra.przeciwnicy:
                gra.wynik += 100
                nazwa_typu = w.__class__.__name__
                if nazwa_typu in gra.zabite_czolgi: 
                    gra.zabite_czolgi[nazwa_typu] += 1
                else: 
                    gra.zabite_czolgi[nazwa_typu] = 1
                if w in gra.obiekty_w_grze: 
                    gra.obiekty_w_grze.remove(w)
            gra.przeciwnicy.clear()

        #Zmodyfikowanie atrybutu gracza (Zwiekszenie predkosci gracza)
        elif self.typ == "SpeedBoost": 
            gra.gracz.predkosc += 1
            gra.gracz.koniec_speed = obecny_czas + 10000

        #Zmodyfikowanie atrybutu gracza (dodanie tarczy)
        elif self.typ == "Shield":
            gra.gracz.tarcza_aktywna = True
            gra.gracz.koniec_tarczy = obecny_czas + 10000

        #Zmodyfikowanie atrybutu gracza (zmiejszenie cooldownu strzalu)
        elif self.typ == "RapidFire":
            gra.gracz.cooldown_strzalu = 200
            gra.gracz.koniec_rapid_fire = obecny_czas + 10000

    #Funkcja logiczna podniesienia powerupu przez enemy czolg
    def zastosuj_dla_wroga(self, wrog, gra):
        #Jesli enemy zbierze bombe grazc traci 1 zycie
        if self.typ == "Bomb":
            gra.audio.play_sound('wybuch')
            if not getattr(gra.gracz, 'tarcza_aktywna', False):
                gra.gracz.liczba_zyc -= 1
                if gra.gracz.liczba_zyc <= 0: 
                    gra.kurtyna_aktywna = True
                    gra.stan_konca_gry = "PRZEGRANA"
        elif self.typ == "SpeedBoost": 
            wrog.predkosc += 1
        elif self.typ == "ExtraLife": 
            wrog.hp += 1
        elif self.typ == "RapidFire": 
            wrog.cooldown_strzalu = 500


