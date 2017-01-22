#!/usr/bin/python

import pygame, random, time
from modulos.levels import *

def cargar_imagen(ruta):
	imagen = pygame.image.load(ruta).convert_alpha()
	return imagen

class Victima(pygame.sprite.Sprite):
    def __init__(self,listaparedes):
    	pygame.sprite.Sprite.__init__(self)
    	random.seed(time.time())
    	self.listap = listaparedes

    	self.dt_animacion = 15
    	self.imagenes = []
    	self.imagenes.append(cargar_imagen("imagenes/bombero1u.png"))
    	self.index = 0
    	self.image = self.imagenes[self.index]
    	self.rect = self.image.get_rect()

    	# generar coordenadas aleatorias
    	x = random.randint(0, 950)
    	y = random.randint(0, 660)
        x32 = x / 32
        y32 = y / 32
        while level1[y32][x32] == "W":
            x = random.randint(0, 950)
            y = random.randint(0, 660)
            x32 = x / 32
            y32 = y / 32
        self.rect.x = x
        self.rect.y = y

    def dibujar(self,ventana):
    	ventana.blit(self.image,(self.rect.x,self.rect.y))

    def actualizar(self):
    	self.dt_animacion -= 1
    	if (self.dt_animacion == 0):
    		self.dt_animacion = 15
    		self.index += 1
    		if self.index >= len(self.imagenes):
    			self.index = 0
    		self.image = self.imagenes[self.index]

    def get_pos(self):
    	return (self.rect.x,self.rect.y)
