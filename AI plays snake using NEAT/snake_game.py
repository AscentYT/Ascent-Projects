import pygame
import random

class SnakeGame:
    def __init__(self, width=540, height=960, tile_size=18, fps=10):
        pygame.init()
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game Class")
        self.clock = pygame.time.Clock()

        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

        self.reset()

    def reset(self):
        self.snake = [(0, 0)]  
        self.direction = 0     
        self.grow = 0
        self.apple = self._random_apple_pos()
        self.running = True

    def _random_apple_pos(self):
        grid_width = self.width // self.tile_size
        grid_height = self.height // self.tile_size
        return (
            random.randint(0, grid_width - 1) * self.tile_size,
            random.randint(0, grid_height - 1) * self.tile_size
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.direction != 1:
                    self.direction = 0
                elif event.key == pygame.K_LEFT and self.direction != 0:
                    self.direction = 1
                elif event.key == pygame.K_UP and self.direction != 3:
                    self.direction = 2
                elif event.key == pygame.K_DOWN and self.direction != 2:
                    self.direction = 3
    def get_inputs(self):
        head_x, head_y = self.snake[0]
        dir = self.direction
        apple_x, apple_y = self.apple


        def danger(x, y):
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return 1.0
            if (x, y) in self.snake:
                return 1.0
            return 0.0

        directions = {
            0: (self.tile_size, 0),  
            1: (-self.tile_size, 0),  
            2: (0, -self.tile_size),  
            3: (0, self.tile_size),
        }

        def turn_left(d):
            return {0: 2, 2: 1, 1: 3, 3: 0}[d]
        def turn_right(d):
            return {0: 3, 3: 1, 1: 2, 2: 0}[d]

        # Danger straight
        dx, dy = directions[dir]
        danger_straight = danger(head_x + dx, head_y + dy)

        # Danger right
        dx, dy = directions[turn_right(dir)]
        danger_right = danger(head_x + dx, head_y + dy)

        # Danger left
        dx, dy = directions[turn_left(dir)]
        danger_left = danger(head_x + dx, head_y + dy)

        # Direction encoding
        moving_up = 1 if dir == 2 else 0
        moving_down = 1 if dir == 3 else 0
        moving_left = 1 if dir == 1 else 0
        moving_right = 1 if dir == 0 else 0

        # Apple location relative to head
        apple_left = 1 if apple_x < head_x else 0
        apple_right = 1 if apple_x > head_x else 0
        apple_up = 1 if apple_y < head_y else 0
        apple_down = 1 if apple_y > head_y else 0

        return [
            danger_straight,
            danger_right,
            danger_left,
            moving_up,
            moving_down,
            moving_left,
            moving_right,
            apple_left,
            apple_right,
            apple_up,
            apple_down
        ]
    
    def update(self):
        head_x, head_y = self.snake[0]

        if self.direction == 0:
            head_x += self.tile_size
        elif self.direction == 1:
            head_x -= self.tile_size
        elif self.direction == 2:
            head_y -= self.tile_size
        elif self.direction == 3:
            head_y += self.tile_size

        # Check for wall collisions
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.running = False
            return

        # Insert new head position
        new_head = (head_x, head_y)
        if new_head in self.snake:
            self.running = False
            return
        self.snake.insert(0, new_head)

        # Check apple collision
        if head_x == self.apple[0] and head_y == self.apple[1]:
            self.grow += 1
            self.apple = self._random_apple_pos()
        else:
            if self.grow > 0:
                self.grow -= 1
            else:
                self.snake.pop()

    def draw(self):
        self.screen.fill(self.black)
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.green, (*segment, self.tile_size, self.tile_size))
        pygame.draw.rect(self.screen, self.red, (*self.apple, self.tile_size, self.tile_size))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    def set_new_direction(self, action):
        if action == 0:
            return self.direction

        right_turns = {0: 3, 3: 1, 1: 2, 2: 0}
        left_turns = {0: 2, 2: 1, 1: 3, 3: 0}

        if action == 1:
            self.direction = right_turns[self.direction]
        else:
            self.direction = left_turns[self.direction]

if __name__ == "__main__":
    game = SnakeGame()
    game.run()