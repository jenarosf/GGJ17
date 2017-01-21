#!/usr/bin/python

import pygame

class Pared(pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		self.imagen = pygame.image.load("imagenes/pared.png").convert()
		self.x = pos[0]
		self.y = pos[1]
	
	def dibujar(self,ventana):
		ventana.blit(self.imagen,(self.x,self.y))
