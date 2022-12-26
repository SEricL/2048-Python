import pygame
import sys
from pygame.locals import *
import math
import random

pygame.init()
state = 0
MASTER_POS = [(0, 0), (1, 0), (2, 0), (3, 0),
              (0, 1), (1, 1), (2, 1), (3, 1),
              (0, 2), (1, 2), (2, 2), (3, 2),
              (0, 3), (1, 3), (2, 3), (3, 3)]

positions = [(0, 0), (1, 0), (2, 0), (3, 0),
             (0, 1), (1, 1), (2, 1), (3, 1),
             (0, 2), (1, 2), (2, 2), (3, 2),
             (0, 3), (1, 3), (2, 3), (3, 3)]

board = [
    [0, 0, 0, 0],  # 0,0 | 0,1 | 0,2 | 0,3
    [0, 0, 0, 0],  # 1,0 | 1,1 | 1,2 | 1,3
    [0, 0, 0, 0],  # 2,0 | 2,1 | 2,2 | 2,3
    [0, 0, 0, 0]  # 3,0 | 3,1 | 3,2 | 3,3
]
lastMove = None


def initial(bor, pos):
    one = random.choice(pos)
    positions.remove(one)
    two = random.choice(pos)
    bor[one[0]][one[1]] = 2
    bor[two[0]][two[1]] = 2


def printB(bo):
    for i in bo:
        print(i)
    print()


display = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Game")
FPS = pygame.time.Clock()
FPS.tick(60)

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# Place starting 2 items
positions = MASTER_POS.copy()
initial(board, positions)


class Value(pygame.sprite.Sprite):

    def __init__(self, spot, pos):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(center=spot)
        self.value = 2
        self.font = pygame.font.SysFont("Times New Roman", 60)
        self.text = self.font.render((str(self.value)), True, (255, 255, 255))
        self.pos = pos  # Position in the board array

    def draw(self, surface):
        surface.blit(self.text, self.rect)


while True:
    if state == 0:
        display.fill(BLACK)
        pygame.display.flip()
        printB(board)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[j][i] != 0:
                                for k in range(j, 0, -1):
                                    if board[k - 1][i] == 0:
                                        board[k - 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                        lastMove = pygame.K_UP
                                    elif board[k - 1][i] == board[k][i]:
                                        board[k - 1][i] = board[k - 1][i] * 2
                                        board[k][i] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                        break
                elif event.key == pygame.K_DOWN:
                    for i in range(4):
                        for j in range(2, -1, -1):
                            if board[j][i] != 0:
                                for k in range(j, 3):
                                    if board[k + 1][i] == 0:
                                        board[k + 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        lastMove = pygame.K_DOWN
                                    elif board[k + 1][i] == board[k][i]:
                                        board[k + 1][i] = board[k + 1][i] * 2
                                        board[k][i] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        break
                elif event.key == pygame.K_LEFT:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[i][j] != 0:
                                for k in range(j, 0, -1):
                                    if board[i][k - 1] == 0:
                                        board[i][k - 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                        lastMove = pygame.K_LEFT
                                    elif board[i][k - 1] == board[i][k]:
                                        board[i][k - 1] = board[i][k - 1] * 2
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                        break
                elif event.key == pygame.K_RIGHT:
                    for i in range(4):
                        for j in range(2, -1, -1):
                            if board[i][j] != 0:
                                for k in range(j, 3):
                                    if board[i][k + 1] == 0:
                                        board[i][k + 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        lastMove = pygame.K_RIGHT
                                    elif board[i][k + 1] == board[i][k]:
                                        board[i][k + 1] = board[i][k + 1] * 2
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        break
