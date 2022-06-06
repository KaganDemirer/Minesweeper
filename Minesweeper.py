import pygame
import random

grid_x = 10
grid_y = 10
screen_x = 20*grid_x
screen_y = 20*grid_y
mines = 10
lost = False
marked = []

# window 500x500
pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Minesweeper')

class Cell:
    def __init__(self, x, y, mine):
        self.x = x
        self.y = y
        self.is_mine = mine
        self.is_revealed = False
        self.neighbors = []
        self.neighbors_with_mine = []

    def set_neighbors(self):
        neighbors = []
        neighbors_with_mine = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                if i >= 0 and j >= 0 and i < grid_x and j < grid_y:
                    neighbors.append(grid[i][j])
                    if grid[i][j].is_mine:
                        neighbors_with_mine.append(grid[i][j])
        self.neighbors = neighbors
        self.neighbors_with_mine = neighbors_with_mine

    def reveal_neighbors(self, count):
        for neighbor in self.neighbors:
            if not neighbor.is_revealed and len(neighbor.neighbors_with_mine) == 0 and count <= grid_x//10:
                neighbor.is_revealed = True
                neighbor.reveal_neighbors(count+1)

grid = [[Cell(y, x, False) for x in range(grid_x)] for y in range(grid_y)]

# reset game
def reset():
    global lost
    global grid
    lost = False
    grid = [[Cell(y, x, False) for x in range(grid_x)] for y in range(grid_y)]
    set_mines(mines)

# set mines
def set_mines(mines):
    for _ in range(mines):
        x = random.randint(0, grid_x-1)
        y = random.randint(0, grid_y-1)
        if grid[y][x].is_mine == False:
            grid[y][x].is_mine = True
        else:
            set_mines(1)

set_mines(mines)

# draw boxes
def draw_boxes():
    for x in range(0, screen_x, 20):
        for y in range(0, screen_y, 20):
            if grid[x//20][y//20].is_revealed == False:
                pygame.draw.rect(screen, (30, 30, 30), (x, y, 20, 20), 1)
                if grid[x//20][y//20] in marked:
                    pygame.draw.rect(screen, (0, 255, 0), (x, y, 20, 20))
            else:
                pygame.draw.rect(screen, (60, 60, 60), (x, y, 20, 20))
                # draw number
                if len(grid[x//20][y//20].neighbors_with_mine) > 0:
                    font = pygame.font.SysFont('Arial', 15)
                    text = font.render(str(len(grid[x//20][y//20].neighbors_with_mine)), True, (255, 255, 255))
                    screen.blit(text, (x+5, y+2))
            if lost:
                if grid[x//20][y//20].is_mine:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, 20, 20))
            grid[x//20][y//20].set_neighbors()


# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            y = pos[0]//20
            x = pos[1]//20
            if event.button == 1:
                if lost == False:
                    if grid[y][x] not in marked:
                        if grid[y][x].is_mine == False:
                            grid[y][x].is_revealed = True
                            if len(grid[y][x].neighbors_with_mine) == 0:
                                grid[y][x].reveal_neighbors(1)
                        else:
                            lost = True
                else:
                    reset()
            if event.button == 3:
                if lost == False:
                    if grid[y][x].is_revealed == False:
                        if grid[y][x] in marked:
                            marked.remove(grid[y][x])
                        else:
                            marked.append(grid[y][x])
                else:
                    reset()

    screen.fill((0, 0, 0))
    draw_boxes()
    pygame.display.flip()