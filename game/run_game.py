#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygame, sys, os, math
from modulos.colors import *
from modulos.bomber import *
from modulos.paredes import *
from modulos.levels import *
from modulos.victim import *
from modulos.ondas import *
from pygame.locals import *

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
medidas_pantalla = (1024,700)

ventana = pygame.display.set_mode(medidas_pantalla)
pygame.display.set_caption("WAVES STATION")
reloj = pygame.time.Clock()

#flecha menu
posX, posY = 750,390
flecha_imagen = pygame.image.load("imagenes/sprite.png").convert_alpha()
seno = 0

cond_menu = True
cond_jugar = True
finjuego = True
background_menu = pygame.image.load("imagenes/background_menu.png")

#musica menu
pygame.mixer.music.load("sonidos/menu.mp3")
pygame.mixer.music.play(-1,1)
sonidoItem = pygame.mixer.Sound("sonidos/item.wav")
sonidoItem.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)

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
		if not posY == 390:
			sonidoItem.play()
		posY = 390
	if key[pygame.K_DOWN]:
		if not posY == 550:
			sonidoItem.play()
		posY = 550
			
	#actualizar
	reloj.tick(60)
	seno += 0.1
	#dibujar
	ventana.blit(background_menu,(0,0))
	ventana.blit(flecha_imagen,(posX,int(posY+math.degrees(math.sin(seno)) / 2 )) )
	pygame.display.update()
# end menu loop --------------------------------------------------------

cond_instrucciones = True
inst = pygame.image.load("imagenes/instrucciones.png").convert()

while cond_instrucciones:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
		if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
			cond_instrucciones = False
		
		ventana.blit(inst,(0,0))
		pygame.display.update()
			
		

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
        x += 32
    y += 32
    x = 0

bombero_iniciox,bombero_inicioy = 32*2,32*20
# inicializamos personajes
bombero = Bombero(bombero_iniciox,bombero_inicioy,paredes)
victima = Victima(paredes,1)
ondas = Ondas(victima.get_pos())
ver_ondas = False
tiempo_ondas = 750
power_correr = 100

# cantidad de victimas rescatadas
rescates = 0
level = 1

pygame.mixer.music.stop()

pygame.mixer.music.load("sonidos/juego.ogg")
pygame.mixer.music.play(-1,1)
pygame.mixer.music.set_volume(0.01)

sonidoLogro = pygame.mixer.Sound("sonidos/victima.wav")
sonidoLogro.set_volume(0.05)

sonido_grito = pygame.mixer.Sound("sonidos/latidos.ogg")
channel = sonido_grito.play(-1)

rescatados = []
puntaje = pygame.image.load("imagenes/victima1.png")

contador = 60

#texto
fuente = pygame.font.Font("fuente/fuente.ttf", 22)
run = fuente.render("RUN", 2, cyan)
bool_gameover = True

tiempo_loco = pygame.time.get_ticks()/ 1000
# juego loop -----------------------------------------------------------
while cond_jugar:
	tiempo = (pygame.time.get_ticks() / 1000) - tiempo_loco
	#procesar eventos
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			cond_jugar = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			cond_jugar = False
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(-11,0)
			power_correr -= 7
		else:
			bombero.mover(-3,0)
	if key[pygame.K_RIGHT]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(11,0)
			power_correr -= 7
		else:
			bombero.mover(3,0)
	if key[pygame.K_UP]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(0,-11)
			power_correr -= 7
		else:
			bombero.mover(0,-3)
	if key[pygame.K_DOWN]:
		if key[pygame.K_SPACE] and power_correr > 0:
			bombero.mover(0,11)
			power_correr -= 7
		else:
			bombero.mover(0,3)
	if not key[pygame.K_UP] and not key[pygame.K_DOWN] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
		bombero.quieto()
	
	filtro = pygame.surface.Surface((1024,700))
	
	label = fuente.render(str(contador-tiempo), 2, (255,255,255))
	reloj.tick(60)
	bombero.actualizar(paredes)
	victima.actualizar()
	ondas.actualizar()
	tiempo_ondas -= 1
	if contador-tiempo == 0:
		cond_jugar = False
	
	if tiempo_ondas < 0:
		ver_ondas = True
	#chequear colisiones
	if pygame.sprite.collide_rect(bombero,victima):
		del victima
		victima = Victima(paredes,level)
		rescates += 1
		rescatados.append(puntaje)
		del ondas
		ondas = Ondas(victima.get_pos())
		ver_ondas = False
		tiempo_ondas = 700
		sonidoLogro.play()
	
	if rescates == 5:
		if level == 1:
			contador += 30
			rescatados = []
			level = 2 
			rescates = 0
			bombero.reset(bombero_iniciox,bombero_inicioy)
			x = y = 0
			for p in paredes:
				del p
			paredes = []
			for row in level2:
				for col in row:
					if col == "W":
						pp = Pared((x, y))
						paredes.append(pp)
					x += 32
				y += 32
				x = 0
		else:
			bool_gameover = False
			cond_jugar = False
	# variable que guarda la distancia entre el bombero y quien tiene que rescatar
	# devuelve (x, y)
	distancia_persona = bombero.calcular_distancia(victima);
	esta_cerca = abs(distancia_persona[0]) + abs(distancia_persona[1])
	# modificacion del sonido segun distancia
	if (distancia_persona[0] < -100):
		#solamente se escucha por el canal izquierdo
		channel.set_volume(0, 1)
	elif (distancia_persona[0] > 100):
		#solamente se escucha por el canal derecho
		channel.set_volume(1, 0)
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
	ondas.dibujar(ventana,ver_ondas)
	filtro.fill((255,255,255))
	filtro.blit(luz_bombero,map(lambda x: x-120,bombero.get_pos()))
	ventana.blit(filtro,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
	ventana.blit(humo,(anim_humo,0))
	ventana.blit(hud,(0,665))
	ventana.blit(label,(875,670))
	x, y = 32, 670
	if power_correr == 100:
		ventana.blit(run,(500,670))
	for p in rescatados:
		ventana.blit(p,(x,y))
		x += 40
	
	pygame.display.flip()
	
pygame.mixer.music.stop()


fuente2 = pygame.font.Font("fuente/fuente.ttf",55)
fuente3 = pygame.font.Font("fuente/fuente.ttf",25)
if bool_gameover:
	label = fuente2.render("GAMEOVER", 2, (30,30,30))
	label2 = fuente3.render("USA LAS ONDAS SONORAS", 2, (30,30,30))
else:
	label = fuente2.render("GANASTE", 2, (30,30,30))
	label2 = fuente3.render("   BOMBERO   BUENO",2,(30,30,30))

while finjuego:
	#procesar eventos
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			finjuego = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()
	fin = pygame.image.load("imagenes/pantallafinal.png")
  	ventana.blit(fin,(0,0))
	ventana.blit(label,(365,335))
	ventana.blit(label2,(365,450))
  	pygame.display.update()
	pygame.display.flip()	
