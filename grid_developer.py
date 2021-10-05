import pygame


def redundant(arr):
    # Delete the elements which appear more than or equal to 1 times.
    for elem in arr:
        if (arr.count(elem) > 1):
            for j in range(arr.count(elem)):
                arr.remove(elem)


def generate_grid(window, coords_of_cells):
    # Positions and sizes
    from settings import gridPos, cellSize

    # coordinates of cells will help us draw the shapes
    lines_to_draw = []

    # This populates the list "lines_to_draw" with lines (this will make a square 2x2 shape)
    for x, y in coords_of_cells:
        lines_to_draw.append({((x * cellSize), (y * cellSize)), ((x * cellSize) + cellSize, (y * cellSize))})
        lines_to_draw.append({((x * cellSize), (y * cellSize)), ((x * cellSize), (y * cellSize) + cellSize)})
        lines_to_draw.append(
            {((x * cellSize), (y * cellSize) + cellSize), ((x * cellSize) + cellSize, (y * cellSize) + cellSize)})
        lines_to_draw.append(
            {((x * cellSize) + cellSize, (y * cellSize)), ((x * cellSize) + cellSize, (y * cellSize) + cellSize)})

    # We then remove lines that appear twice in that list (those lines are the interior lines)
    redundant(lines_to_draw)

    # We can now draw the lines because all lines left are outline
    for line in lines_to_draw:
        # Grid area color
        from settings import GRID_AREA_RED

        list_from_set = list(line)
        pygame.draw.line(window, GRID_AREA_RED, (gridPos[0] + list_from_set[0][0], gridPos[1] + list_from_set[0][1]),
                         (gridPos[0] + list_from_set[1][0], gridPos[1] + list_from_set[1][1]), 3)
