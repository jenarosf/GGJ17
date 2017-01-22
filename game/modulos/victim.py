#!/usr/bin/python

import pygame, random, time
from modulos.levels import *

def cargar_imagen(ruta):
	imagen = pygame.image.load(ruta).convert_alpha()
	return imagen

class Victima(pygame.sprite.Sprite):
    def __init__(self,listaparedes,num):
    	pygame.sprite.Sprite.__init__(self)
    	random.seed(time.time())
    	self.listap = listaparedes
    	self.dt_animacion = 7
    	self.imagenes = []
    	self.imagenes.append(cargar_imagen("imagenes/victima1.png"))
	self.imagenes.append(cargar_imagen("imagenes/victima2.png"))
	self.imagenes.append(cargar_imagen("imagenes/victima3.png"))    	
	self.index = 0
    	self.image = self.imagenes[self.index]
    	self.rect = self.image.get_rect()
    	x = random.randint(0,30)
    	y = random.randint(0,20)
	if num == 1:
    		while level1[y][x] == "W":
			x = random.randint(0,30)
			y = random.randint(0,20)
	else:
		while level2[y][x] == "W":
			x = random.randint(0,30)
			y = random.randint(0,20)	
	self.rect.x = x*32
	self.rect.y = y*32
		
    def dibujar(self,ventana):
    	ventana.blit(self.image,(self.rect.x,self.rect.y))

    def actualizar(self):
    	self.dt_animacion -= 1
    	if self.dt_animacion == 0:
    		self.dt_animacion = 7
    		self.index += 1
    		if self.index >= len(self.imagenes):
    			self.index = 0
    		self.image = self.imagenes[self.index]
	print self.index

    def get_pos(self):
    	return (self.rect.x,self.rect.y)
