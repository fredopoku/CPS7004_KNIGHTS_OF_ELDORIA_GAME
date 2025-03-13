import random


class Grid:
    """
    Represents the kingdom of Eldoria as a 2D grid.
    The grid wraps around at the edges.
    """

    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def wrap_coordinates(self, x, y):
        """Ensure coordinates wrap around the grid edges."""
        return x % self.size, y % self.size


class Treasure:
    """Represents a piece of treasure with decay mechanics."""

    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type
        self.value = {"bronze": 3, "silver": 7, "gold": 13}[treasure_type]

    def decay(self):
        """Reduces the treasure's value by 0.1% per step."""
        self.value -= 0.1 * self.value
        if self.value <= 0:
            self.value = 0


class TreasureHunter:
    """Represents a treasure hunter who collects treasure and manages stamina."""

    def __init__(self, x, y, skill):
        self.x = x
        self.y = y
        self.stamina = 100
        self.skill = skill
        self.treasure = None

    def find_closest_treasure(self, treasures):
        """Find the closest treasure and move towards it."""
        if not treasures:
            return None
        closest = min(treasures, key=lambda t: abs(self.x - t.x) + abs(self.y - t.y))
        dx = 1 if closest.x > self.x else -1 if closest.x < self.x else 0
        dy = 1 if closest.y > self.y else -1 if closest.y < self.y else 0
        return dx, dy

    def move(self, grid, treasures):
        """Move towards treasure instead of randomly moving."""
        if self.stamina > 0:
            direction = self.find_closest_treasure(treasures)
            if direction:
                dx, dy = direction
                self.x, self.y = grid.wrap_coordinates(self.x + dx, self.y + dy)
            self.stamina -= 2
        if self.stamina <= 0:
            print(f"Hunter at ({self.x}, {self.y}) has collapsed.")
            return False  # Hunter is removed
        return True

    def collect_treasure(self, treasures):
        """Pick up treasure if on the same location."""
        for treasure in treasures:
            if self.x == treasure.x and self.y == treasure.y and self.treasure is None:
                self.treasure = treasure
                treasures.remove(treasure)
                print(f"Hunter collected {treasure.type} treasure!")


class Knight:
    """Represents a knight who patrols and chases hunters."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100

    def patrol(self, hunters, grid):
        """Look for hunters and chase if within a 3-cell radius."""
        for hunter in hunters:
            if abs(self.x - hunter.x) + abs(self.y - hunter.y) <= 3:
                self.chase(hunter, grid)
                return hunter
        return None

    def chase(self, hunter, grid):
        """Move towards the detected hunter and drain energy."""
        dx = 1 if hunter.x > self.x else -1 if hunter.x < self.x else 0
        dy = 1 if hunter.y > self.y else -1 if hunter.y < self.y else 0
        self.x, self.y = grid.wrap_coordinates(self.x + dx, self.y + dy)
        self.energy -= 20
        print(f"Knight is chasing hunter at ({hunter.x}, {hunter.y})")


class Simulation:
    """Controls the game flow and updates all entities."""

    def __init__(self, grid_size=20, max_steps=100000):
        self.grid = Grid(grid_size)
        self.hunters = [TreasureHunter(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1), "navigation")
                        for _ in range(5)]
        self.knights = [Knight(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(3)]
        self.treasures = [Treasure(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1),
                                   random.choice(["bronze", "silver", "gold"])) for _ in range(10)]
        self.steps = 0
        self.max_steps = max_steps

    def run(self):
        """Runs the simulation step by step."""
        print(
            f"Starting simulation with {len(self.hunters)} hunters, {len(self.treasures)} treasures, and {len(self.knights)} knights.")

        while self.treasures and self.hunters and self.steps < self.max_steps:
            self.steps += 1
            print(f"\nSimulation Step {self.steps}")

            self.hunters = [hunter for hunter in self.hunters if hunter.move(self.grid, self.treasures)]
            for hunter in self.hunters:
                hunter.collect_treasure(self.treasures)

            for knight in self.knights:
                captured_hunter = knight.patrol(self.hunters, self.grid)
                if captured_hunter:
                    self.hunters.remove(captured_hunter)
                    print("A hunter was eliminated!")

            for treasure in self.treasures:
                treasure.decay()

            self.treasures = [t for t in self.treasures if t.value > 0]

            if not self.hunters:
                print("All hunters have been eliminated! Simulation Over.")
                break

        print("Simulation ended after", self.steps, "steps.")


# Running the simulation
def main():
    simulation = Simulation(grid_size=20, max_steps=100000)
    simulation.run()


if __name__ == "__main__":
    main()
