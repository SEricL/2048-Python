gridSize = (4, 4)
fmt = '{}AdjOf({}, {}).'

output = []
grid = [[col + (row * gridSize[1]) for col in range(gridSize[1])] for row in range(gridSize[0])]

"""
0   1   2   3
4   5   6   7
8   9   10  11
12  13  14  15
"""
for rowIndex, rowValue in enumerate(grid):
    for colIndex, colValue in enumerate(rowValue):
        """ North adjacent """
        adjRow = rowIndex + 1
        if not (adjRow < 0 or adjRow >= gridSize[0]):
            adjCol = colIndex
            if not (adjCol < 0 or adjCol >= gridSize[1]):
                output.append(fmt.format('north', colValue, grid[adjRow][adjCol]))
        """ South adjacent """
        adjRow = rowIndex - 1
        if not (adjRow < 0 or adjRow >= gridSize[0]):
            adjCol = colIndex
            if not (adjCol < 0 or adjCol >= gridSize[1]):
                output.append(fmt.format('south', colValue, grid[adjRow][adjCol]))
        """ East adjacent """
        adjCol = colIndex - 1
        if not (adjCol < 0 or adjCol >= gridSize[1]):
            adjRow = rowIndex
            if not (adjRow < 0 or adjRow >= gridSize[0]):
                output.append(fmt.format('east', colValue, grid[adjRow][adjCol]))
        """ West adjacent """
        adjCol = colIndex + 1
        if not (adjCol < 0 or adjCol >= gridSize[1]):
            adjRow = rowIndex
            if not (adjRow < 0 or adjRow >= gridSize[0]):
                output.append(fmt.format('west', colValue, grid[adjRow][adjCol]))

output.sort()
print('\n'.join(output))
