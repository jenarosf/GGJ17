#!/usr/bin/python

import pygame

class Ondas(pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		self.dt_animacion = 10
		self.imagenes = []
		self.imagenes.append(pygame.image.load("imagenes/onda1.png"))
		self.imagenes.append(pygame.image.load("imagenes/onda2.png"))
		self.imagenes.append(pygame.image.load("imagenes/onda3.png"))
		self.index = 0
		self.image = self.imagenes[self.index]
		self.x = pos[0] - 60
		self.y = pos[1] - 60
		
	def dibujar(self,ventana,b):
		if b:
			ventana.blit(self.image,(self.x,self.y))
		
	def actualizar(self):
    		self.dt_animacion -= 1
    		if self.dt_animacion == 0:
    			self.dt_animacion = 10
    			self.index += 1
    			if self.index >= len(self.imagenes):
    				self.index = 0
    			self.image = self.imagenes[self.index]
