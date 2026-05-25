import pygame
import os

#Klasa zarzadzajaca audio w grze 
class AudioManager:
    def __init__(self):
        #Inicjalizacja miksera dzwieku jesli nie zostal uruchomiony wczesniej
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        self.dzwieki = {}
        self.zaladuj_dzwieki()

    #Lokalizacja zasobow
    def zaladuj_dzwieki(self):
        #Automatyczne wykrywanie sciezki folderu z dzwiekami
        katalog_pliku = os.path.dirname(os.path.abspath(__file__))
        folder_dzwiekow = os.path.join(katalog_pliku, "dzwieki")
        
        #Funkcja pomocnicza do bezpiecznego wczytywania plikow .wav/.mp3/.ogg 
        def wczytaj(nazwa):
            sciezka = os.path.join(folder_dzwiekow, nazwa)
            if os.path.exists(sciezka):
                try:
                    return pygame.mixer.Sound(sciezka)
                except Exception as e:
                    print(f"Blad ladowania dzwieku {nazwa}: {e}")
                    return None
            else:
                print(f"Brakuje pliku dzwiekowego: {nazwa}")
            return None

       
        #Ladowanie dzwiekow do slownika
        self.dzwieki['strzal'] = wczytaj('strzal.wav')
        self.dzwieki['powerup'] = wczytaj('powerup.wav')
        self.dzwieki['wybuch'] = wczytaj('wybuchbomby.wav')
        self.dzwieki['zabicie'] = wczytaj('zabicieprzeciwnika.wav')
        self.dzwieki['jazda'] = wczytaj('jechanie_czolgu.wav')
        self.dzwieki['wygrana'] = wczytaj('wygranielevelu.mp3')
        self.dzwieki['wybor'] = wczytaj('menu.wav')
        self.dzwieki['metal'] = wczytaj('strzal_w_metal.ogg')
        self.dzwieki['obramowanie'] = wczytaj('strzal_w_obramowanie.ogg')

    #Metoda ktora odtwarza dzwieki o podanej nazwie
    def play_sound(self, nazwa, loops=0):
        if nazwa in self.dzwieki and self.dzwieki[nazwa]:
            self.dzwieki[nazwa].play(loops=loops)

    #Metoda zatrzymuje odtwarzanie dzwieku
    def stop_sound(self, nazwa):
        if nazwa in self.dzwieki and self.dzwieki[nazwa]:
            self.dzwieki[nazwa].stop()