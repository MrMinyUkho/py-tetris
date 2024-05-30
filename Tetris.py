from random import randint
import pygame
import time

def millis():
    return round(time.time() * 1000)

pygame.init()

field_size = [10, 25]
tile_size = 20
gap_size = 1

field = []

for i in range(field_size[1]):
    field.append([])
    for j in range(field_size[0]):
        field[i].append((10,10,10))

field_size_px = [
    field_size[0] * (tile_size + gap_size) - gap_size,
    field_size[1] * (tile_size + gap_size) - gap_size
]

content_gap = [10, 10]

score_board_width = 150

window_size = [
    field_size_px[0] + content_gap[0] * 2 + score_board_width,    
    field_size_px[1] + content_gap[1] * 2   
]

screen = pygame.display.set_mode(window_size)


figures = [
    [(-2,  0), (-1, 0), (0,  0), ( 1, 0)],    
    [( 0,  0), ( 1, 0), (0,  1), ( 1, 1)],    
    [( 0, -1), ( 0, 0), (0,  1), ( 1, 1)],    
    [( 0, -1), ( 0, 0), (0,  1), (-1, 1)],    
    [(-1,  0), ( 0, 0), (1,  0), ( 0, 1)],    
    [( 0,  0), ( 1, 0), (0, -1), ( 1, 1)],    
    [( 0,  0), ( 1, 0), (1, -1), ( 0, 1)]    
]

colors = [
    (  0, 255, 255),    
    (255, 255,   0),    
    (255, 125,   0),    
    (  0,   0, 255),    
    (255,   0, 255),    
    (  0, 255,   0),    
    (255,   0,   0)    
]

figure_fall = False

timer = millis()

current_figure = figures[0]
fig_pos = [0,0]
current_figure_id = 0

def checkSideCollision(shift):
    isLeftRightCollision = False
    for i in current_figure:
        isLeftRightCollision = isLeftRightCollision or i[0] + fig_pos[0] + shift[0] < 0 or i[0] + fig_pos[0] + shift[0] > field_size[0]-1
        isLeftRightCollision = isLeftRightCollision or field[i[1] + fig_pos[1] + shift[1]][i[0] + fig_pos[0] + shift[0]] != (10,10,10)

    return not isLeftRightCollision

def checkFallCollision(shift):
    isFallCollison = False
    for i in current_figure:
        isFallCollison = isFallCollison or i[1] + fig_pos[1] + shift[1] < 0 or i[1] + fig_pos[1] + shift[1] > field_size[1]-1
        isFallCollison = isFallCollison or field[i[1] + fig_pos[1] + shift[1]][i[0] + fig_pos[0] + shift[0]] != (10,10,10)
    return not isFallCollison

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                oldFigure = current_figure.copy()
                if current_figure_id != 1:
                    for i in range(4):
                        current_figure[i] = (-current_figure[i][1], current_figure[i][0])
                if not checkSideCollision((0,0)):
                    current_figure = oldFigure
            if event.key == pygame.K_LEFT:
                if checkSideCollision((-1, 0)):
                    fig_pos[0] -= 1
            if event.key == pygame.K_RIGHT:
                if checkSideCollision((1, 0)):
                    fig_pos[0] += 1
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        timer -= 10
            
    screen.fill((25, 25, 25))
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            pygame.draw.rect(screen, field[j][i], 
                             (content_gap[0] + (tile_size + gap_size) * i + gap_size,
                              content_gap[1] + (tile_size + gap_size) * j + gap_size,
                              tile_size - gap_size,
                              tile_size - gap_size))

    for i in current_figure:
        pygame.draw.rect(screen,colors[current_figure_id], 
                             (content_gap[0] + (tile_size + gap_size) * (i[0] + fig_pos[0]) + gap_size,
                              content_gap[1] + (tile_size + gap_size) * (i[1] + fig_pos[1]) + gap_size,
                              tile_size - gap_size,
                              tile_size - gap_size))

    if figure_fall:
        if millis() - timer > 500:
            if checkFallCollision((0, 1)):
                fig_pos[1] += 1
            else:
                figure_fall = False
                for i in current_figure:
                    field[i[1] + fig_pos[1]][i[0] + fig_pos[0]] = colors[current_figure_id]
                
                lineToDelete = []
                for i in range(field_size[1]-1, 0, -1):
                    filled_current_line = True
                    
                    for j in range(field_size[0]):
                        filled_current_line = filled_current_line and field[i][j] != (10,10,10)
                        print(field[i][j] == (10,10,10),":",filled_current_line, end=", ")
                     
                    print(filled_current_line)

                    if filled_current_line:
                        lineToDelete.append(i)
                    
                for i in lineToDelete:
                    field.pop(i)
                    
                for i in range(len(lineToDelete)):
                    field.insert(0, field[0].copy())
                
            timer = millis()
    else:
        current_figure_id = randint(0, 6)
        current_figure = figures[current_figure_id]
        figure_fall = True
        fig_pos = [field_size[0]//2, 1]

    pygame.display.flip()

pygame.quit()