#!/usr/bin/python

import pygame

class Pared(pygame.sprite.Sprite):
	def __init__(self,pos):
		paredes.append(self)
		self.rect = pygame.Rect(pos[0],pos[1],32,32)
