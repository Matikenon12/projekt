import pygame
import random
import os

from constants import CZARNY, FPS, SZEROKOSC_OKNA, WYSOKOSC_OKNA, ROZMIAR_KAFELKA, CIEMNY_SZARY, BIALY, ZOLTY, JASNY_SZARY, JASNY_CZERWONY
from entities.player_tank import PlayerTank
from entities.enemy_tank import EnemyTank, BasicTank, FastTank, ArmoredTank, ShooterTank
from entities.base import Base
from entities.powerups import PowerUp
from map.levels import WSZYSTKIE_POZIOMY
from map.tile import BrickWall, SteelWall, Water, Bush, Ice
from assets.sounds import AudioManager
from map.spritesheet import arkusz_grafik
from utils.collision import sprawdz_wszystkie_kolizje  # DODANY IMPORT SYSTEMU KOLIZJI

class Environment:
    def __init__(self):
        pygame.init()
        
        self.okno = pygame.display.set_mode((SZEROKOSC_OKNA, WYSOKOSC_OKNA))
        pygame.display.set_caption("TANKS 1990 / BATTLE CITY")

        self.dziala = True
        self.zegar = pygame.time.Clock()

        try:
            self.czcionka_hud = pygame.font.Font("kongtext.ttf", 16)
            self.czcionka_duza = pygame.font.Font("kongtext.ttf", 40)
        except FileNotFoundError:
            self.czcionka_hud = pygame.font.SysFont("Courier", 20, bold=True)
            self.czcionka_duza = pygame.font.SysFont("Courier", 50, bold=True)

        self.obiekty_w_grze = []
        self.sciany = []

        self.aktualny_numer_poziomu = 0
        self.wynik = 0
        self.wynik_na_poczatku_poziomu = 0 
        self.zabite_czolgi = {"BasicTank": 0, "FastTank": 0, "ArmoredTank": 0, "ShooterTank": 0}

        self.stan_gry = "EKRAN_STARTOWY" 
        self.opcje_menu = ["NOWA GRA", "POZIOM 1", "POZIOM 2", "POZIOM 3"]
        self.wybrana_opcja = 0
        self.tryb_kampanii = True 
        
        self.czas_wyswietlania_ekranu = 0
        self.czas_startu_rundy = 0
        self.sekundy_w_rundzie = 0
        
        self.dzwiek_jazdy_gra = False
        self.audio = AudioManager()

        # --- ZMIENNE DO ANIMACJI KURTYNY ---
        self.kurtyna_y = 600           
        self.kurtyna_aktywna = False   
        self.stan_konca_gry = None     

        self.zaladuj_poziom(self.aktualny_numer_poziomu)

    def zaladuj_poziom(self, numer):
        self.obiekty_w_grze = []
        self.sciany = []
        self.przeciwnicy = []
        
        self.zabite_czolgi = {"BasicTank": 0, "FastTank": 0, "ArmoredTank": 0, "ShooterTank": 0}
        self.wynik_na_poczatku_poziomu = self.wynik

        dane_poziomu = WSZYSTKIE_POZIOMY[numer]
        mapa = dane_poziomu["mapa"]
        start_x, start_y = dane_poziomu["start_gracza"]

        self.kolejka_wrogow = dane_poziomu["fala_wrogow"].copy()
        self.ostatni_spawn = pygame.time.get_ticks()
        self.ostatni_spawn_bonusu = pygame.time.get_ticks()

        for wiersz_idx, wiersz in enumerate(mapa):
            for kolumna_idx, wartosc in enumerate(wiersz):
                px = kolumna_idx * ROZMIAR_KAFELKA
                py = wiersz_idx * ROZMIAR_KAFELKA

                nowy_kafelek = None
                if wartosc == 1:
                    polowa = ROZMIAR_KAFELKA // 2
                    male_cegly = [BrickWall(px, py), BrickWall(px + polowa, py), BrickWall(px, py + polowa), BrickWall(px + polowa, py + polowa)]
                    for cegla in male_cegly:
                        self.obiekty_w_grze.append(cegla)
                        if cegla.blokuje_czolgi: self.sciany.append(cegla)
                elif wartosc == 2: nowy_kafelek = SteelWall(px, py)
                elif wartosc == 3: nowy_kafelek = Water(px, py)
                elif wartosc == 4: nowy_kafelek = Bush(px, py)
                elif wartosc == 5: nowy_kafelek = Ice(px, py)

                if nowy_kafelek:
                    self.obiekty_w_grze.append(nowy_kafelek)
                    if nowy_kafelek.blokuje_czolgi: self.sciany.append(nowy_kafelek)

        self.baza = Base(12 * ROZMIAR_KAFELKA, 16 * ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.baza)
        self.gracz = PlayerTank(start_x * ROZMIAR_KAFELKA, start_y * ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.gracz)

        if self.stan_gry != "EKRAN_STARTOWY":
            self.stan_gry = "EKRAN_POZIOMU"
            self.czas_wyswietlania_ekranu = pygame.time.get_ticks() + 2500

    def nastepny_poziom(self):
        if self.tryb_kampanii:
            self.aktualny_numer_poziomu += 1
            if self.aktualny_numer_poziomu < len(WSZYSTKIE_POZIOMY):
                self.zaladuj_poziom(self.aktualny_numer_poziomu)
            else:
                self.stan_gry = "WYGRANA"
                self.audio.play_sound('wygrana') 
        else:
            self.stan_gry = "WYGRANA"
            self.audio.play_sound('wygrana')     

    def obsluga_zdarzen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dziala = False
            elif event.type == pygame.KEYDOWN:
                if self.stan_gry == "EKRAN_STARTOWY":
                    if event.key == pygame.K_UP:
                        self.wybrana_opcja = (self.wybrana_opcja - 1) % len(self.opcje_menu)
                        self.audio.play_sound('wybor')
                    elif event.key == pygame.K_DOWN:
                        self.wybrana_opcja = (self.wybrana_opcja + 1) % len(self.opcje_menu)
                        self.audio.play_sound('wybor')
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.audio.play_sound('wybor')
                        if self.wybrana_opcja == 0:  
                            self.wynik = 0
                            self.wynik_na_poczatku_poziomu = 0
                            self.aktualny_numer_poziomu = 0
                            self.tryb_kampanii = True 
                        elif self.wybrana_opcja == 1: 
                            self.aktualny_numer_poziomu = 0
                            self.tryb_kampanii = False 
                        elif self.wybrana_opcja == 2: 
                            self.aktualny_numer_poziomu = 1
                            self.tryb_kampanii = False 
                        elif self.wybrana_opcja == 3: 
                            self.aktualny_numer_poziomu = 2
                            self.tryb_kampanii = False 
                        
                        self.zaladuj_poziom(self.aktualny_numer_poziomu)
                        self.stan_gry = "EKRAN_POZIOMU"
                        self.czas_wyswietlania_ekranu = pygame.time.get_ticks() + 2500
                        
                elif self.stan_gry == "PODSUMOWANIE_POZIOMU":
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if getattr(self, 'podsumowanie_gotowe', False):
                            self.audio.stop_sound('wygrana')
                            self.nastepny_poziom()
                        else:
                            self.podsumowanie_etap = 4
                            self.wyswietlany_wynik = self.wynik
                            self.podsumowanie_gotowe = True
                        
                elif self.stan_gry in ["KONIEC_GRY", "WYGRANA"]:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.stan_gry = "EKRAN_STARTOWY"

    def aktualizacja(self):
        obecny_czas = pygame.time.get_ticks()

        # JEŒLI KURTYNA WJE¯D¯A LUB TRWA, ZAMRA¯AMY RUCH CZO£GÓW I POCISKÓW
        if getattr(self, 'kurtyna_aktywna', False):
            if getattr(self, 'dzwiek_jazdy_gra', False):
                self.audio.stop_sound('jazda')
                self.dzwiek_jazdy_gra = False
            return

        if self.stan_gry != "GRA":
            if getattr(self, 'dzwiek_jazdy_gra', False):
                self.audio.stop_sound('jazda')
                self.dzwiek_jazdy_gra = False

        if self.stan_gry == "EKRAN_STARTOWY":
            return

        if self.stan_gry == "EKRAN_POZIOMU":
            if obecny_czas > self.czas_wyswietlania_ekranu:
                self.stan_gry = "GRA"
                self.czas_startu_rundy = obecny_czas
            return

        if self.stan_gry == "PODSUMOWANIE_POZIOMU":
            if not getattr(self, 'podsumowanie_gotowe', False):
                if obecny_czas > getattr(self, 'podsumowanie_ostatnia_zmiana', 0):
                    if self.podsumowanie_etap < 4:
                        typ = self.podsumowanie_typy[self.podsumowanie_etap]
                        cel = self.zabite_czolgi.get(typ, 0)
                        
                        if self.podsumowanie_licznik < cel:
                            self.podsumowanie_licznik += 1
                            self.audio.play_sound('wybor') 
                            self.podsumowanie_ostatnia_zmiana = obecny_czas + 150 
                        else:
                            self.podsumowanie_etap += 1
                            self.podsumowanie_licznik = 0
                            self.podsumowanie_ostatnia_zmiana = obecny_czas + 300 
                            
                    elif self.podsumowanie_etap == 4:
                        if self.wyswietlany_wynik < self.wynik:
                            krok = max(10, (self.wynik - self.wyswietlany_wynik) // 10) 
                            self.wyswietlany_wynik = min(self.wyswietlany_wynik + krok, self.wynik)
                            self.audio.play_sound('wybor') 
                            self.podsumowanie_ostatnia_zmiana = obecny_czas + 50
                        else:
                            self.podsumowanie_gotowe = True
            return

        if self.stan_gry in ["KONIEC_GRY", "WYGRANA"]:
            return

        # SPRAWDZANIE WARUNKU WYGRANEJ POZIOMU Z KURTYN¥
        if len(self.przeciwnicy) == 0 and len(self.kolejka_wrogow) == 0 and self.stan_gry == "GRA":
            self.kurtyna_aktywna = True
            self.stan_konca_gry = "WYGRANA"
            self.audio.play_sound('wygrana')
            return

        if hasattr(self, 'kolejka_wrogow') and len(self.kolejka_wrogow) > 0 and obecny_czas - self.ostatni_spawn > 3000 and len(self.przeciwnicy) < 4:
            typ_wroga = self.kolejka_wrogow.pop(0)
            wx = random.choice([1, 23]) * ROZMIAR_KAFELKA
            wy = 1 * ROZMIAR_KAFELKA 
            if typ_wroga == "Basic": nowy_wrog = BasicTank(wx, wy)
            elif typ_wroga == "Fast": nowy_wrog = FastTank(wx, wy)
            elif typ_wroga == "Armored": nowy_wrog = ArmoredTank(wx, wy)
            elif typ_wroga == "Shooter": nowy_wrog = ShooterTank(wx, wy)
            else: nowy_wrog = EnemyTank(wx, wy)
            self.obiekty_w_grze.append(nowy_wrog)
            self.przeciwnicy.append(nowy_wrog)
            self.ostatni_spawn = obecny_czas

        if hasattr(self, 'ostatni_spawn_bonusu') and obecny_czas - self.ostatni_spawn_bonusu > 12000:
            self.ostatni_spawn_bonusu = obecny_czas
            wolne_miejsca = []
            for x in range(0, 800, ROZMIAR_KAFELKA):
                for y in range(0, 600, ROZMIAR_KAFELKA):
                    test_rect = pygame.Rect(x, y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA)
                    zajete = False
                    for obj in self.obiekty_w_grze:
                        if test_rect.colliderect(obj.hitbox):
                            zajete = True
                            break
                    if not zajete:
                        wolne_miejsca.append((x, y))
            
            if wolne_miejsca:
                bx, by = random.choice(wolne_miejsca)
                nowy_bonus = PowerUp(bx, by)
                nowy_bonus.czas_wygasniecia = obecny_czas + 10000 
                self.obiekty_w_grze.append(nowy_bonus)

        keys = pygame.key.get_pressed()
        ruch_gracza = keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_RIGHT]
        ruch_wrogow = len(self.przeciwnicy) > 0
        
        if ruch_gracza or ruch_wrogow:
            if not getattr(self, 'dzwiek_jazdy_gra', False):
                self.audio.play_sound('jazda', loops=-1)
                self.dzwiek_jazdy_gra = True
        else:
            if getattr(self, 'dzwiek_jazdy_gra', False):
                self.audio.stop_sound('jazda')
                self.dzwiek_jazdy_gra = False

        if keys[pygame.K_SPACE]:
            p = self.gracz.strzelaj()
            if p: 
                self.obiekty_w_grze.append(p)
                self.audio.play_sound('strzal') 

        for wrog in self.przeciwnicy:
            p = wrog.strzelaj()
            if p: self.obiekty_w_grze.append(p)

        przeszkody_dla_czolgow = self.sciany + [self.baza]
        for obiekt in self.obiekty_w_grze:
            if isinstance(obiekt, EnemyTank): obiekt.update(przeszkody_dla_czolgow, self.baza, self.gracz)
            elif obiekt == self.gracz: obiekt.update(przeszkody_dla_czolgow)
            else: obiekt.update()

        # --- WYWO£ANIE NOWEGO ZEWNÊTRZNEGO SYSTEMU KOLIZJI I WYBUCHÓW ---
        sprawdz_wszystkie_kolizje(self)

        # Filtrowanie i usuwanie nieaktywnych œmieci z planszy
        nowa = []
        for o in self.obiekty_w_grze:
            if hasattr(o, 'aktywny') and not o.aktywny: continue
            if hasattr(o, 'wlasciciel') and not (0 <= o.x <= 800 and 0 <= o.y <= 600): continue
            nowa.append(o)
        self.obiekty_w_grze = nowa

    def obsluga_animacji_kurtyny(self):
        if not getattr(self, 'kurtyna_aktywna', False):
            return

        # Zwijanie kurtyny do góry
        if self.kurtyna_y > 0:
            self.kurtyna_y -= 10
            if self.kurtyna_y < 0:
                self.kurtyna_y = 0

        # Rysowanie czarnego prostok¹ta
        pygame.draw.rect(self.okno, (0, 0, 0), (0, self.kurtyna_y, 1000, 600 - self.kurtyna_y))

        # Kiedy wjedzie na sam¹ górê - rysujemy tekst i czekamy na klawisz
        if self.kurtyna_y == 0:
            if self.stan_konca_gry == "WYGRANA":
                tekst_glowny = "STAGE CLEAR"
                kolor_tekstu = (0, 255, 0)
            else:
                tekst_glowny = "GAME OVER"
                kolor_tekstu = (255, 0, 0)

            napis_wynikowy = self.czcionka_duza.render(tekst_glowny, True, kolor_tekstu)
            rect_napisu = napis_wynikowy.get_rect(center=(400, 260))
            self.okno.blit(napis_wynikowy, rect_napisu)

            tekst_dalej = self.czcionka_hud.render("PRESS ENTER TO CONTINUE", True, (255, 255, 255))
            rect_dalej = tekst_dalej.get_rect(center=(400, 340))
            self.okno.blit(tekst_dalej, rect_dalej)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.kurtyna_aktywna = False
                self.kurtyna_y = 600
                
                if self.stan_konca_gry == "WYGRANA":
                    self.stan_gry = "PODSUMOWANIE_POZIOMU"
                    self.podsumowanie_etap = 0
                    self.podsumowanie_licznik = 0
                    self.podsumowanie_ostatnia_zmiana = pygame.time.get_ticks() + 500 
                    self.podsumowanie_typy = ["BasicTank", "FastTank", "ArmoredTank", "ShooterTank"]
                    self.podsumowanie_gotowe = False
                    self.wyswietlany_wynik = self.wynik_na_poczatku_poziomu
                else:
                    self.stan_gry = "KONIEC_GRY"

    def rysuj_hud(self):
        pygame.draw.rect(self.okno, CIEMNY_SZARY, (800, 0, 200, 600))
        self.sekundy_w_rundzie = (pygame.time.get_ticks() - self.czas_startu_rundy) // 1000

        tekst_poziom = self.czcionka_hud.render(f"STAGE: {self.aktualny_numer_poziomu + 1}", True, BIALY)
        tekst_wynik = self.czcionka_hud.render(f"PTS: {self.wynik}", True, BIALY)
        tekst_zycia = self.czcionka_hud.render(f"LIVES: {self.gracz.liczba_zyc}", True, BIALY)

        self.okno.blit(tekst_poziom, (820, 40))
        self.okno.blit(tekst_wynik, (820, 100))
        self.okno.blit(tekst_zycia, (820, 160))

        obecny_czas = pygame.time.get_ticks()
        aktywne = []
        if getattr(self.gracz, 'tarcza_aktywna', False): aktywne.append("SHIELD")
        if obecny_czas < getattr(self.gracz, 'koniec_rapid_fire', 0): aktywne.append("RAPID")
        if obecny_czas < getattr(self.gracz, 'koniec_speed', 0) or self.gracz.predkosc > 2: aktywne.append("SPEED")
        if hasattr(self, 'koniec_powiadomienia') and obecny_czas < getattr(self, 'koniec_powiadomienia', 0):
            aktywne.append(getattr(self, 'powiadomienie_bonus', ''))

        tekst_bonus_label = self.czcionka_hud.render("POWERUPS:", True, BIALY)
        self.okno.blit(tekst_bonus_label, (820, 240))

        start_y_bonusow = 280  
        odstep_y = 42

        koordynaty_ikon = {
            "SHIELD": (256, 112),
            "SPEED":  (272, 112),
            "RAPID":  (304, 112),
            "BOMB":   (320, 112),
            "1-UP":   (336, 112)
        }

        if aktywne:
            for index, nazwa_bonusu in enumerate(aktywne):
                obecne_y = start_y_bonusow + (index * odstep_y)
                
                if nazwa_bonusu in koordynaty_ikon:
                    spr_x, spr_y = koordynaty_ikon[nazwa_bonusu]
                    ikona_image = arkusz_grafik.pobierz_obrazek(
                        x=spr_x, y=spr_y, szerokosc=16, wysokosc=16, rozmiar_docelowy=(32, 32)
                    )
                    self.okno.blit(ikona_image, (820, obecne_y))
                
                tekst_pojedynczy_bonus = self.czcionka_hud.render(str(nazwa_bonusu), True, ZOLTY)
                self.okno.blit(tekst_pojedynczy_bonus, (865, obecne_y + 6))
        else:
            tekst_brak = self.czcionka_hud.render("NONE", True, JASNY_SZARY)
            self.okno.blit(tekst_brak, (820, start_y_bonusow))

        wrogowie_lewa = len(self.kolejka_wrogow) + len(self.przeciwnicy)
        tekst_wrogowie = self.czcionka_hud.render(f"ENEMIES: {wrogowie_lewa}", True, JASNY_CZERWONY)
        self.okno.blit(tekst_wrogowie, (820, 500))

    def rysowanie(self):
        self.okno.fill(CZARNY)

        if self.stan_gry == "EKRAN_STARTOWY":
            tytul = self.czcionka_duza.render("BATTLE CITY", True, (255, 255, 0))
            self.okno.blit(tytul, (SZEROKOSC_OKNA//2 - tytul.get_width()//2, 120))
            
            for idx, opcja in enumerate(self.opcje_menu):
                if idx == self.wybrana_opcja:
                    kolor = (255, 255, 0)
                    tekst_str = f"> {opcja} <"
                else:
                    kolor = (255, 255, 255)
                    tekst_str = opcja
                    
                tekst_opcji = self.czcionka_hud.render(tekst_str, True, kolor)
                self.okno.blit(tekst_opcji, (SZEROKOSC_OKNA//2 - tekst_opcji.get_width()//2, 280 + idx * 45))

        elif self.stan_gry == "EKRAN_POZIOMU":
            napis = self.czcionka_duza.render(f"STAGE {self.aktualny_numer_poziomu + 1}", True, (255, 255, 255))
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, WYSOKOSC_OKNA//2 - napis.get_height()//2))

        elif self.stan_gry == "PODSUMOWANIE_POZIOMU":
            napis = self.czcionka_duza.render(f"STAGE {self.aktualny_numer_poziomu + 1} CLEARED!", True, (255, 255, 0))
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, 80))
            
            y_offset = 180
            suma_zabitych = 0
            
            for i in range(4):
                if hasattr(self, 'podsumowanie_etap') and getattr(self, 'podsumowanie_etap', 0) >= i:
                    typ = self.podsumowanie_typy[i]
                    czysty_typ = typ.replace("Tank", "").upper()
                    
                    if self.podsumowanie_etap > i:
                        ilosc_do_pokazania = self.zabite_czolgi.get(typ, 0)
                        kolor = (150, 150, 150) 
                    else:
                        ilosc_do_pokazania = self.podsumowanie_licznik
                        kolor = (255, 255, 255) 
                        
                    tekst = self.czcionka_hud.render(f"{czysty_typ} TANKS KILLED: {ilosc_do_pokazania}", True, kolor)
                    self.okno.blit(tekst, (SZEROKOSC_OKNA//2 - tekst.get_width()//2, y_offset))
                    suma_zabitych += ilosc_do_pokazania
                y_offset += 40
                    
            if hasattr(self, 'podsumowanie_etap') and self.podsumowanie_etap >= 4:
                y_offset += 20
                tekst_suma = self.czcionka_hud.render(f"TOTAL KILLS IN STAGE: {suma_zabitych}", True, (255, 100, 100))
                self.okno.blit(tekst_suma, (SZEROKOSC_OKNA//2 - tekst_suma.get_width()//2, y_offset))
                
                y_offset += 60
                tekst_wynik = self.czcionka_hud.render(f"TOTAL SCORE: {getattr(self, 'wyswietlany_wynik', 0)}", True, (0, 255, 0))
                self.okno.blit(tekst_wynik, (SZEROKOSC_OKNA//2 - tekst_wynik.get_width()//2, y_offset))
            
            if getattr(self, 'podsumowanie_gotowe', False):
                restart = self.czcionka_hud.render("WCISNIJ SPACJE ABY KONTYNUOWAC", True, (255, 255, 255))
                self.okno.blit(restart, (SZEROKOSC_OKNA//2 - restart.get_width()//2, 500))

        elif self.stan_gry == "KONIEC_GRY":
            napis = self.czcionka_duza.render("GAME OVER", True, (255, 0, 0))
            wynik = self.czcionka_hud.render(f"WYNIK KONCOWY: {self.wynik}", True, (255, 255, 255))
            czas = self.czcionka_hud.render(f"PRZEZYTO CZASU: {self.sekundy_w_rundzie}s", True, (255, 255, 255))
            restart = self.czcionka_hud.render("WCISNIJ SPACJE ABY WROCIC DO MENU", True, (255, 255, 0))
            
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, 150))
            self.okno.blit(wynik, (SZEROKOSC_OKNA//2 - wynik.get_width()//2, 250))
            self.okno.blit(czas, (SZEROKOSC_OKNA//2 - czas.get_width()//2, 300))
            self.okno.blit(restart, (SZEROKOSC_OKNA//2 - restart.get_width()//2, 420))

        elif self.stan_gry == "WYGRANA":
            napis = self.czcionka_duza.render("WYGRALES CALA GRE!", True, (0, 255, 0))
            wynik = self.czcionka_hud.render(f"WYNIK KONCOWY: {self.wynik}", True, (255, 255, 255))
            restart = self.czcionka_hud.render("WCISNIJ SPACJE ABY WROCIC DO MENU", True, (255, 255, 0))
            
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, 150))
            self.okno.blit(wynik, (SZEROKOSC_OKNA//2 - wynik.get_width()//2, 250))
            self.okno.blit(restart, (SZEROKOSC_OKNA//2 - restart.get_width()//2, 380))

        elif self.stan_gry == "GRA":
            for obiekt in self.obiekty_w_grze:
                if not isinstance(obiekt, Bush):
                    obiekt.draw(self.okno)
            for obiekt in self.obiekty_w_grze:
                if isinstance(obiekt, Bush):
                    obiekt.draw(self.okno)      
            
            self.rysuj_hud()
            self.obsluga_animacji_kurtyny()

        pygame.display.flip()

    def uruchom(self):
        while self.dziala:
            self.obsluga_zdarzen()
            self.aktualizacja()
            self.rysowanie()
            self.zegar.tick(FPS)
        pygame.quit()