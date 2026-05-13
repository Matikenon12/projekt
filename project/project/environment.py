import pygame
import random

from constants import CZARNY, FPS, SZEROKOSC_OKNA, WYSOKOSC_OKNA, ROZMIAR_KAFELKA
from entities.player_tank import PlayerTank
from entities.enemy_tank import EnemyTank, BasicTank, FastTank, ArmoredTank, ShooterTank
from entities.base import Base
from entities.powerups import PowerUp
from map.levels import WSZYSTKIE_POZIOMY
from map.tile import BrickWall, SteelWall, Water, Bush

class Environment:
    def __init__(self):
        pygame.init()
        self.okno = pygame.display.set_mode((SZEROKOSC_OKNA, WYSOKOSC_OKNA))
        pygame.display.set_caption("TANKS 1990 / BATTLE CITY")

        self.dziala = True
        self.zegar = pygame.time.Clock()

        # Próba za³adowania pikselowej czcionki, jeœli plik czcionka.ttf istnieje
        try:
            self.czcionka_hud = pygame.font.Font("czcionka.ttf", 16)
            self.czcionka_duza = pygame.font.Font("czcionka.ttf", 40)
        except FileNotFoundError:
            self.czcionka_hud = pygame.font.SysFont("Courier", 20, bold=True)
            self.czcionka_duza = pygame.font.SysFont("Courier", 50, bold=True)

        self.obiekty_w_grze = []
        self.sciany = []

        self.aktualny_numer_poziomu = 0
        self.wynik = 0

        # --- ZMIENNE STANU GRY ---
        self.stan_gry = "EKRAN_POZIOMU" # Mo¿liwe: EKRAN_POZIOMU, GRA, KONIEC_GRY, WYGRANA
        self.czas_wyswietlania_ekranu = 0
        self.czas_startu_rundy = 0
        self.sekundy_w_rundzie = 0

        self.zaladuj_poziom(self.aktualny_numer_poziomu)

    def zaladuj_poziom(self, numer):
        self.obiekty_w_grze = []
        self.sciany = []
        self.przeciwnicy = []

        dane_poziomu = WSZYSTKIE_POZIOMY[numer]
        mapa = dane_poziomu["mapa"]
        start_x, start_y = dane_poziomu["start_gracza"]

        # Kolejka wrogów do wypuszczenia i zegar spawnowania
        self.kolejka_wrogow = dane_poziomu["fala_wrogow"].copy()
        self.ostatni_spawn = pygame.time.get_ticks()

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

                if nowy_kafelek:
                    self.obiekty_w_grze.append(nowy_kafelek)
                    if nowy_kafelek.blokuje_czolgi: self.sciany.append(nowy_kafelek)

        self.baza = Base(12 * ROZMIAR_KAFELKA, 16 * ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.baza)
        self.gracz = PlayerTank(start_x * ROZMIAR_KAFELKA, start_y * ROZMIAR_KAFELKA)
        self.obiekty_w_grze.append(self.gracz)

        # Ustawienie ekranu rundy na 2.5 sekundy
        self.stan_gry = "EKRAN_POZIOMU"
        self.czas_wyswietlania_ekranu = pygame.time.get_ticks() + 2500

    def nastepny_poziom(self):
        self.aktualny_numer_poziomu += 1
        if self.aktualny_numer_poziomu < len(WSZYSTKIE_POZIOMY):
            self.zaladuj_poziom(self.aktualny_numer_poziomu)
        else:
            self.stan_gry = "WYGRANA"

    def obsluga_zdarzen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dziala = False

    def aktualizacja(self):
        obecny_czas = pygame.time.get_ticks()

        if self.stan_gry == "EKRAN_POZIOMU":
            if obecny_czas > self.czas_wyswietlania_ekranu:
                self.stan_gry = "GRA"
                self.czas_startu_rundy = obecny_czas
            return

        if self.stan_gry in ["KONIEC_GRY", "WYGRANA"]:
            return

        # SPAWN
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

        # STRZELANIE I RUCH
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            p = self.gracz.strzelaj()
            if p: self.obiekty_w_grze.append(p)

        for wrog in self.przeciwnicy:
            p = wrog.strzelaj()
            if p: self.obiekty_w_grze.append(p)

        for obiekt in self.obiekty_w_grze:
            if isinstance(obiekt, EnemyTank): obiekt.update(self.sciany, self.baza, self.gracz)
            elif obiekt == self.gracz: obiekt.update(self.sciany)
            else: obiekt.update()

        # KOLIZJE POCISKÓW (Pêtla 1)
        for obj in self.obiekty_w_grze:
            if hasattr(obj, 'kierunek') and hasattr(obj, 'wlasciciel'):
                if obj.hitbox.colliderect(self.baza.hitbox) and not self.baza.zniszczona:
                    obj.aktywny = False
                    self.baza.zniszczona = True
                    self.stan_gry = "KONIEC_GRY"

                for sciana in self.sciany:
                    if obj.hitbox.colliderect(sciana.hitbox) and sciana.blokuje_pociski:
                        obj.aktywny = False
                        if getattr(sciana, 'zniszczalny', False):
                            if sciana in self.obiekty_w_grze: self.obiekty_w_grze.remove(sciana)
                            if sciana in self.sciany: self.sciany.remove(sciana)
                        break

                if obj.wlasciciel == "wrog" and obj.hitbox.colliderect(self.gracz.hitbox) and obj.aktywny:
                    obj.aktywny = False
                    if not getattr(self.gracz, 'tarcza_aktywna', False):
                        self.gracz.liczba_zyc -= 1
                        if self.gracz.liczba_zyc <= 0: self.stan_gry = "KONIEC_GRY"

                if obj.wlasciciel == "gracz" and obj.aktywny:
                    for wrog in self.przeciwnicy:
                        if obj.hitbox.colliderect(wrog.hitbox):
                            obj.aktywny = False
                            wrog.hp -= 1
                            if wrog.hp <= 0:
                                self.przeciwnicy.remove(wrog)
                                self.obiekty_w_grze.remove(wrog)
                                self.wynik += 100
                                if random.randint(1, 100) > 50:
                                    self.obiekty_w_grze.append(PowerUp(wrog.x, wrog.y))
                            break

        # ZBIERANIE BONUSÓW (Pêtla 2 - ODDZIELNA!)
        for p_up in self.obiekty_w_grze:
            if isinstance(p_up, PowerUp) and p_up.aktywny:
                if self.gracz.hitbox.colliderect(p_up.hitbox):
                    p_up.aktywny = False
                    self.wynik += 500
                    
                    # --- POWIADOMIENIE NA HUD (3 SEKUNDY DLA BOMBY I ZYCIA) ---
                    if p_up.typ in ["ExtraLife", "Bomb"]:
                        self.powiadomienie_bonus = "1-UP" if p_up.typ == "ExtraLife" else "BOMB"
                        self.koniec_powiadomienia = pygame.time.get_ticks() + 3000
                    # ----------------------------------------------------------

                    if p_up.typ == "ExtraLife": self.gracz.liczba_zyc += 1
                    elif p_up.typ == "Bomb":
                        for w in self.przeciwnicy:
                            self.wynik += 100
                            if w in self.obiekty_w_grze: self.obiekty_w_grze.remove(w)
                        self.przeciwnicy.clear()
                    elif p_up.typ == "SpeedBoost": self.gracz.predkosc += 1
                    elif p_up.typ == "Shield":
                        self.gracz.tarcza_aktywna = True
                        self.gracz.koniec_tarczy = pygame.time.get_ticks() + 10000
                    elif p_up.typ == "RapidFire":
                        self.gracz.cooldown_strzalu = 200
                        self.gracz.koniec_rapid_fire = pygame.time.get_ticks() + 10000

        # CZYSZCZENIE
        nowa = []
        for o in self.obiekty_w_grze:
            if hasattr(o, 'aktywny') and not o.aktywny: continue
            if hasattr(o, 'wlasciciel') and not (0 <= o.x <= 800 and 0 <= o.y <= 600): continue
            nowa.append(o)
        self.obiekty_w_grze = nowa

        if len(self.przeciwnicy) == 0 and len(self.kolejka_wrogow) == 0:
            self.nastepny_poziom()

    def rysuj_hud(self):
        # 1. Rysujemy szary pasek t³a dla HUD
        pygame.draw.rect(self.okno, (50, 50, 50), (0, 0, 800, 40)) 
        
        # Czas jest teraz liczony tylko w tle (do statystyk koñcowych)
        self.sekundy_w_rundzie = (pygame.time.get_ticks() - self.czas_startu_rundy) // 1000

        # Teksty podstawowe (czas usuniêty)
        tekst_zycia = self.czcionka_hud.render(f"LIVES:{self.gracz.liczba_zyc}", True, (255, 255, 255))
        tekst_wynik = self.czcionka_hud.render(f"PTS:{self.wynik}", True, (255, 255, 255))
        tekst_poziom = self.czcionka_hud.render(f"STAGE:{self.aktualny_numer_poziomu + 1}", True, (255, 255, 255))

        # --- LOGIKA WYŒWIETLANIA WSZYSTKICH BONUSÓW ---
        obecny_czas = pygame.time.get_ticks()
        aktywne = []
        
        if getattr(self.gracz, 'tarcza_aktywna', False): aktywne.append("SHIELD")
        if obecny_czas < getattr(self.gracz, 'koniec_rapid_fire', 0): aktywne.append("RAPID")
        if self.gracz.predkosc > 2: aktywne.append("SPEED")
        if hasattr(self, 'koniec_powiadomienia') and obecny_czas < getattr(self, 'koniec_powiadomienia', 0):
            aktywne.append(getattr(self, 'powiadomienie_bonus', ''))

        napis_bonus = " + ".join(aktywne) if aktywne else "NONE"
        kolor_bonusu = (255, 255, 0) if aktywne else (180, 180, 180) 
        tekst_bonus = self.czcionka_hud.render(f"POWER:{napis_bonus}", True, kolor_bonusu)

        # Uk³adamy na pasku z nowymi odstêpami - bonus ma teraz ca³¹ praw¹ stronê dla siebie!
        self.okno.blit(tekst_zycia, (20, 10))
        self.okno.blit(tekst_wynik, (160, 10))
        self.okno.blit(tekst_bonus, (330, 10)) 
        self.okno.blit(tekst_poziom, (680, 10))

    def rysowanie(self):
        self.okno.fill(CZARNY)

        if self.stan_gry == "EKRAN_POZIOMU":
            napis = self.czcionka_duza.render(f"RUNDA {self.aktualny_numer_poziomu + 1}", True, (255, 255, 255))
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, WYSOKOSC_OKNA//2 - napis.get_height()//2))

        elif self.stan_gry == "KONIEC_GRY":
            napis = self.czcionka_duza.render("GAME OVER", True, (255, 0, 0))
            wynik = self.czcionka_hud.render(f"WYNIK KONCOWY: {self.wynik}", True, (255, 255, 255))
            czas = self.czcionka_hud.render(f"PRZEZYTO CZASU: {self.sekundy_w_rundzie}s", True, (255, 255, 255))
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, 200))
            self.okno.blit(wynik, (SZEROKOSC_OKNA//2 - wynik.get_width()//2, 300))
            self.okno.blit(czas, (SZEROKOSC_OKNA//2 - czas.get_width()//2, 350))

        elif self.stan_gry == "WYGRANA":
            napis = self.czcionka_duza.render("WYGRALES!", True, (0, 255, 0))
            wynik = self.czcionka_hud.render(f"WYNIK KONCOWY: {self.wynik}", True, (255, 255, 255))
            self.okno.blit(napis, (SZEROKOSC_OKNA//2 - napis.get_width()//2, 200))
            self.okno.blit(wynik, (SZEROKOSC_OKNA//2 - wynik.get_width()//2, 300))

        elif self.stan_gry == "GRA":
            # Rysujemy wszystko poza krzakami
            for obiekt in self.obiekty_w_grze:
                if not isinstance(obiekt, Bush):
                    obiekt.draw(self.okno)
            # Rysujemy krzaki na koñcu
            for obiekt in self.obiekty_w_grze:
                if isinstance(obiekt, Bush):
                    obiekt.draw(self.okno)
            self.rysuj_hud()

        pygame.display.flip()

    def uruchom(self):
        while self.dziala:
            self.obsluga_zdarzen()
            self.aktualizacja()
            self.rysowanie()
            self.zegar.tick(FPS)
        pygame.quit()
