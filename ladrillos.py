import pygame
import sys
from pygame.locals import *

def generate_blocks():
    for row in range(rows):
        for col in range(columns):
            x = ((padding_left * col) + padding_left) + (block_width * col)
            y = ((padding_top * row) + padding_top) + (block_height * row)
            block = pygame.Rect(x,y,block_width,block_height)
            block_list.append(block)

def draw_blocks(blocks):
    for block in blocks:
        pygame.draw.rect(screen, COLOR, block)

def ball_animation():
    global ball_y_change, ball_x_change, lose_time, score
    ball.x += ball_x_change
    ball.y += ball_y_change

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_x_change = - ball_x_change

    if ball.top <= 0:
        ball_y_change = - ball_y_change

    if ball.bottom >= HEIGHT:
        lose_time = pygame.time.get_ticks()

    if ball.colliderect(paddle):
        ball_y_change = - ball_y_change

    for block in block_list:
        if ball.colliderect(block):
            ball_y_change = - ball_y_change
            block_list.remove(block)
            score += 1

def reset():
    global ball_x_change, ball_y_change, lose_time, score
    ball.x = WIDTH//2-10
    ball.y = HEIGHT-40
    paddle.x = WIDTH//2-150//2
    paddle.y = HEIGHT-20
    block_list.clear()
    generate_blocks()
    score = 0
    

    current_time = pygame.time.get_ticks()

    if current_time - lose_time < 1000:
        num_three = timer_font.render("3", True, COLOR)
        num_three_rect = num_three.get_rect(center=(WIDTH//2, HEIGHT//2+10))
        screen.blit(num_three, num_three_rect)

    elif 1000 < current_time - lose_time < 2000:
        num_two = timer_font.render("2", True, COLOR)
        num_two_rect = num_two.get_rect(center=(WIDTH//2, HEIGHT//2+10))
        screen.blit(num_two, num_two_rect)

    elif 2000 <current_time - lose_time < 3000:
        num_one = timer_font.render("1", True, COLOR)
        num_one_rect = num_one.get_rect(center=(WIDTH//2, HEIGHT//2+10))
        screen.blit(num_one, num_one_rect)

    if current_time - lose_time >= 3000:
        ball_x_change = - ball_x_change
        ball_y_change = - ball_y_change
        lose_time = None

def draw_score():
    score_text = score_font.render(f"{score}",True,COLOR)
    score_rect = score_text.get_rect(center= (20,HEIGHT-20))
    screen.blit(score_text, score_rect)

def win():
    if len(block_list) == 0:
        screen.fill(BG_COLOR)
        ball_y_change, ball_x_change = 0,0
        won_text = timer_font.render("You won !!",True,COLOR)
        won_rect = won_text.get_rect(center = (WIDTH//2, HEIGHT//2))
        screen.blit(won_text, won_rect)

pygame.init()
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Breakout")
clock = pygame.time.Clock()

BG_COLOR = pygame.Color("#2b2b2b")
COLOR = pygame.Color("#ff7259")
score = 0

paddle = pygame.Rect(WIDTH//2-150//2, HEIGHT-20, 150, 10)
paddle_x_change = 0

ball = pygame.Rect(WIDTH//2-10,HEIGHT-40,20,20)
ball_x_change = 5
ball_y_change = -5

rows = 4
columns = 5
padding_left = 10
padding_top = 10
block_width = 147
block_height = 40
block_list = []
generate_blocks()

lose_time = None
timer_font = pygame.font.SysFont("monospace", 70)
score_font = pygame.font.SysFont("monospace", 35)

while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            print(score)
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                paddle_x_change = -5

            if event.key == K_RIGHT:
                paddle_x_change = 5

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                paddle_x_change = 0

    screen.fill(BG_COLOR)

    paddle.x += paddle_x_change

    if paddle.left <= 0:
        paddle.left = 0

    if paddle.right >= WIDTH:
        paddle.right = WIDTH

    if lose_time:
        reset()

    
    ball_animation()
    draw_blocks(block_list)
    draw_score()
    pygame.draw.rect(screen, COLOR, paddle)
    pygame.draw.ellipse(screen, COLOR, ball)
    win()
    pygame.display.update()