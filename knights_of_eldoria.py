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


# Testing the Grid, Treasure, and TreasureHunter classes
if __name__ == "__main__":
    grid = Grid(10)
    treasure = Treasure(2, 3, "gold")
    hunter = TreasureHunter(0, 0, "navigation")

    print("Grid initialized with size 10x10.")
    print(f"Treasure placed at ({treasure.x}, {treasure.y}) with value {treasure.value}.")
    print(f"Hunter initialized at ({hunter.x}, {hunter.y}) with skill {hunter.skill}.")
