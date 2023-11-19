#Librerias
import pygame
from pygame.locals import *
import random 
import time 
#Codigo usado pyinstaller --onefile --noconsole brack.py
#Para el ejecutable se instalo 
#pyinstaller
#Colores
color=(144, 16, 144)
#Pantalla
pygame.init()
screen= pygame.display.set_mode([1280,720])
fondodepantalla= pygame.image.load('./pixel.jpg').convert()
fuente = pygame.font.Font(None, 60)
fuente2 = pygame.font.Font(None, 30)
fuente3 = pygame.font.Font(None, 20)
#Posicion
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
sphere_start = (650, 250)
sphere_speed = (3.0, 3.0)
sx, sy = sphere_speed
sphere_served = False
sphere_rect.topleft = sphere_start

# La plataforma 
pad = pygame.image.load('./plataforma.png')
pad = pad.convert_alpha()
pad_rect = pad.get_rect()
pad_rect[1] = screen.get_height() - 150

clock = pygame.time.Clock()
game_over = False
#///////////////
if sphere_rect[1] >= screen.get_height() - sphere_rect.height:
        sphere_served = False
        sphere_rect.topleft = sphere_start
#/////////
tiempo = 0
time= 0
#Tiempo

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
    #Posicion de vidas
    Vida1=(10,630)
    Vida2=(70,630)
    Vida3=(130,630)
    global Vidamenos
    Vidamenos=0
    #Logica de sprites
    
    #Texto en si
    text = "Pulsa espacio para jugar"
    mensaje = fuente.render(text, 1, (color))
    screen.blit(mensaje, (Posicionx, Posiciony))
    Hecho = "Hecho por Mateo Bv"
    hecho2 = fuente2.render(Hecho, 1, (255,255,255))
    screen.blit(hecho2, (1060, 600))
    Version = "V.1.O.Beta"
    Version2 = fuente3.render(Version, 1, (255,255,255))
    screen.blit(Version2, (1060, 630))
    texto = "Fin del juego ganaste"
    Fin_del_game_papa = fuente.render(texto, 1, (color))
    #Cerrar juego 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
#FIN DEL BUCLE PRINCIPAL
#LOGICA DEL JUEGO 
    #Movimientos del jugador.
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        x -= 0.4 * dt
    if pressed[K_RIGHT]:
        x += 0.4 * dt
    if pressed[K_SPACE]:
        sphere_served = True
    # "colision" de plataforma con la esfera
    if pad_rect[0] + pad_rect.width >= sphere_rect[0] >= pad_rect[0] and \
            sphere_rect[1] + sphere_rect.height >= pad_rect[1] and sy > 0:
        sy *= -1
        # Incrementar dificultad "Aumentar la velocidad de la pelota "
        #sy *= 1.1
        #sx *= 1.1
        continue

    delete_brick = None
   
    for b in bricks:
        bx, by = b
        Primeravida=0
        # Destruir Ladrillos por colision de la pelota 
        if bx <= sphere_rect[0] <= bx + brick_rect.width and \
                by <= sphere_rect[1] <= by + brick_rect.height:
            delete_brick = b

            if sphere_rect[0] <= bx + 2:
                sx *= -1
                
            elif sphere_rect[0] >= bx + brick_rect.width - 2:
                sx *= -1
                
            if sphere_rect[1] <= by + 2:
                sy *= -1
                
            elif sphere_rect[1] >= bx + brick_rect.height - 2:
                sy *= -1
            
            break

    if bx <= sphere_rect[0] <= bx + brick_rect.width and \
                by <= sphere_rect[1] <= by + brick_rect.height:
            delete_brick = b
            
    if delete_brick is not None:
        bricks.remove(delete_brick)
        
    # Limite de arriba
    if sphere_rect[1] <= 0:
        sphere_rect[1] = 0
        sy *= -1
        
    # Limite de abajo
    if sphere_rect[1] >= screen.get_height() - sphere_rect.height:
        sphere_served = False
        sphere_rect.topleft = sphere_start
        Primeravida += 1
    
    # Limite derecho
    if sphere_rect[0] <= 0:
        sphere_rect[0] = 0
        sx *= -1

    # Limite izquierdo
    if sphere_rect[0] >= screen.get_width() - sphere_rect.width:
        sphere_rect[0] = screen.get_width() - sphere_rect.width
        sx *= -1

    pad_rect[0] = x
    if sphere_served:
        # movi sphere
        sphere_rect[0] += sx
        sphere_rect[1] += sy
    #Fin del juego
    #if Primeravida == 1:
       #Vida3=(-400,-400)
    #if Primeravida== 2:
        # Vida2=(-400,-400)
    #if Primeravida == 3:
        # Vida1=(-400,-400)
    
    #Vida = pygame.image.load('./Vidas.png')
    #screen.blit(Vida, Vida1)
    #screen.blit(Vida, Vida2)
    #screen.blit(Vida, Vida3)
   
    #screen.blit(Fin_del_game_papa, (390, 350))
    
    #escribircontador=str(contadoralp)
    #contador2 = fuente2.render(escribircontador, 1, (255,255,255))
    #screen.blit(contador2, (200, 600))
    #print(contador2)

    pygame.display.update()
pygame.quit()