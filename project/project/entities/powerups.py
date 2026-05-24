import pygame
import random
from entities.game_object import GameObject
from constants import ROZMIAR_KAFELKA
from map.spritesheet import arkusz_grafik 

KOLORY_POWERUPOW={
    "Shield": (0, 255, 255),
    "SpeedBoost": (255, 255, 0),
    "RapidFire": (255, 100, 0),
    "ExtraLife": (0, 255, 255),
    "Bomb": (255, 0, 0)
}

class PowerUp(GameObject):
    # ... (Twój obecny kod __init__, aktualizuj_grafike, update, draw bez zmian) ...
    
    # --- NOWE METODY OBS£UGI ZBIERANIA ---
    def zastosuj(self, gra):
        gra.audio.play_sound('powerup') 
        gra.wynik += 500
        obecny_czas = pygame.time.get_ticks()
        
        if self.typ in ["ExtraLife", "Bomb"]:
            gra.powiadomienie_bonus = "1-UP" if self.typ == "ExtraLife" else "BOMB"
            gra.koniec_powiadomienia = obecny_czas + 3000

        if self.typ == "ExtraLife": 
            gra.gracz.liczba_zyc += 1
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
        elif self.typ == "SpeedBoost": 
            gra.gracz.predkosc += 1
            gra.gracz.koniec_speed = obecny_czas + 10000
        elif self.typ == "Shield":
            gra.gracz.tarcza_aktywna = True
            gra.gracz.koniec_tarczy = obecny_czas + 10000
        elif self.typ == "RapidFire":
            gra.gracz.cooldown_strzalu = 200
            gra.gracz.koniec_rapid_fire = obecny_czas + 10000

    def zastosuj_dla_wroga(self, wrog, gra):
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