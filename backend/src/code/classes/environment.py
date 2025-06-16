import random

class Environment:
    def __init__(self, width, height, food_chemical_structure, food_spawn_amount, num_of_diffusion_blocks, diffusion_rate):
        self.width = width
        self.height = height
        self.env = [[{'chemicals': {}, 'block': None} for _ in range(width)] for _ in range(height)]
        self.food_chemical_structure = food_chemical_structure
        self.food_spawn_amount = food_spawn_amount
        self.num_of_diffusion_blocks = num_of_diffusion_blocks
        self.diffusion_rate = diffusion_rate

    def spawn_food(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)

        if self.food_chemical_structure in self.env[y][x]['chemicals']:
            self.env[y][x]['chemicals'][self.food_chemical_structure] += self.food_spawn_amount
        else:
            self.env[y][x]['chemicals'][self.food_chemical_structure] = self.food_spawn_amount

    def diffuse(self):
        changes = [[{chemical: 0 for chemical in self.env[i][j]['chemicals']} for j in range(self.width)] for i in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                chemicals = self.env[i][j]['chemicals']
                if chemicals:
                    for chemical, chemical_amount in chemicals.items():
                        diffusion_amount = (chemical_amount / self.num_of_diffusion_blocks) * self.diffusion_rate

                        changes[i][j][chemical] -= chemical_amount * self.diffusion_rate

                        for x, y in [(i-1, j-1), (i-1, j), (i-1, j+1),
                                     (i, j-1),               (i, j+1),
                                     (i+1, j-1), (i+1, j), (i+1, j+1)]:
                            if 0 <= x < self.height and 0 <= y < self.width:
                                if chemical not in changes[x][y]:
                                    changes[x][y][chemical] = 0
                                changes[x][y][chemical] += diffusion_amount

        for i in range(self.height):
            for j in range(self.width):
                for chemical, change_amount in changes[i][j].items():
                    if chemical not in self.env[i][j]['chemicals']:
                        self.env[i][j]['chemicals'][chemical] = 0
                    self.env[i][j]['chemicals'][chemical] += change_amount

    def print_env(self):
        for row in self.env:
            for unit in row:
                if unit['block']:
                    print('x', end='')
                else:
                    print('.', end='')
            print()

    def place_blocks(self, blocks):
        for block in blocks:
            placed = False
            while not placed:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if not self.env[y][x]['block']:
                    block.x = x
                    block.y = y
                    self.env[y][x]['block'] = block
                    placed = True

    def randomly_move_blocks(self, blocks, moving_base_cost):
        moves = []
        for block in blocks:
            x, y = block.x, block.y
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            x2, y2 = x + dx, y + dy

            if 0 <= x2 < self.width and 0 <= y2 < self.height and not self.env[y2][x2]['block']:
                moves.append((block, x2, y2))
                block.energy -= moving_base_cost

        for block, x2, y2 in moves:
            self.env[block.y][block.x]['block'] = None
            block.x = x2
            block.y = y2
            self.env[y2][x2]['block'] = block

    def blocks_eat(self, blocks, eat_rate, energy_conversion_rate):
        for block in blocks:
            cell = self.env[block.y][block.x]
            if block and cell['chemicals']:
                for chemical, amount in list(cell['chemicals'].items()):
                    consume_amount = min(eat_rate, amount)
                    cell['chemicals'][chemical] -= consume_amount
                    if cell['chemicals'][chemical] <= 0:
                        del cell['chemicals'][chemical]
                    block.energy += consume_amount * energy_conversion_rate

    def check_death(self, blocks, step_base_cost):
        for block in blocks:
            block.energy -= step_base_cost
            if block.energy <= 0:
                self.env[block.y][block.x]['block'] = None
                blocks.remove(block)  # Be cautious with modifying the list while iterating
