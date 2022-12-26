import pygame
import sys
from pygame.locals import *
import math
import random
import time

pygame.init()
state = 0
turns = 0
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

font_size = []
game_over_font = pygame.font.SysFont("Times New Roman", 32)


def max_size(val, text):
    # Returns maximum font size for displaying given text.
    font = pygame.font.SysFont("Times New Roman", val)
    while font.size(text)[0] < 100 and font.size(text)[1] < 100:
        val += 1
        font = pygame.font.SysFont("Times New Roman", val)
    return val - 1


for i in range(0, 6):
    font_size.append(max_size(1, str(pow(10, i))))


class Value(pygame.sprite.Sprite):

    def __init__(self, spot, pos, val):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(center=(spot[0] + 50, spot[1] + 50))
        self.value = val
        self.font = pygame.font.SysFont("Times New Roman", 89)
        self.text = self.font.render((str(self.value)), True, (255, 255, 255))
        self.pos = pos  # Position in the board array

    def resize(self):
        global font_size
        key = math.log(self.value, 10)
        # Resize the font of tiles as needed
        self.font = pygame.font.SysFont("Times New Roman", font_size[int(key)])

    def draw(self, surface):
        # draws the values onto the board
        self.resize()
        self.text = self.font.render((str(self.value)), True, (255, 255, 255))
        # Finds proper position for text before bliting text
        params = self.font.size(str(self.value))
        params = ((self.rect[2] - params[0]) // 2, (self.rect[3] - params[1]) // 2)
        params = (self.rect[0] + params[0], self.rect[1] + params[1], self.rect[2], self.rect[3])
        surface.blit(self.text, params)

    def __repr__(self):
        return repr(self.value)


def initial(bor, pos):
    # Places initial 2 values on board
    # Can remove
    one = random.choice(pos)
    positions.remove(one)
    two = random.choice(pos)
    positions.remove(two)
    bor[one[0]][one[1]] = Value(((one[1] + 1) * 100, (one[0] + 1) * 100), one, 2)
    bor[two[0]][two[1]] = Value(((two[1] + 1) * 100, (two[0] + 1) * 100), two, 2)


def add(turns):
    # Used to add tiles after each turn
    global positions
    global board
    # Subject to balance changes
    key = 2
    if turns % 40 == 0 and turns != 0:  # Occasionally adds a 4 to slightly accelerate gameplay.
        key = 4

    # TESTING VALUE, REMOVE IN FINAL
    # key = 512

    if len(positions) > 0:
        # Only adds if possible
        spot = random.choice(positions)
        board[spot[0]][spot[1]] = Value(((spot[1] + 1) * 100, (spot[0] + 1) * 100), (spot[0], spot[1]), key)
        positions.remove(spot)


def printB(bo):
    # Note: Unneeded in final build
    # Prints the board as an array to console.
    for e in bo:
        print(e)
    print()


def changes(oldB, newB):
    # Returns False if there are no changes between the two
    # True if any changes are detected
    for i in range(len(oldB)):
        for j in range(len(oldB)):
            if oldB[i][j] and newB[i][j]:
                if oldB[i][j].value != newB[i][j].value:
                    return True
            elif not oldB[i][j] and not newB[i][j]:
                pass
            else:
                return True
    return False



display = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Game")
FPS = pygame.time.Clock()
FPS.tick(60)

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

old = []
scoreF = pygame.font.SysFont("Times New Roman", 32)
retry = game_over_font.render("Retry?: Spacebar", True, (255, 255, 255))
retry_rect = retry.get_rect()
params = game_over_font.size(("Retry?: Spacebar" + (str(turns))))
params = ((600 - params[0]) // 2, (600 - params[1]) // 2)
retry_rect = (params[0], params[1] + 50, retry_rect[2], retry_rect[3])
indices = []

def scoreDisplay(display, turns):
    # Puts score on main display
    global scoreF
    scoreText = scoreF.render(("Turns: " + (str(turns))), True, RED)
    scoreRect = scoreText.get_rect()
    display.blit(scoreText, scoreRect)


def drawBox(display, colour):
    # Draws the "container" of the game as well as the grid
    # Outsize border
    pygame.draw.rect(display, colour, pygame.Rect(100, 100, 400, 400), 1)
    # Inner grid
    # Vertical
    pygame.draw.line(display, colour, (200, 100), (200, 500))
    pygame.draw.line(display, colour, (300, 100), (300, 500))
    pygame.draw.line(display, colour, (400, 100), (400, 500))
    # Horizontal Lines
    pygame.draw.line(display, colour, (100, 200), (500, 200))
    pygame.draw.line(display, colour, (100, 300), (500, 300))
    pygame.draw.line(display, colour, (100, 400), (500, 400))

def adj_indices():
    # Initializes a list of adj indices per index
    global indices
    for a in range(0, 4):
        inner = []
        for b in range(0, 4):
            values = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if abs(i) != abs(j):
                        if 0 <= i + a <= 3:
                            if 0 <= j + b <= 3:
                                values.append((i + a, j + b))
            inner.append(values.copy())
        indices.append(inner.copy())

def adj_check(board, ind):
    global indices
    # Given an index, checks if any adj values are the same
    for e in indices[ind[0]][ind[1]]:
        if board[e[0]][e[1]].value == board[ind[0]][ind[1]].value:
            return True
    else:
        return False

def loss_check(board):
    # Returns true if there are any moves left on the board
    for i in range(0,4):
        for j in range(0,4):
            if i % 3 != j % 3:
                if adj_check(board, (i,j)):
                    return True
    return False
def start():
    # Initializes the game.
    global state
    global turns
    global MASTER_POS
    global positions
    global old
    global board
    # Reset all relevant variables
    state = 0
    turns = 0
    # Clears the board
    for e in range(len(board)):
        for i in range(len(board)):
            board[e][i] = 0
    positions = MASTER_POS.copy()
    # Starting 2 pieces
    add(turns)
    add(turns)
    turns = 0
    old = []

adj_indices()
start()
# TODO: Choose nicer colours for game
while True:
    if state == 0:
        display.fill(BLACK)
        drawBox(display, RED)
        scoreDisplay(display, turns)
        for arr in board:
            for e in arr:
                if e:
                    e.draw(display)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for e in board:
                    old.append(e.copy())
                if event.key == pygame.K_UP:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[j][i] != 0:
                                for k in range(j, 0, -1):
                                    if board[k - 1][i] == 0:
                                        # TODO: Clean up movement animation
                                        for a in range(2):
                                            board[k][i].rect.move_ip(0, -50)
                                            board[k][i].draw(display)
                                            pygame.display.flip()
                                        board[k - 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k - 1, i) in positions:
                                            positions.remove((k - 1, i))
                                    elif board[k - 1][i].value == board[k][i].value:
                                        for a in range(2):
                                            board[k][i].rect.move_ip(0, -50)
                                            board[k][i].draw(display)
                                            pygame.display.flip()
                                        board[k - 1][i].value = board[k - 1][i].value * 2
                                        if board[k - 1][i].value == 2048:
                                            state = 2
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k - 1, i) in positions:
                                            positions.remove((k - 1, i))
                                        break
                elif event.key == pygame.K_DOWN:
                    for i in range(4):
                        for j in range(2, -1, -1):
                            if board[j][i] != 0:
                                for k in range(j, 3):
                                    if board[k + 1][i] == 0:
                                        for a in range(2):
                                            board[k][i].rect.move_ip(0, 50)
                                            board[k][i].draw(display)
                                            pygame.display.flip()
                                        board[k + 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k + 1, i) in positions:
                                            positions.remove((k + 1, i))
                                    elif board[k + 1][i].value == board[k][i].value:
                                        for a in range(2):
                                            board[k][i].rect.move_ip(0, 50)
                                            board[k][i].draw(display)
                                            pygame.display.flip()
                                        board[k + 1][i].value = board[k + 1][i].value * 2
                                        if board[k + 1][i].value == 2048:
                                            state = 2
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k + 1, i) in positions:
                                            positions.remove((k + 1, i))
                                        break
                elif event.key == pygame.K_LEFT:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[i][j] != 0:
                                for k in range(j, 0, -1):
                                    if board[i][k - 1] == 0:
                                        for a in range(2):
                                            board[i][k].rect.move_ip(-50, 0)
                                            board[i][k].draw(display)
                                            pygame.display.flip()
                                        board[i][k - 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                    elif board[i][k - 1].value == board[i][k].value:
                                        for a in range(2):
                                            board[i][k].rect.move_ip(-50, 0)
                                            board[i][k].draw(display)
                                            pygame.display.flip()
                                        board[i][k - 1].value = board[i][k - 1].value * 2
                                        if board[i][k - 1].value == 2048:
                                            state = 2
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
                                        for a in range(2):
                                            board[i][k].rect.move_ip(50, 0)
                                            board[i][k].draw(display)
                                            pygame.display.flip()
                                        board[i][k + 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                    elif board[i][k + 1].value == board[i][k].value:
                                        for a in range(2):
                                            board[i][k].rect.move_ip(50, 0)
                                            board[i][k].draw(display)
                                            pygame.display.flip()
                                        board[i][k + 1].value = board[i][k + 1].value * 2
                                        if board[i][k + 1].value == 2048:
                                            state = 2
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        break
                if changes(old, board):
                    turns += 1
                    add(turns)
                old = []
        if len(positions) == 0:
            if not loss_check(board):
                state = 1
    elif state == 1:
        # TODO: implement opaque/transparent screen as game over rather than full black screen (let player see end grid)
        # Game over/restart screen
        game_over = game_over_font.render(("Game Over! Turns taken: " + (str(turns))), True, (255, 255, 255))
        go_rect = game_over.get_rect()
        display.fill(BLACK)
        params = game_over_font.size(("Game Over! Turns taken: " + (str(turns))))
        params = ((600 - params[0]) // 2, (600 - params[1]) // 2)
        params = (params[0], params[1], go_rect[2], go_rect[3])
        display.blit(game_over, params)
        display.blit(retry, retry_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start()
    elif state == 2:
        # Player win screen/restart?
        game_over = game_over_font.render(("You win! Turns taken: " + (str(turns))), True, (255, 255, 255))
        go_rect = game_over.get_rect()
        display.fill(BLACK)
        params = game_over_font.size(("You win! Turns taken: " + (str(turns))))
        params = ((600 - params[0]) // 2, (600 - params[1]) // 2)
        params = (params[0], params[1], go_rect[2], go_rect[3])
        display.blit(game_over, params)
        display.blit(retry, retry_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start()