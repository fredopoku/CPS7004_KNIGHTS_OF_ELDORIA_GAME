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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

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
        self.stamina = 100
        self.treasure = None

    def move(self, grid, treasures):
        if self.stamina > 0:
            if treasures:
                closest = min(treasures, key=lambda t: abs(self.x - t.x) + abs(self.y - t.y))
                dx = 1 if closest.x > self.x else -1 if closest.x < self.x else 0
                dy = 1 if closest.y > self.y else -1 if closest.y < self.y else 0
                self.x, self.y = grid.wrap_coordinates(self.x + dx, self.y + dy)
            self.stamina -= 2
        if self.stamina <= 0:
            return False
        return True

    def collect_treasure(self, treasures):
        for treasure in treasures:
            if self.x == treasure.x and self.y == treasure.y and self.treasure is None:
                self.treasure = treasure
                treasures.remove(treasure)
                print(f"Hunter collected {treasure.type} treasure!")


class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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
        self.x, self.y = grid.wrap_coordinates(self.x + dx, self.y + dy)
        self.energy -= 20


class Simulation:
    def __init__(self):
        self.grid = Grid(GRID_SIZE)
        self.hunters = [TreasureHunter(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in
                        range(5)]
        self.knights = [Knight(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(3)]
        self.treasures = [Treasure(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1),
                                   random.choice(["bronze", "silver", "gold"])) for _ in range(10)]
        self.steps = 0
        self.running = True

    def run(self):
        while self.running and self.treasures and self.hunters:
            self.steps += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.hunters = [hunter for hunter in self.hunters if hunter.move(self.grid, self.treasures)]
            for hunter in self.hunters:
                hunter.collect_treasure(self.treasures)

            for knight in self.knights:
                captured_hunter = knight.patrol(self.hunters, self.grid)
                if captured_hunter:
                    self.hunters.remove(captured_hunter)

            for treasure in self.treasures:
                treasure.decay()

            self.treasures = [t for t in self.treasures if t.value > 0]

            self.draw()
            clock.tick(FPS)
        pygame.quit()

    def draw(self):
        screen.fill(WHITE)
        for hunter in self.hunters:
            pygame.draw.rect(screen, GREEN, (hunter.x * CELL_SIZE, hunter.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for knight in self.knights:
            pygame.draw.rect(screen, RED, (knight.x * CELL_SIZE, knight.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for treasure in self.treasures:
            pygame.draw.rect(screen, YELLOW, (treasure.x * CELL_SIZE, treasure.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()


def main():
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()
