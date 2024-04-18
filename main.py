from pygame import display, time, draw, QUIT, init
from random import randint
import pygame
from numpy import sqrt

# Initialize Pygame
init()

# Define colors
done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the number of columns and rows for the game grid
cols = 25
rows = 25

# Set the window dimensions
width = 600
height = 600
wr = width / cols  # Width of each cell
hr = height / rows  # Height of each cell
direction = 1  # Initial direction of the snake

# Create the game window
screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()

# Function to find the path from snake to food using the A* algorithm
def getpath(food1, snake1):
    # Reset the came_from and path-finding values for the food and snake
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]  # Open set starts with the snake's head
    closedset = []  # Closed set is initially empty
    dir_array1 = []  # Array to store the directions for the snake to follow

    while True:
        # Get the current cell with the lowest f-score from the open set
        current1 = min(openset, key=lambda x: x.f)
        # Remove the current cell from the open set
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        # Add the current cell to the closed set
        closedset.append(current1)

        # Check if the current cell is the food cell
        if current1 == food1:
            break

        # Explore the neighbors of the current cell
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1

    # Reconstruct the path from the snake's head to the food
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)  # Up
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)  # Down
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)  # Left
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)  # Right
        current1 = current1.camefrom

    # Reset the path-finding values for all cells in the grid
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0

    return dir_array1

# Spot class representing each cell in the grid
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        # 3% chance of being an obstacle
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    # Function to draw the cell on the screen
    def show(self, color):
        draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4])

    # Function to add neighboring cells to the neighbors list
    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Create the game grid
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

# Add neighbors to each cell in the grid
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

# Initialize the snake at the center of the grid
snake = [grid[round(rows / 2)][round(cols / 2)]]
# Initialize the food at a random location
food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
current = snake[-1]  # Current head of the snake
# Get the path from the snake to the food
dir_array = getpath(food, snake)
food_array = [food]  # List to store the food locations

# Game loop
while not done:
    clock.tick(12)  # Limit the frame rate to 12 FPS
    screen.fill(BLACK)  # Clear the screen

    # Get the next direction from the path
    direction = dir_array.pop(-1)

    # Move the snake based on the direction
    if direction == 0:    # Down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # Right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # Up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # Left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]  # Update the current head

    # Check if the snake reached the food
    if current.x == food.x and current.y == food.y:
        # Find a new non-obstacle location for the food
        while True:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)  # Add the new food location
        dir_array = getpath(food, snake)  # Get the new path
    else:
        snake.pop(0)  # Remove the tail

    # Draw the snake
    for spot in snake:
        spot.show(WHITE)

    # Draw the obstacles
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    # Draw the food and the snake's head
    food.show(GREEN)
    snake[-1].show(BLUE)

    display.flip()  # Update the display

    # Check for quit event
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True