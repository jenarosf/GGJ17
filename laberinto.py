#!/usr/bin/python
#-*- coding:utf-8 -*-


import os
import random
import pygame
# -------------------------------------------------------
# PERSONAJE
class Player(object):
    # CONSTRUCTOR, lo crea como un cuadrado
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 32, 32)
    # Funcion wrapper para mover el personaje
    def move(self, dx, dy):
        if dx != 0:
            # si se mueve solo en x, a la funcion de movimiento no le manda un valor para y
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    # mueve y revisa colision
    def move_single_axis(self, dx, dy):
        # Movemos el personaje
        self.rect.x += dx
        self.rect.y += dy
        # Si colisionamos con un muro
        # ¡¡¡¡REVISAR!!!!
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
# end class
# -------------------------------------------------------

# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        # agrega la instancia en la lista de paredes
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
# end class
# -------------------------------------------------------

# Inicializamos el juego
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Seteamos el display
pygame.display.set_caption("Llega al cuadrado rojo!")
screen = pygame.display.set_mode((1024, 700))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
"W--------WWWWWWWWWWWWWWWWWWWWWW",
"W--------W-------W----W-------W",
"W--------W-------W----W-------W",
"W--------W-------W----W-------W",
"W--------W-------W----W-------W",
"W--------W-------W----W-------W",
"W--------W-------W------------W",
"W--------WWWWWW--W------------W",
"W                W    WWWWWWWWW",
"W-----------------------------W",
"W-----------------------------W",
"W--------WWWW--WWWWW--W-------W",
"W--------W-----W------W-------W",
"W--------W-----W------W-------W",
"W--------W-----W------W-------W",
"W--------W-----W------W-------W",
"W--WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W------------------------------",
"W------------------------------",
"W--W--------W------------------",
"---WWWWWWWWWWWWWWW------------E",

]

# Convierte en objetos el nivel de arriba. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)
        x += 32
    y += 32
    x = 0

# LOOP
running = True
while running:

    # fps
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Movimiento del personaje
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Si llega al cuadrado, sale de sistema con un mensaje de ganaste
    if player.rect.colliderect(end_rect):
        raise SystemExit, "You win!"

    # Dibuja la escena
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()

# end loop
