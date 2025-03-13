import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
CELL_SIZE = 30
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)

# Load Sprites
hunter_sprite = pygame.image.load("assets/hunter.png")
knight_sprite = pygame.image.load("assets/knight.png")
treasure_sprite = pygame.image.load("assets/treasure.png")

# Scale Sprites
hunter_sprite = pygame.transform.scale(hunter_sprite, (CELL_SIZE, CELL_SIZE))
knight_sprite = pygame.transform.scale(knight_sprite, (CELL_SIZE, CELL_SIZE))
treasure_sprite = pygame.transform.scale(treasure_sprite, (CELL_SIZE, CELL_SIZE))

# Initialize the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Knights of Eldoria")
clock = pygame.time.Clock()


class Grid:
    def __init__(self, size):
        self.size = size

    def wrap_coordinates(self, x, y):
        return x % self.size, y % self.size


class Treasure:
    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type
        self.value = {"bronze": 3, "silver": 7, "gold": 13}[treasure_type]

    def decay(self):
        self.value -= 0.1 * self.value
        if self.value <= 0:
            self.value = 0


class TreasureHunter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.stamina = 100
        self.treasure = None

    def move(self, grid, treasures, knights):
        if self.stamina > 0:
            if treasures:
                closest = min(treasures, key=lambda t: abs(self.x - t.x) + abs(self.y - t.y))
                dx = 1 if closest.x > self.x else -1 if closest.x < self.x else 0
                dy = 1 if closest.y > self.y else -1 if closest.y < self.y else 0

                for knight in knights:
                    if abs(knight.x - self.x) + abs(knight.y - self.y) <= 3:
                        dx, dy = -dx, -dy
                        break

                self.target_x, self.target_y = grid.wrap_coordinates(self.x + dx, self.y + dy)
            self.stamina -= 2
        if self.stamina <= 6:
            self.stamina += 1
        return True

    def collect_treasure(self, treasures):
        for treasure in treasures:
            if self.x == treasure.x and self.y == treasure.y and self.treasure is None:
                self.treasure = treasure
                treasures.remove(treasure)
                print(f"Hunter collected {treasure.type} treasure!")

    def update_position(self):
        if self.x != self.target_x:
            self.x += (self.target_x - self.x) * 0.2
        if self.y != self.target_y:
            self.y += (self.target_y - self.y) * 0.2


class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.energy = 100

    def patrol(self, hunters, grid):
        for hunter in hunters:
            if abs(self.x - hunter.x) + abs(self.y - hunter.y) <= 3:
                self.chase(hunter, grid)
                return hunter
        return None

    def chase(self, hunter, grid):
        dx = 1 if hunter.x > self.x else -1 if hunter.x < self.x else 0
        dy = 1 if hunter.y > self.y else -1 if hunter.y < self.y else 0
        self.target_x, self.target_y = grid.wrap_coordinates(self.x + dx, self.y + dy)
        self.energy -= 20
        if self.energy <= 20:
            self.energy += 10

    def update_position(self):
        if self.x != self.target_x:
            self.x += (self.target_x - self.x) * 0.2
        if self.y != self.target_y:
            self.y += (self.target_y - self.y) * 0.2


class Simulation:
    def __init__(self):
        self.grid = Grid(GRID_SIZE)
        self.hunters = [TreasureHunter(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in
                        range(5)]
        self.knights = [Knight(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(3)]
        self.treasures = [Treasure(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1),
                                   random.choice(["bronze", "silver", "gold"])) for _ in range(10)]
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.hunters = [hunter for hunter in self.hunters if hunter.move(self.grid, self.treasures, self.knights)]
            for hunter in self.hunters:
                hunter.collect_treasure(self.treasures)
                hunter.update_position()
            for knight in self.knights:
                knight.patrol(self.hunters, self.grid)
                knight.update_position()
            for treasure in self.treasures:
                treasure.decay()
            self.treasures = [t for t in self.treasures if t.value > 0]

            self.draw()
            clock.tick(FPS)
        pygame.quit()

    def draw(self):
        screen.fill(WHITE)
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
            pygame.draw.line(screen, GRID_COLOR, (0, x), (WINDOW_SIZE, x))
        for hunter in self.hunters:
            screen.blit(hunter_sprite, (int(hunter.x * CELL_SIZE), int(hunter.y * CELL_SIZE)))
        for knight in self.knights:
            screen.blit(knight_sprite, (int(knight.x * CELL_SIZE), int(knight.y * CELL_SIZE)))
        for treasure in self.treasures:
            screen.blit(treasure_sprite, (treasure.x * CELL_SIZE, treasure.y * CELL_SIZE))
        pygame.display.flip()


def main():
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()
