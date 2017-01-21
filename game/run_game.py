#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygame, sys, os, math
from modulos.colors import *
from modulos.bomber import *
from modulos.paredes import *
from modulos.levels import *

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
medidas_pantalla = (1024,700)

ventana = pygame.display.set_mode(medidas_pantalla)
pygame.display.set_caption("game")
reloj = pygame.time.Clock()

cond_menu = True
cond_jugar = True

#flecha menu
posX, posY = 200,450
flecha_imagen = pygame.image.load("imagenes/sprite.png").convert_alpha()
seno = 0
background_menu = pygame.image.load("imagenes/background_menu.png")



# menu loop ----------------------------------------------------------
while cond_menu:
	#procesar eventos
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
			if posY == 450:
				cond_menu = False
			else:
				pygame.quit()
				sys.exit()
		
	key = pygame.key.get_pressed()
	if key[pygame.K_UP]:
		posY = 450
	if key[pygame.K_DOWN]:
		posY = 550
			
	#actualizar
	reloj.tick(60)
	seno += 0.1
	#dibujar
	ventana.blit(background_menu,(0,0))
	ventana.blit(flecha_imagen,(posX,int(posY+math.degrees(math.sin(seno)) / 2 )) )
	pygame.display.update()
# end menu loop --------------------------------------------------------


dx, dy = 0,0
luz_bombero = pygame.image.load("imagenes/linterna.png")
background_game = pygame.image.load("imagenes/background_game.png").convert()
paredes = []


# Convierte en objetos el nivel de arriba. W = wall, E = exit
x = y = 0
for row in level1:
    for col in row:
        if col == "W":
            pp = Pared((x, y))
            paredes.append(pp)
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)
        x += 32
    y += 32
    x = 0

bombero = Bombero(300,300,paredes)

# juego loop -----------------------------------------------------------
while cond_jugar:
	filtro = pygame.surface.Surface((1024,700))

	#procesar eventos
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			cond_jugar = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			cond_jugar = False
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		bombero.mover(-3,0)
	if key[pygame.K_RIGHT]:
		bombero.mover(3,0)
	if key[pygame.K_UP]:
		bombero.mover(0,-3)
	if key[pygame.K_DOWN]:
		bombero.mover(0,3)
		

	#actualizar
	reloj.tick(60)
	bombero.actualizar()
	#dibujar
	ventana.blit(background_game,(0,0))
	for p in paredes:
		p.dibujar(ventana)
	filtro.fill(blanco)
	filtro.blit(luz_bombero,map(lambda x: x-120,bombero.get_pos()))
	ventana.blit(filtro,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
	bombero.dibujar(ventana)

	
	pygame.display.flip()
