import pygame as pg
import sys
import math
import random
from Dot_circle import *
from Dot_settings import *

class Game:
    def __init__(self):
        print("__init__")
        pg.init() # initierer pygame
        pg.mixer.init()
        self.overflate = pg.display.set_mode(SIZE) # Lager en overflate (surface) vi kan tegne på
        pg.display.set_caption('IT-prosjekt') # Tittel
        self.clock = pg.time.Clock() # Lager en klokke
        self.font = pg.font.SysFont('Arial', 20) # henter font
        self.running = True
        self.gameOver = False
        
        # Henter inn bakgrunnsbilde
        self.backgroundImg = pg.image.load(bakgrunn)
        
        # skalerer bildet
        self.backgroundImg = pg.transform.scale(self.backgroundImg, SIZE)
        
        # lyd
        self.lyd = pg.mixer.Sound(bakgrunnslyd)
        
        # Spillere
        sirkel1 = Sirkel_player(50, 50, 10, RED)
        sirkel2 = Sirkel_player(300, 300, 10, GREEN)
        self.player_list = [sirkel1, sirkel2]
        
        
        self.spiselig = []
        self.uspiselig = []

        for i in range(1):
            a = Sirkel_sprett(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), 10, BLUE)
            self.uspiselig.append(a)

        for i in range(50):
            b = Sirkel_sprett(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), random.randint(10,10), BLACK)
            self.spiselig.append(b)
        
    def move(self):
        for player in self.player_list:
            player.move()
        
        for prikk in self.spiselig:
            prikk.move()
      
        for prikk in self.uspiselig:
            prikk.move()
            
    def draw(self):
        for player in self.player_list:
            player.draw(self.overflate)
        
        for prikk in self.spiselig:
            prikk.draw(self.overflate)
            
        for prikk in self.uspiselig:
            prikk.draw(self.overflate)
    
    def sjekk_kollisjoner(self):
#        return False # True if Game Over
        for player in self.player_list:
            self.gameOver = self.gameOver or player.kollisjon(self.uspiselig) #returnerer enten false eller true, velger halst at game over er true (velger game over hvis game over = true
            player.kollisjon(self.spiselig)
   
                
        alle = self.spiselig
       
        for i in range(len(alle)):
            for j in range(len(alle)):
                if i!=j and i<j: # sjekker ikke like 
                    ki = alle[i] # kule i
                    kj = alle[j] # kule j
                    if ki.active and kj.active and ki.er_det_kollisjon(kj):
                        #gjennomsnittshastighet
                        vx = 0.5*(ki.vx+kj.vx)
                        vy = 0.5*(ki.vy+kj.vy)
                        
                        #trekk fra gjennomsnittshastighet
                        ki.vx = ki.vx-vx
                        ki.vy = ki.vy-vy
                        
                        kj.vx = kj.vx-vx
                        kj.vy = kj.vy-vy
                        
                        ki.endre_fartsretning(kj)
                        kj.endre_fartsretning(ki)
                                 
                        #legg til gjennomsnittshastighet
                        ki.vx = ki.vx+vx
                        ki.vy = ki.vy+vy
                        
                        kj.vx = kj.vx+vx
                        kj.vy = kj.vy+vy
                        
                    
    

    def run(self):
        
        # Løkken kjører i korrekt hastighet
        self.clock.tick(FPS)

        # Går gjennom hendelser (events)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                self.running = False # Spillet skal avslutte
        
        if not self.gameOver:
            self.overflate.blit(self.backgroundImg, (0,0)) 
            
            self.draw()
            self.move()
            self.sjekk_kollisjoner()
            
            self.tegnScore()
            pg.display.update()
        else:
            self.game_over()

        
        # Etter vi har tegner alt, "flipper" vi displayet
        pg.display.flip()

    
    # funksjon som tegner score til skjermen
    def tegnScore(self):
        
        player1 = self.player_list[0]
        player2 = self.player_list[1]
        
        score_red = self.font.render(f'Score:{player1.score}', True, BLACK) #tekst, alias, farge
        self.overflate.blit(score_red, (10, 20))
        
        score_green = self.font.render(f'Score:{player2.score}', True, BLACK) # Right = green
        
        # henter rektangelet fra tekstbildet
        score_green_rect = score_green.get_rect()
        self.overflate.blit(score_green, (WIDTH - score_green_rect.width - 10, 20))

    #funksjon som skriver tekst til vinnerne
    def tegnTekst(self, text, x, y, farge, fontSize):
        
        #henter font
        font = pg.font.SysFont('Arial', fontSize)
        
        # Lager et tekstbilde
        textImg = font.render(text, True, farge)
        
        # henter rektangelet til tekstboksen
        textRect = textImg.get_rect()
        
        # setter i vinduet
        self.overflate.blit(textImg, (x - textRect.width//2, y - textRect.height//2))
        
        
    def game_over(self):
        self.overflate.fill(BLACK)
        self.lyd.play()
            
        if self.player_list[0].score > self.player_list[1].score:
            self.tegnTekst(f"Rød vant med {self.player_list[0].score - self.player_list[1].score} poeng!", WIDTH//2, HEIGHT//2, self.player_list[0].color, 50)
        elif self.player_list[0].score < self.player_list[1].score:
            self.tegnTekst(f"Grønn vant med {self.player_list[1].score - self.player_list[0].score} poeng!", WIDTH//2, HEIGHT//2, self.player_list[1].color, 50)
        else:
            self.tegnTekst("Det ble uavgjort!", WIDTH//2, HEIGHT//2, WHITE, 50)
    
        

g = Game()

while g.running:
    g.run()
    
sys.exit()
    