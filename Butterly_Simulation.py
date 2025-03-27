import random
import logging
import csv

# Constants for symbols
SYMBOL_SC = '!'
SYMBOL_MC = '$'
SYMBOL_LC = '&'
SYMBOL_BUTTERFLY = 'B'
SYMBOL_LEAF = '*'
SYMBOL_EMPTY = '.'

# Set up logging for debugging
logging.basicConfig(filename='simulation_debug.log', level=logging.DEBUG)

def simulation(
    grid_width=15,
    grid_height=15,
    initial_sc=10,
    initial_mc=5,
    initial_lc=3,
    initial_leaves=15,
    ticks=1000,
    sc_hunger_death_prob=0.01,
    mc_hunger_revert_prob=0.03,
    lc_to_butterfly_prob=0.05,
    lc_hunger_revert_prob=0.05,
    leaf_generation_prob=0.01,
    butterfly_sc_prob=0.2,
    butterfly_death_prob=0.02,
    log_file='simulation_population_log.csv'
):
    # Entities
    class Entity:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def move(self, grid, moved_entities):
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height and not grid[nx][ny]:
                    grid[self.x][self.y] = None
                    self.x = nx
                    self.y = ny
                    grid[self.x][self.y] = self
                    moved_entities.add((self.x, self.y))
                    break

    class Caterpillar(Entity):
        def __init__(self, x, y):
            super().__init__(x, y)
            self.hunger_ticks = 0

    class SmallCaterpillar(Caterpillar):
        def __init__(self, x, y):
            super().__init__(x, y)

        def act(self, grid, moved_entities):
            self.hunger_ticks += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height and isinstance(grid[nx][ny], Leaf):
                    logging.debug(f'Small Caterpillar at ({self.x},{self.y}) ate a leaf at ({nx},{ny}).')
                    grid[nx][ny] = MediumCaterpillar(nx, ny)
                    grid[self.x][self.y] = None
                    moved_entities.add((nx, ny))
                    return
            if random.random() < sc_hunger_death_prob:
                logging.debug(f'Small Caterpillar at ({self.x},{self.y}) died of hunger.')
                grid[self.x][self.y] = None
            else:
                self.move(grid, moved_entities)

    class MediumCaterpillar(Caterpillar):
        def __init__(self, x, y):
            super().__init__(x, y)

        def act(self, grid, moved_entities):
            self.hunger_ticks += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height:
                    if isinstance(grid[nx][ny], Leaf):
                        logging.debug(f'Medium Caterpillar at ({self.x},{self.y}) ate a leaf at ({nx},{ny}).')
                        grid[nx][ny] = LargeCaterpillar(nx, ny)
                        grid[self.x][self.y] = None
                        moved_entities.add((nx, ny))
                        return
                    elif isinstance(grid[nx][ny], SmallCaterpillar):
                        logging.debug(f'Medium Caterpillar at ({self.x},{self.y}) ate a Small Caterpillar at ({nx},{ny}).')
                        grid[nx][ny] = LargeCaterpillar(nx, ny)
                        grid[self.x][self.y] = None
                        moved_entities.add((nx, ny))
                        return
            if random.random() < mc_hunger_revert_prob:
                logging.debug(f'Medium Caterpillar at ({self.x},{self.y}) reverted to Small Caterpillar due to hunger.')
                grid[self.x][self.y] = SmallCaterpillar(self.x, self.y)
            else:
                self.move(grid, moved_entities)

    class LargeCaterpillar(Caterpillar):
        def __init__(self, x, y):
            super().__init__(x, y)

        def act(self, grid, moved_entities):
            self.hunger_ticks += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height:
                    if isinstance(grid[nx][ny], Leaf):
                        logging.debug(f'Large Caterpillar at ({self.x},{self.y}) ate a leaf at ({nx},{ny}).')
                        grid[nx][ny] = LargeCaterpillar(nx, ny)
                        grid[self.x][self.y] = None
                        moved_entities.add((nx, ny))
                        return
                    elif isinstance(grid[nx][ny], SmallCaterpillar):
                        logging.debug(f'Large Caterpillar at ({self.x},{self.y}) ate a Small Caterpillar at ({nx},{ny}).')
                        grid[nx][ny] = LargeCaterpillar(nx, ny)
                        grid[self.x][self.y] = None
                        moved_entities.add((nx, ny))
                        return
                    elif isinstance(grid[nx][ny], MediumCaterpillar):
                        logging.debug(f'Large Caterpillar at ({self.x},{self.y}) ate a Medium Caterpillar at ({nx},{ny}).')
                        grid[nx][ny] = LargeCaterpillar(nx, ny)
                        grid[self.x][self.y] = None
                        moved_entities.add((nx, ny))
                        return
            if random.random() < lc_to_butterfly_prob:
                logging.debug(f'Large Caterpillar at ({self.x},{self.y}) became a Butterfly due to no food.')
                grid[self.x][self.y] = Butterfly(self.x, self.y)
            elif random.random() < lc_hunger_revert_prob:
                logging.debug(f'Large Caterpillar at ({self.x},{self.y}) reverted to Medium Caterpillar due to hunger.')
                grid[self.x][self.y] = MediumCaterpillar(self.x, self.y)
            else:
                self.move(grid, moved_entities)

    class Butterfly(Entity):
        def __init__(self, x, y):
            super().__init__(x, y)
            self.hunger_ticks = 0  # Add hunger_ticks for butterflies

        def act(self, grid, moved_entities):
            self.hunger_ticks += 1
            # Check surrounding cells for leaves
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height and isinstance(grid[nx][ny], Leaf):
                    logging.debug(f'Butterfly at ({self.x},{self.y}) ate a leaf at ({nx},{ny}).')
                    grid[nx][ny] = None  # Remove the leaf
                    self.hunger_ticks = 0  # Reset hunger_ticks upon eating
                    if random.random() < butterfly_sc_prob:
                        logging.debug(f'Butterfly at ({self.x},{self.y}) left behind a Small Caterpillar at ({nx},{ny}).')
                        grid[nx][ny] = SmallCaterpillar(nx, ny)
                        moved_entities.add((nx, ny))
                    else:
                        self.move(grid, moved_entities)
                    return
            if random.random() < butterfly_death_prob:
                logging.debug(f'Butterfly at ({self.x},{self.y}) died.')
                grid[self.x][self.y] = None
            else:
                self.move(grid, moved_entities)

    class Leaf(Entity):
        def __init__(self, x, y):
            super().__init__(x, y)

        def act(self, grid, moved_entities):
            pass

    # Initialize grid
    grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

    # Function to place initial entities on the grid
    def place_entity(entity_class, count):
        placed = 0
        while placed < count:
            x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
            if grid[x][y] is None:
                grid[x][y] = entity_class(x, y)
                placed += 1

    # Place initial entities
    place_entity(SmallCaterpillar, initial_sc)
    place_entity(MediumCaterpillar, initial_mc)
    place_entity(LargeCaterpillar, initial_lc)
    place_entity(Leaf, initial_leaves)

    # Function to print the grid
    def print_grid(grid):
        entity_symbols = {
            SmallCaterpillar: SYMBOL_SC,
            MediumCaterpillar: SYMBOL_MC,
            LargeCaterpillar: SYMBOL_LC,
            Butterfly: SYMBOL_BUTTERFLY,
            Leaf: SYMBOL_LEAF,
            None: SYMBOL_EMPTY
        }
        for row in range(grid_height):
            line = ""
            for col in range(grid_width):
                cell = grid[col][row]
                line += entity_symbols[type(cell)] + " " if cell else SYMBOL_EMPTY + " "
            print(line)
        print('-' * (grid_width * 2))

    # Function to log population counts
    def log_population(grid, tick, csv_writer):
        population_counts = {
            SmallCaterpillar: 0,
            MediumCaterpillar: 0,
            LargeCaterpillar: 0,
            Butterfly: 0,
            Leaf: 0
        }

        for row in range(grid_height):
            for col in range(grid_width):
                cell = grid[col][row]
                if cell:
                    population_counts[type(cell)] += 1

        csv_writer.writerow([tick, population_counts[SmallCaterpillar], population_counts[MediumCaterpillar], population_counts[LargeCaterpillar], population_counts[Butterfly], population_counts[Leaf]])

    # Log csv headers
    with open(log_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Tick', 'SmallCaterpillars', 'MediumCaterpillars', 'LargeCaterpillars', 'Butterflies', 'Leaves'])

        # Log initial conditions
        logging.info(f"Starting simulation with grid size ({grid_width}x{grid_height})")
        logging.info(f"Initial small caterpillars: {initial_sc}")
        logging.info(f"Initial medium caterpillars: {initial_mc}")
        logging.info(f"Initial large caterpillars: {initial_lc}")
        logging.info(f"Initial leaves: {initial_leaves}")

        # Simulation loop
        for tick in range(ticks):
            log_population(grid, tick + 1, csv_writer)
            print(f"Tick {tick + 1}:")
            print_grid(grid)

            moved_entities = set()
            entities_to_act = [(x, y) for x in range(grid_width) for y in range(grid_height) if grid[x][y]]

            # Let each entity act
            for x, y in entities_to_act:
                if (x, y) in moved_entities:
                    continue
                entity = grid[x][y]
                if entity:
                    entity.act(grid, moved_entities)

            # Generate new leaves
            for _ in range(grid_width * grid_height):
                if random.random() < leaf_generation_prob:
                    x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
                    if grid[x][y] is None:
                        grid[x][y] = Leaf(x, y)

if __name__ == "__main__":
    simulation()