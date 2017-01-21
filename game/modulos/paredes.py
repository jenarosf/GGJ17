#!/usr/bin/python

import pygame

class Pared(pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("imagenes/pared.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
	
	def dibujar(self,ventana):
		ventana.blit(self.image,(self.rect.x,self.rect.y))
