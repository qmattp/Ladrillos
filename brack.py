#Librerias
import pygame
from pygame.locals import *

#Colores
color=(144, 16, 144)
#Pantalla
pygame.init()
screen= pygame.display.set_mode([1280,720])
fondodepantalla= pygame.image.load('./pixel.jpg').convert()
fuente = pygame.font.Font(None, 60)
fuente2 = pygame.font.Font(None, 30)
fuente3 = pygame.font.Font(None, 20)
#Posiion
Posicionx=390
Posiciony=350
#Escritura
WIDTH = 1280
HEIGHT = 720
#Nombre del juego
pygame.display.set_caption("Rompe Nubes")

#Musica 8bits
pygame.mixer.music.load("./8bit.wav")
pygame.mixer.music.play()

# Ladrillos
brick = pygame.image.load('./Ladrillo.png')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()

# coordenada x,y , ancho y altura
bricks = []
Numero_nubes = 6
# gap =>brecha
brick_gap = 10
# r= 7 //3 =>2
brick_cols = screen.get_width() // (brick_rect[2] + brick_gap)
# lado del brecha
side_gap = (screen.get_width() - (brick_rect[2] + brick_gap) * brick_cols + brick_gap) // 2

for y in range(Numero_nubes):
    brickY = y * (brick_rect[3] + brick_gap)
    for x in range(brick_cols):
        brickX = x * (brick_rect[2] + brick_gap) + side_gap
        bricks.append((brickX, brickY))

# Pelota
sphere = pygame.image.load('./estrella.png')
sphere = sphere.convert_alpha()
sphere_rect = sphere.get_rect()
sphere_start = (350, 250)
sphere_speed = (3.0, 3.0)
sx, sy = sphere_speed
sphere_served = False
sphere_rect.topleft = sphere_start

# La plataforma 
pad = pygame.image.load('./plataforma.png')
pad = pad.convert_alpha()
pad_rect = pad.get_rect()
pad_rect[1] = screen.get_height() - 100

clock = pygame.time.Clock()
game_over = False
#///////////////

#INICIO DEL BUCLE PRINCIPAL
while not game_over:
    dt = clock.tick(80)
    screen.blit(fondodepantalla, [0,0])
    # Dibuja las nubes
    for br in bricks:
        screen.blit(brick, br)

    # Dibujar plataforma
    screen.blit(pad, pad_rect)

    # Dibujar luna o pelta (Como le quieras decir)
    screen.blit(sphere, sphere_rect)
    #Texto
    pressed = pygame.key.get_pressed()
    if pressed[K_SPACE]:
        Posicionx=-40
        Posiciony=-40
    
    #Texto
    text = "Pulsa espacio para jugar"
    mensaje = fuente.render(text, 1, (color))
    screen.blit(mensaje, (Posicionx, Posiciony))
    Hecho = "Hecho por Mateo Bv"
    hecho2 = fuente2.render(Hecho, 1, (255,255,255))
    screen.blit(hecho2, (1060, 600))
    Version = "V.1.O.Beta"
    Version2 = fuente3.render(Version, 1, (255,255,255))
    screen.blit(Version2, (1060, 630))
    #Cerrar juego 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

#FIN DEL BUCLE PRINCIPAL
#LOGICA DEL JUEGO 
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        x -= 0.4 * dt
    if pressed[K_RIGHT]:
        x += 0.4 * dt
    if pressed[K_SPACE]:
        sphere_served = True
    # "colision" de paleta con la esfera
    if pad_rect[0] + pad_rect.width >= sphere_rect[0] >= pad_rect[0] and \
            sphere_rect[1] + sphere_rect.height >= pad_rect[1] and sy > 0:
        sy *= -1
        # Incrementar dificultad
        sy *= 1.1
        sx *= 1.1
        continue

    delete_brick = None

    for b in bricks:
        bx, by = b
        # Destruir Ladrillos por colision de nuestra esfera
        if bx <= sphere_rect[0] <= bx + brick_rect.width and \
                by <= sphere_rect[1] <= by + brick_rect.height:
            delete_brick = b

            if sphere_rect[0] <= bx + 2:
                sx *= -1
                contador =+ 1
            elif sphere_rect[0] >= bx + brick_rect.width - 2:
                sx *= -1
            if sphere_rect[1] <= by + 2:
                sy *= -1
            elif sphere_rect[1] >= bx + brick_rect.height - 2:
                sy *= -1
            break

    if delete_brick is not None:
        bricks.remove(delete_brick)

    # Top
    if sphere_rect[1] <= 0:
        sphere_rect[1] = 0
        sy *= -1

    # Bottom
    if sphere_rect[1] >= screen.get_height() - sphere_rect.height:
        # sphere_rect[1] = screen.get_height() - sphere_rect.height
        # sy *= -1
        # resetear juego
        sphere_served = False
        sphere_rect.topleft = sphere_start

    # Left
    if sphere_rect[0] <= 0:
        sphere_rect[0] = 0
        sx *= -1

    # Right
    if sphere_rect[0] >= screen.get_width() - sphere_rect.width:
        sphere_rect[0] = screen.get_width() - sphere_rect.width
        sx *= -1

    pad_rect[0] = x
    if sphere_served:
        # movi sphere
        sphere_rect[0] += sx
        sphere_rect[1] += sy

    pygame.display.update()
pygame.quit()