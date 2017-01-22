#!/usr/bin/python

import pygame

def cargar_imagen(ruta):
	imagen = pygame.image.load(ruta)
	return imagen
	
class Bombero(pygame.sprite.Sprite):
	def __init__(self,inicioX,inicioY,listaparedes):
		pygame.sprite.Sprite.__init__(self)
		self.dt_animacion = 7
		self.rango = [3]
		self.imagenes = []
		self.imagenes.append(cargar_imagen("imagenes/bombero1l.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero2l.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero3l.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero1u.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero2u.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero3u.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero1r.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero2r.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero3r.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero1d.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero2d.png"))
		self.imagenes.append(cargar_imagen("imagenes/bombero3d.png"))
		self.index = 0
		self.image = self.imagenes[self.rango[0]]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = inicioX, inicioY
		self.listap = listaparedes
		self.time = 5
		
	def dibujar(self,ventana):
		ventana.blit(self.image,(self.rect.x,self.rect.y))
		
	def actualizar(self,paredes):
		self.listap = paredes
		self.dt_animacion -= 1
		if (self.dt_animacion == 0):
			self.dt_animacion = 7
			self.index += 1
			if self.index >= len(self.rango):
				self.index = 0
			self.image = self.imagenes[self.rango[self.index]]

	def quieto(self):
		self.rango = [3]

	def mover(self,dx,dy):
		if dx == 0 and dy == 0:
			self.rango = [3]
		if dx < 0:
			self.rango = [0,1,2]
		if dx > 0:
			self.rango = [6,7,8]
		if dy < 0:
			self.rango = [3,4,5]
		if dy > 0:
			self.rango = [9,10,11]
		self.rect.x = self.rect.x + dx
		self.rect.y = self.rect.y + dy
		for p in self.listap:
			if pygame.sprite.collide_rect(self,p):
				if dx > 0:
					self.rect.right = p.rect.left
				if dx < 0:
					self.rect.left = p.rect.right
				if dy > 0:
					self.rect.bottom = p.rect.top
				if dy < 0:
					self.rect.top = p.rect.bottom
			

	def get_pos(self):
		return (self.rect.x,self.rect.y)
	
	def calcular_distancia(self, persona):
		return (self.rect.x-persona.rect.x, self.rect.y-persona.rect.y)
		
	def reset(self,x,y):
		self.rect.x = x
		self.rect.y = y
