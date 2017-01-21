#!/usr/bin/python

import pygame

def cargar_imagen(ruta):
	imagen = pygame.image.load(ruta).convert_alpha()
	return imagen
	
class Bombero(pygame.sprite.Sprite):
	def __init__(self,inicioX,inicioY,listaparedes):
		pygame.sprite.Sprite.__init__(self)
		self.dt_animacion = 15
		self.imagenes = []
		self.imagenes.append(cargar_imagen("imagenes/bombero.png"))
		self.index = 0
		self.image = self.imagenes[self.index]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = inicioX, inicioY
		self.listap = listaparedes
		
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

	def mover(self,dx,dy):
		if not pygame.sprite.collide_rect(self,self.listap[1]):
			self.rect.x += dx
			self.rect.y += dy

	def get_pos(self):
		return (self.rect.x,self.rect.y)
