#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygame, sys, os, math
from modulos.colors import *
from modulos.bomber import *
from modulos.paredes import *
from modulos.levels import *
from modulos.victim import *

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
medidas_pantalla = (1024,700)

ventana = pygame.display.set_mode(medidas_pantalla)
pygame.display.set_caption("game")
reloj = pygame.time.Clock()

#flecha menu
posX, posY = 750,390
flecha_imagen = pygame.image.load("imagenes/sprite.png").convert_alpha()
seno = 0

cond_menu = True
cond_jugar = True
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
			if posY == 390:
				cond_menu = False
			else:
				pygame.quit()
				sys.exit()	
	key = pygame.key.get_pressed()
	if key[pygame.K_UP]:
		posY = 390
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


# movimiento bombero
dx, dy = 0,0
# animaciones
anim_linterna = 10
change_linterna = True
humo = pygame.image.load("imagenes/humo.png").convert_alpha()
luz_bombero = pygame.image.load("imagenes/linterna.png")
anim_humo = 0

bool_humo = True
background_game = pygame.image.load("imagenes/background_game.png").convert()
hud = pygame.image.load("imagenes/hud.png").convert()
paredes = []

# Convierte en objetos el nivel. W = wall
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
    
# inicializamos personajes
bombero = Bombero(300,300,paredes)
#cambiarlo a rescates (ojo con el sonido)
victima = Victima(paredes)

# start playing the sound and remember on which channel it is being played
sonido_grito = pygame.mixer.Sound("sonidos/wind1.wav")
channel = sonido_grito.play()

# correr
power_correr = 100

# juego loop -----------------------------------------------------------
while cond_jugar:
	#procesar eventos
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			cond_jugar = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			cond_jugar = False
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(-10,0)
			power_correr -= 7
		else:
			bombero.mover(-3,0)
	if key[pygame.K_RIGHT]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(10,0)
			power_correr -= 7
		else:
			bombero.mover(3,0)
	if key[pygame.K_UP]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(0,-10)
			power_correr -= 7
		else:
			bombero.mover(0,-3)
	if key[pygame.K_DOWN]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(0,10)
			power_correr -= 7
		else:
			bombero.mover(0,3)
		
	filtro = pygame.surface.Surface((1024,700))
	
	#actualizar
	reloj.tick(60)
	bombero.actualizar()
	
	# variable que guarda la distancia entre el bombero y quien tiene que rescatar
	# devuelve (x, y)
	distancia_persona = bombero.calcular_distancia(victima);
	esta_cerca = abs(distancia_persona[0]) + abs(distancia_persona[1])
	# modificacion del sonido segun distancia
	if (distancia_persona[0] < -150):
		#solamente se escucha por el canal izquierdo
		channel.set_volume(1, 0)
	elif (distancia_persona[0] > 150):
		#solamente se escucha por el canal derecho
		channel.set_volume(0, 1)
	else:
		#solamente se escucha por los dos canales
		channel.set_volume(1, 1)
	if (esta_cerca > 1500):
		sonido_grito.set_volume(0.1)
	elif (esta_cerca > 1250 and esta_cerca < 1500):
		sonido_grito.set_volume(0.3)
	elif (esta_cerca > 1000 and esta_cerca < 1250):
		sonido_grito.set_volume(0.5)
	elif (esta_cerca > 750 and esta_cerca < 1000):
		sonido_grito.set_volume(0.6)
	elif (esta_cerca > 500 and esta_cerca < 750 ):
		sonido_grito.set_volume(0.7)
	elif (esta_cerca > 250 and esta_cerca < 500):
		sonido_grito.set_volume(0.8)
	else:
		sonido_grito.set_volume(0.9)

	# Animacion de la luz del bombero
	anim_linterna -= 1
	if anim_linterna < 0:
		anim_linterna = 10
		change_linterna = not change_linterna
	if change_linterna:
		luz_bombero = pygame.image.load("imagenes/linterna2.png")
	else:
		luz_bombero = pygame.image.load("imagenes/linterna.png")
	
	# Animacion humo sobre la pantalla
	if bool_humo:
		anim_humo -= 1
	else:
		anim_humo += 1
	if anim_humo == -500:
		bool_humo = False
		anim_humo = -499
	if anim_humo == 0:
		bool_humo = True
		anim_humo = -10
	
	if power_correr < 100:
		power_correr += 0.5
	
	# DIBUJAR
	ventana.blit(background_game,(0,0))
	for p in paredes:
		p.dibujar(ventana)
	bombero.dibujar(ventana)
	victima.dibujar(ventana)
	filtro.fill((255,255,255))
	filtro.blit(luz_bombero,map(lambda x: x-120,bombero.get_pos()))
	ventana.blit(filtro,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
	#ventana.blit(humo,(anim_humo,0))
	ventana.blit(hud,(0,665))


	
	pygame.display.flip()
