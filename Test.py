import random

turns = 0

MASTER_POS = [(0, 0), (0, 1), (0, 2), (0, 3),
              (1, 0), (1, 1), (1, 2), (1, 3),
              (2, 0), (2, 1), (2, 2), (2, 3),
              (3, 0), (3, 1), (3, 2), (3, 3)]

positions = [(0, 0), (0, 1), (0, 2), (0, 3),
             (1, 0), (1, 1), (1, 2), (1, 3),
             (2, 0), (2, 1), (2, 2), (2, 3),
             (3, 0), (3, 1), (3, 2), (3, 3)]

board = [
    [0, 0, 0, 0],  # 0,0 | 0,1 | 0,2 | 0,3
    [0, 0, 0, 0],  # 1,0 | 1,1 | 1,2 | 1,3
    [0, 0, 0, 0],  # 2,0 | 2,1 | 2,2 | 2,3
    [0, 0, 0, 0]  # 3,0 | 3,1 | 3,2 | 3,3
]


def add(turns):
    # Used to add tiles after each turn
    global positions
    global board
    # Subject to balance changes
    key = 2
    if turns % 40 == 0 and turns != 0:  # Occasionally adds a 4 to slightly accelerate gameplay.
        key = 4

    if len(positions) > 0:
        # Only adds if possible
        spot = random.choice(positions)
        board[spot[0]][spot[1]] = key
        positions.remove(spot)


def restart():
    global board
    global positions
    global MASTER_POS
    global turns
    board = [
        [0, 0, 0, 0],  # 0,0 | 0,1 | 0,2 | 0,3
        [0, 0, 0, 0],  # 1,0 | 1,1 | 1,2 | 1,3
        [0, 0, 0, 0],  # 2,0 | 2,1 | 2,2 | 2,3
        [0, 0, 0, 0]  # 3,0 | 3,1 | 3,2 | 3,3
    ]
    positions = MASTER_POS.copy()
    turns = 0
    add(turns)
    add(turns)


def moveEntry(i, j, direction, axis):
    # If calling function
    global board
    global positions
    global turns

    current = board[i][j] if axis == 0 else board[j][i]
    if current == 0:
        return False

    if axis == 0:
        if board[i+direction][j] == 0 or board[i+direction][j] == current:
            # Do stuff
            board[i+direction][j] += current
            board[i][j] = 0
            try:
                positions.remove((i+direction, j))
            except ValueError:
                pass
            positions.append((i, j))
            return True
    else:
        if board[j][i+direction] == 0 or board[j][i+direction] == current:
            # Do stuff
            board[j][i+direction] += current
            board[j][i] = 0
            try:
                positions.remove((j, i+direction))
            except ValueError:
                pass
            positions.append((j, i))
            return True

    return False


def move(axis, direction):
    """
        Axis: 0 = Up/Down, 1 = Left/Right
        Direction: -1 = Up/Left, 1 = Down/Right

        Currently merges all possible tiles at once, rather than in several levels ([2][2][4] -> [8])
    """
    global board
    global positions
    global MASTER_POS
    global turns
    moved = False
    other = 3
    ran = range(2, -1, -1)
    if direction == -1:
        ran = range(0, 4)
        other = 0

    for j in ran:
        for i in range(j, other, direction):
            if moveEntry(i, 0, direction, axis) or moveEntry(i, 1, direction, axis) or moveEntry(i, 2, direction, axis)\
                    or moveEntry(i, 3, direction, axis):
                moved = True

    if moved:
        return True
    return False


# restart()
board = [[0, 0, 0, 0],
         [0, 2, 0, 2],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

for row in board:
    print(row)

while len(positions) > 0:
    print("Key:")
    movement = False
    key = input().lower()
    match key:
        case "w":
            movement = move(0, -1)
        case "s":
            movement = move(0, 1)
        case "a":
            movement = move(1, -1)
        case "d":
            movement = move(1, 1)

    if movement:
        add(turns)

    for row in board:
        print(row)
