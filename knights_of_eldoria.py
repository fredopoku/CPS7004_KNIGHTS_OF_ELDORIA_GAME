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

    def place_entity(self, entity, x, y):
        """Places an entity on the grid."""
        x, y = self.wrap_coordinates(x, y)
        self.grid[x][y] = entity
        entity.x, entity.y = x, y

    def remove_entity(self, x, y):
        """Removes an entity from the grid."""
        self.grid[x][y] = None

    def move_entity(self, entity, new_x, new_y):
        """Moves an entity to a new location, ensuring wrap-around."""
        old_x, old_y = entity.x, entity.y
        new_x, new_y = self.wrap_coordinates(new_x, new_y)

        if self.grid[new_x][new_y] is None:
            self.grid[old_x][old_y] = None
            self.grid[new_x][new_y] = entity
            entity.x, entity.y = new_x, new_y
            return True
        return False  # Cannot move if the target cell is occupied


class Treasure:
    """Represents a piece of treasure with decay mechanics."""

    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type
        self.value = {"bronze": 3, "silver": 7, "gold": 13}[treasure_type]  # Percentage increase

    def decay(self):
        """Reduces the treasure's value by 0.1% per step."""
        self.value -= 0.1 * self.value
        if self.value <= 0:
            self.value = 0  # Treasure disappears


class TreasureHunter:
    """Represents a treasure hunter who collects treasure and manages stamina."""

    def __init__(self, x, y, skill):
        self.x = x
        self.y = y
        self.stamina = 100
        self.skill = skill  # Can be 'navigation', 'endurance', or 'stealth'
        self.treasure = None
        self.memory = {"treasure": [], "hideouts": []}

    def move(self, grid, dx, dy):
        """Move in the specified direction if possible."""
        new_x, new_y = grid.wrap_coordinates(self.x + dx, self.y + dy)
        if grid.grid[new_x][new_y] is None:  # Only move if the space is empty
            self.x, self.y = new_x, new_y
            self.stamina -= 2
        if self.stamina <= 6:
            self.rest()

    def collect_treasure(self, treasures):
        """Pick up treasure if on the same location."""
        for treasure in treasures:
            if self.x == treasure.x and self.y == treasure.y and self.treasure is None:
                self.treasure = treasure
                treasures.remove(treasure)
                print(f"Hunter collected {treasure.type} treasure!")

    def rest(self):
        """Recover stamina if in a hideout."""
        self.stamina = min(100, self.stamina + 1)


class Hideout:
    """Represents a hideout where hunters can store treasure and rest."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hunters = []

    def store_treasure(self, hunter):
        """Allows a hunter to store collected treasure."""
        if hunter.treasure:
            print(f"Treasure {hunter.treasure.type} stored in hideout.")
            hunter.treasure = None

    def rest_hunters(self):
        """Allows all hunters in the hideout to regain stamina."""
        for hunter in self.hunters:
            hunter.rest()


class Knight:
    """Represents a knight who patrols and chases hunters."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
        self.target = None

    def patrol(self, hunters, grid):
        """Look for hunters and chase if within a 3-cell radius."""
        for hunter in hunters:
            if abs(self.x - hunter.x) + abs(self.y - hunter.y) <= 3:
                self.target = hunter
                self.chase(grid)
                break

    def chase(self, grid):
        """Move towards the detected hunter and drain energy."""
        if self.target:
            dx = 1 if self.target.x > self.x else -1 if self.target.x < self.x else 0
            dy = 1 if self.target.y > self.y else -1 if self.target.y < self.y else 0
            self.x, self.y = grid.wrap_coordinates(self.x + dx, self.y + dy)
            self.energy -= 20
            print(f"Knight is chasing hunter at {self.target.x}, {self.target.y}")


class Simulation:
    """Controls the game flow and updates all entities."""

    def __init__(self, grid_size=20):
        self.grid = Grid(grid_size)
        self.hunters = []
        self.knights = []
        self.hideouts = []
        self.treasures = []
        self.steps = 0

    def run(self):
        """Runs the simulation step by step."""
        while self.treasures and self.hunters:
            self.steps += 1
            print(f"Simulation Step {self.steps}")

            for hunter in self.hunters:
                hunter.move(self.grid, random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
                hunter.collect_treasure(self.treasures)

            for knight in self.knights:
                knight.patrol(self.hunters, self.grid)

            for treasure in self.treasures:
                treasure.decay()

            self.treasures = [t for t in self.treasures if t.value > 0]

            if not self.hunters:
                print("All hunters have been eliminated! Simulation Over.")
                break


# Running the simulation
def main():
    simulation = Simulation(grid_size=20)
    simulation.run()


if __name__ == "__main__":
    main()
