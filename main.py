import pygame
import math
import copy
import random

pygame.font.init()

FPS = 60
WIDTH = 1300
HEIGTH = 600
CELL_SIZE = 25

WIN = pygame.display.set_mode((WIDTH, HEIGTH))  # 52 x 24 cells (25 x 25 px)
pygame.display.set_caption("Game of Life")

CELL = pygame.image.load("assets/cell.jpg")
GOD_TEXTURE = pygame.transform.scale(pygame.image.load("assets/god.jpg"), (CELL_SIZE, CELL_SIZE))
BACKGROUND = pygame.image.load("assets/background.jpg")
BORDER = pygame.image.load("assets/border.jpg")
TOP_BAR = pygame.image.load("assets/top_bar.jpg")
MENU_BG = pygame.image.load("assets/menu_bg.jpg")

MENU_BG = pygame.transform.scale(MENU_BG, (WIDTH, HEIGTH))
PLACEMENT_TEXT = pygame.font.SysFont("Arial", 21)

CELL = pygame.transform.scale(CELL, (CELL_SIZE, CELL_SIZE))


def board_process(BOARD):
    INITIAL_BOARD = copy.deepcopy(BOARD)

    for i, list in enumerate(INITIAL_BOARD):
        for j, item in enumerate(list):
            if item == 2:
                continue

            neigbors = 0
            if INITIAL_BOARD[i-1][j] == 1:
                neigbors += 1
            if INITIAL_BOARD[i+1][j] == 1:
                neigbors += 1
            if INITIAL_BOARD[i][j+1] == 1:
                neigbors += 1
            if INITIAL_BOARD[i][j-1] == 1:
                neigbors += 1

            if INITIAL_BOARD[i-1][j+1] == 1:
                neigbors += 1
            if INITIAL_BOARD[i+1][j-1] == 1:
                neigbors += 1
            if INITIAL_BOARD[i+1][j+1] == 1:
                neigbors += 1
            if INITIAL_BOARD[i-1][j-1] == 1:
                neigbors += 1

            if neigbors < 2:
                BOARD[i][j] = 0 # cell dies underpopulation
            elif neigbors == 3:
                BOARD[i][j] = 1 #cell becomes alive
            elif neigbors > 3:
                BOARD[i][j] = 0 # cell dies overpopulation

    for i, line in enumerate(BOARD):
        for j, item in enumerate(line):
            if i == 1 or i == 23 or j == 0 or j == 51:
                BOARD[i][j] = 2
    return BOARD

def update_window(WIN, BOARD):
    pygame.display.update()
    i, j = 0, 0

    while j < HEIGTH:
        if j != 0:
            WIN.blit(BACKGROUND, (i, j))
        i += CELL_SIZE
        if i >= WIDTH:
            i = 0
            j += CELL_SIZE

    for i, line in enumerate(BOARD):
        if i > 1:
            for j, number in enumerate(line):
                if number == 1:
                    WIN.blit(CELL, (j * 25, i * 25))

    for i, line in enumerate(BOARD):
        if i != 0:
            for j, number in enumerate(line):
                if number == 2:
                    WIN.blit(BORDER, (j * 25, i * 25))


def main():
    run = 1

    BOARD = [[0] * math.floor(WIDTH / 25) for i in range(math.floor(HEIGTH / 25))]

    for i, line in enumerate(BOARD):
        for j, item in enumerate(line):
            if i == 1 or i == 23 or j == 0 or j == 51:
                BOARD[i][j] = 2

    GOD = pygame.Rect(WIDTH // 25 // 2 * 25, HEIGTH // 25 // 2 * 25, CELL_SIZE, CELL_SIZE)
    placement = 1
    gameplay = 1
    generation = 1
    menu = 1
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
# MENU =======================================================================================================================
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    placement = 0
                    run = 0
                    gameplay = 0
                    menu = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_1]:
                menu = 0
            if keys[pygame.K_2]:
                for i, line in enumerate(BOARD):
                    for j, item in enumerate(line):
                        if i == 1 or i == 23 or j == 0 or j == 51:
                            BOARD[i][j] = 2
                        else:
                            lol = random.randint(0, 15)
                            if lol < 7:
                                BOARD[i][j] = 1
                menu = 0

            pygame.display.update()
            WIN.blit(MENU_BG, (0,0))

# CELL PLACEMENT =============================================================================================================
        while placement:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    placement = 0
                    run = 0
                    gameplay = 0

            WIN.blit(GOD_TEXTURE, (GOD.x, GOD.y))
            update_window(WIN, BOARD)

            keys = pygame.key.get_pressed()

            for i in keys:
                if i:
                    pygame.time.delay(100)
                    break

            if keys[pygame.K_d] and GOD.x < WIDTH - 50:
                GOD.x += CELL_SIZE
            if keys[pygame.K_a] and GOD.x > 25:
                GOD.x -= CELL_SIZE
            if keys[pygame.K_w] and GOD.y > 50:
                GOD.y -= CELL_SIZE
            if keys[pygame.K_s] and GOD.y < HEIGTH - 50:
                GOD.y += CELL_SIZE

            if keys[pygame.K_SPACE]:
                BOARD[GOD.y // 25][GOD.x // 25] = 1
            if keys[pygame.K_LSHIFT]:
                BOARD[GOD.y // 25][GOD.x // 25] = 0

            if keys[pygame.K_ESCAPE]:
                placement = 0

            text = PLACEMENT_TEXT.render("Use the WASD keys to move around. Press SPACE to place a cell and press "
                                         "LEFT_SHIFT to delete a cell. Press ESC to run the game!", 1, (255, 255, 255))
            WIN.blit(text, (0, 0))
        WIN.blit(TOP_BAR, (0, 0))
# GAMEPLAY =============================================================================================================
        while gameplay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    placement = 0
                    run = 0
                    gameplay = 0

            pygame.time.delay(160)
            update_window(WIN, BOARD)
            #pygame.time.delay(100)
            WIN.blit(TOP_BAR, (0, 0))
            text = PLACEMENT_TEXT.render("Generation: " + str(generation) + "     "
                                                                            "                                                                               Conway's Game of Life",
                                         1, (255, 255, 255))
            WIN.blit(text, (0, 0))
            pygame.display.update()
            BOARD = board_process(BOARD)
            generation += 1

        update_window(WIN, BOARD)

    pygame.quit()


if __name__ == "__main__":
    main()
