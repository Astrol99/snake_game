import pygame
import random

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
DARK_GREEN = (36, 166, 54)
RED =   (255,   0,   0)

class Snake:
    def __init__(self, screen, width, height):
        # Starting location of snake
        self.x = 0
        self.y = 0
        # Distance to travel of snake
        self.distance = 20
        # Screen of snake
        self.screen = screen
        # Size of snake
        self.s_width = width
        self.s_height = height
        # Color of snake
        self.head_color = GREEN
        self.tail_color = DARK_GREEN
        # Direction of snake
        self.direction = "right"
        # Tails
        self.tails = 0
        self.history = []

    def draw(self): 
        pygame.draw.rect(self.screen, self.head_color, (self.x, self.y, self.s_width, self.s_height))
        for i in range(self.tails):
            pygame.draw.rect(self.screen, self.tail_color, (self.history[(len(self.history)-2)-i][0], self.history[(len(self.history)-2)-i][1], self.s_width, self.s_height))

    def move(self, keys, score):
        # Change coordinate and direction of snake
        if self.direction == "right":
            # Snake going right, either go up or down
            self.x += self.distance
            if keys[pygame.K_UP]:
                self.direction = "up"
            elif keys[pygame.K_DOWN]:
                self.direction = "down"
        elif self.direction == "left":
            # Snake going left, either go up or down
            self.x -= self.distance
            if keys[pygame.K_UP]:
                self.direction = "up"
            elif keys[pygame.K_DOWN]:
                self.direction = "down"
        elif self.direction == "up":
            # Snake going up, either go left or right
            self.y -= self.distance
            if keys[pygame.K_LEFT]:
                self.direction = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction = "right"
        elif self.direction == "down":
            # Snake going down, either go left or right
            self.y += self.distance
            if keys[pygame.K_LEFT]:
                self.direction = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction = "right"
        self.history.append([self.x, self.y])

class Apple:
    def __init__(self, screen, length, width):
        # Starting location of apple
        self.x, self.y = 0,0
        # Screen of apple
        self.screen = screen
        # Size of apple
        self.a_length = length
        self.a_width = width
        # Color of apple
        self.apple_color = RED
        self.distance = 20

        # Give apple a random coord
        self.random_pos()
    
    # Generate a random location for apple
    def random_pos(self):
        self.x = self.distance*random.randint(0,49)
        self.y = self.distance*random.randint(0, 29)
    
    def draw(self):
        pygame.draw.rect(self.screen, RED, (self.x, self.y, self.a_width, self.a_length))

class Game:
    def __init__(self):
        self.running = True
        self.window_size = self.width, self.height = 1000, 600

        # Regular pygame starting stuff
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snek Game")
        self.running = True

        self.score = 0

        # Text attributes
        self.myfont = pygame.font.SysFont("monospace", 16)

        # Create objects
        self.snake = Snake(self.screen, 15, 15)
        self.apple = Apple(self.screen, 15, 15)

        # Grid stuff
        self.grid_size = self.grid_x, self.grid_y = 999, 599

    def event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def loop(self):
        # Check if snake is out of bounds
        if self.snake.x < 0 or self.snake.x > self.grid_size[0] or self.snake.y < 0 or self.snake.y > self.grid_size[1]:
            print("Snake went over the grid")
            self.running = False

        # Check if snake is on apple
        if self.snake.x == self.apple.x and self.snake.y == self.apple.y:
            self.score += 1
            self.snake.tails += 1
            print("Score:",self.score)
            self.apple.random_pos()
            self.snake.history = self.snake.history[len(self.snake.history)-self.snake.tails:]

        keys = pygame.key.get_pressed()
        self.snake.move(keys, self.score)

        for i in range(self.snake.tails):
            # Check if snake eats it self
            if [self.snake.x, self.snake.y] == self.snake.history[(len(self.snake.history)-2)-i]:
                print("Snake ate itself")
                self.running = False

    def render(self):
        # Generate black background
        self.screen.fill(BLACK)

        # Text for score of snake
        scoreText = self.myfont.render(f"Score: {self.score}", 1, WHITE)
        self.screen.blit(scoreText, (5, 10))

        # Grid of play area
        # Vertical Lines
        pygame.draw.line(self.screen, WHITE, [0,0], [0, self.grid_size[1]], 1)
        pygame.draw.line(self.screen, WHITE, [self.grid_size[0], 0], [self.grid_size[0], self.grid_size[1]], 1)
        # Horizontal Line
        pygame.draw.line(self.screen, WHITE, [0,0], [self.grid_size[0], 0], 1)
        pygame.draw.line(self.screen, WHITE, [0, self.grid_size[1]], [self.grid_size[0], self.grid_size[1]], 1)

        # Draw snake
        self.snake.draw()
        # Draw apple
        self.apple.draw()

    def clean_exit(self):
        pygame.quit()

    def run(self):
        while(self.running):
            # Delay
            pygame.time.delay(80)
            # Get key events
            for event in pygame.event.get():
                self.event(event)
            # Actions and display loops
            self.loop()
            self.render()
            # Update screen
            pygame.display.update()
        # Smooth exit if while loop doesn't loop anymore
        self.clean_exit()

if __name__ == '__main__':
    snek_game = Game()
    snek_game.run()