import pygame as pg
import math
import numpy as np
import random
from Dot_settings import *



class Sirkel_player:
    def __init__(self, x, y, r, color):
        pg.mixer.init()
        self.x = x
        self.y = y
        
        self.r = r
        self.color = color
        
        self.score = 0
        
        # Hastighet/fart
        self.speed = 5
        self.vx = 0
        self.vy = 0
        self.active = True
        
        self.spis_lyd = pg.mixer.Sound(spiselyd)

    
    # Metode som tegner figuren
    def draw(self, overflate):
        if self.active:
            center = (self.x, self.y)
            pg.draw.circle(overflate, self.color, center, self.r)
    

    # Metode som håndterer tastaturinput
    def move(self):
        v = 5 #fart
        # henter tastene fra tastaturet som trykkes
        keys = pg.key.get_pressed()
        if self.color == RED:
            # sjekker om venstre-pil er trykket på
            if keys[pg.K_LEFT]:
                self.x -= v
                
            # sjekker om høyre-pil er trykket på
            if keys[pg.K_RIGHT]:
                self.x += v
                
            # sjekker om opp-pil er trykket på
            if keys[pg.K_UP]:
                self.y -= v
            
            # sjekker om ned-pil er trykket på
            if keys[pg.K_DOWN]:
                self.y += v
                
        if self.color == GREEN:
            # sjekker om venstre-pil er trykket på
            if keys[pg.K_a]:
                self.x -= v
                
            # sjekker om høyre-pil er trykket på
            if keys[pg.K_d]:
                self.x += v
                
            # sjekker om opp-pil er trykket på
            if keys[pg.K_w]:
                self.y -= v
            
            # sjekker om ned-pil er trykket på
            if keys[pg.K_s]:
                self.y += v
            
    
    def kollisjon(self, sprett_list):
        
        # Kollisjon mot høyre
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            
        # Kollisjon mot venstre
        if self.x - self.r < 0:
            self.x = 0 + self.r
            
        # Kollisjon oppover
        if self.y - self.r < 0:
            self.y = 0 + self.r
            
        # Kollisjon nedover
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
    
        for b in sprett_list:
            if b.active:
                if self.sprett_kollisjon(b):
                    return True
        return False
                
            
    def sprett_kollisjon(self, b):
        # Pytagoras
        koll_avstand = math.sqrt((self.x - b.x)**2 + (self.y - b.y)**2)
        
        # de blå sirklene
        if b.color == BLUE:
            if koll_avstand <= abs(self.r + b.r):
                print ("Game over")
                return True
        
        # de svarte sirklene
        if b.color == BLACK:
            if self.color == RED:
                if koll_avstand <= abs(self.r + b.r):
                    b.active = False
                    self.score += 1
                    self.spis_lyd.play()

                    
            if self.color == GREEN:
                if koll_avstand <= abs(self.r + b.r):
                    b.active = False
                    self.score += 1
                    self.spis_lyd.play()
    
        return False
    
    def er_det_kollisjon(self, b):
         # Pytagoras
        koll_avstand = math.sqrt((self.x - b.x)**2 + (self.y - b.y)**2)
        if koll_avstand <= abs(self.r + b.r):
            return True
        return False
    
    def endre_fartsretning(self, k):
        n = np.array([self.x - k.x, self.y - k.y]) # vektor n
        lengde_n = math.sqrt(n[0]**2 + n[1]**2) #lengde av vektor n
        n = n/lengde_n
        
        v = np.array([self.vx, self.vy]) # v vektor
        
        u = np.inner(n, v) * n # u vektor
        w = v - 2*u # w vektor
        
        # ny fartsretning
        self.vx = w[0] 
        self.vy = w[1]


    
class Sirkel_sprett(Sirkel_player):
    def __init__(self, x, y, r, color):
        super().__init__(x, y, r, color)
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = 4*random.random();
        self.vy = 4*random.random();
        
        
        print(self.x, self.y)
        
    def move(self):
        # Oppdaterer posisjonen fra farten
        self.x += self.vx
        self.y += self.vy
        
        # Sjekker kollisjon med høyre vegg
        if self.x + self.r >= WIDTH:
            self.vx *= -1
            self.x = WIDTH - self.r
            
        # Sjekker kollisjon med venstre vegg
        if self.x - self.r <= 0:
            self.vx *= -1
            self.x = self.r
            
        # Sjekker kollisjon med topp
        if self.y - self.r <= 0:
            self.vy *= -1
            self.y = self.r
            
        # Sjekker kollisjon med bunn
        if self.y + self.r >= HEIGHT:
            self.vy *= -1
            self.y = HEIGHT - self.r
            