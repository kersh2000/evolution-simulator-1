from itertools import product
import os
import random, math
from .classes.block import Block
from .classes.pfs import PFS
from .functions import functions

current_directory = os.path.dirname(os.path.abspath(__file__))
filename = 'interactions.json'
file_path = os.path.join(current_directory, filename)
load_file = True

pfs = PFS()

# Dogma variables
genome_length = 1000
genomic_base_num = 3
codon_length = 3
proteomic_base_num = 10
food_chemical_structure = "ABABA"
chemical_base_num = 3
protein_codon_factor = 2
codon_mapping_method = "non-linear"
codon_map = {}
binding_exponent = 3
upper_binding_prob = 0.9
lower_binding_prob = 0.1
num_of_binding_intervals = 3
binding_map = {}
energy_conversion_rate = 25
mitosis_base_cost = 100
mitosis_base_mutation_rate = 0.002
moving_base_cost = 100
protein_synthesis_base_cost = 100
step_base_cost = 100
eat_rate = 500

base_mutation_rate = 0.0005
width = 20
height = 20
food_spawn_rate = 0.1
food_spawn_amount = 10000
concentration_limit = 0.001
diffusion_rate = 0.01
num_of_diffusion_blocks = 26
num_of_blocks = 200
starting_energy = 50000


a_conversion_rate = 2
env = []
blocks = []
chemical_bases = []
binding_intervals = [0.95, 0.7, 0.5, 0.3, 0.1]
global_average_food_binding_prob = 0
global_food_prob_sum = 0

conversion_rates = {
    "A-B": 8,
    "A-C": 2,
    "B-A": -10,
    "B-C": 20,
    "C-A": 30,
    "C-B": -1
}

total_concs = []

def create_env():
    
    for row in env:
        for unit in row:
            unit["chemicals"] = {}
            unit["block"] = {}

def spawn_food():
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)

    if food_chemical_structure in env[y][x]["chemicals"]:
        env[y][x]["chemicals"][food_chemical_structure] += food_spawn_amount
    else:
        env[y][x]["chemicals"][food_chemical_structure] = food_spawn_amount

def diffuse():
    # Clear chemicals under concentration limit:
    for i in range(len(env)):
        for j in range(len(env[0])):
            chemicals = env[i][j]["chemicals"]
            remove_chemicals = []
            for chemical, amount in chemicals.items():
                if amount < concentration_limit:
                    remove_chemicals.append(chemical)
            for remove in remove_chemicals:
                env[i][j]["chemicals"].pop(remove)
            
            if env[i][j]["block"]:
                metabolites = env[i][j]["block"].metabolome
                remove_metabolites = []
                for metabolite, amount in metabolites.items():
                    if amount < concentration_limit:
                        remove_metabolites.append(metabolite)
                for remove in remove_metabolites:
                    env[i][j]["block"].metabolome.pop(remove)
    # Initialize a temporary structure to store changes
    changes = [[{chemical: 0 for chemical in env[i][j]["chemicals"]} for j in range(len(env[0]))] for i in range(len(env))]

    for i in range(len(env)):
        for j in range(len(env[0])):
            chemicals = env[i][j]["chemicals"]
            if chemicals:
                for chemical, chemical_amount in chemicals.items():
                    # Now, consider 8 neighbors for diffusion
                    diffusion_amount = (chemical_amount / num_of_diffusion_blocks) * diffusion_rate  # Dividing by 16 for 8 neighbors

                    # Subtract the total diffused amount from the original cell
                    changes[i][j][chemical] -= chemical_amount * diffusion_rate  # Multiplying by 16 for 8 neighbors

                    # Accumulate the diffusion amount to all 8 adjacent cells in the changes structure
                    for x, y in [(i-1, j-1), (i-1, j), (i-1, j+1),
                                 (i, j-1),               (i, j+1),
                                 (i+1, j-1), (i+1, j), (i+1, j+1)]:
                        if 0 <= x < len(env) and 0 <= y < len(env[0]):
                            if chemical not in changes[x][y]:
                                changes[x][y][chemical] = 0
                            changes[x][y][chemical] += diffusion_amount

    # Apply the accumulated changes to the environment
    for i in range(len(env)):
        for j in range(len(env[0])):
            for chemical, change_amount in changes[i][j].items():
                if chemical not in env[i][j]["chemicals"]:
                    env[i][j]["chemicals"][chemical] = 0
                env[i][j]["chemicals"][chemical] += change_amount

def begining():
    global blocks, env, total_concs
    Block.set_codons(genomic_base_num, codon_length)
    blocks = []
    env = [[{} for _ in range(width)] for _ in range(height)]
    total_concs = []
    # Create env
    create_env()
    create_maps(loadfile=load_file)
    # Create blocks "fddabc"
    print(codon_map)
    desired_proteins = [
        "bhbhdcbgabc", # Replicase (abc): egeg = binding sequence, d = binding threshold, cbg = amount threshold
        "feeefdddbdb", #Transportase (bdb): f = substrate length entering, eee = substrate amount limit entering, f = substrate length exiting, ddd = substrate amount limit exiting
        "ccdddcac", # Digestase (cac): g = conversion rate, c = number of A's digested, ddd = substrate amount limit
        "bhbhdcbgabc", # Replicase Duplicate 1 (abc)
        # Diversity
        "________abc", # Replicase (abc): egeg = binding sequence, d = binding threshold, cbg = amount threshold
        "________bdb", # Transportase (bdb): f = substrate length, eee = substrate amount limit, f = substrate length exiting, ddd = substrate amount limit exiting
        "_____cac", # Digestase (cac): g = conversion rate, c = number of A's digested, ddd = substrate amount limit
        "______________cba", # Convertase (cba)
        "______________cba", # Convertase (cba)
        "______________cba", # Convertase (cba)
    ]
    desired_genes = functions.reverse_transcript_proteins(desired_proteins, codon_map, Block.end_codon, Block.start_codon, join_genes=True)
    inserted_genome = "xxxxxxxxx" + desired_genes + "000xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx010002001222"
    for i in range(num_of_blocks):
        block = Block(genome_length, genomic_base_num, inserted_genome)
        block.energy = starting_energy
        block.colour = number_string_to_color(genomic_base_num, len(block.genome), block.genome)
        block.create_proteome(block.find_transcriptions(), codon_map)
        blocks.append(block)
    # Place blocks
    place_blocks(env, blocks)

def setup(env_data):
    global blocks, env
    Block.set_codons(genomic_base_num, codon_length)
    blocks = []
    env = [[{} for _ in range(width)] for _ in range(height)]
    # Create env
    for i in range(len(env_data)):
        for j in range(len(env_data[0])):
            env[i][j]["chemicals"] = env_data[i][j]["chemicals"]
            block_data = env_data[i][j]["block"]
            if block_data:
                block = Block(genome=block_data["genome"])
                block.colour = block_data["colour"]
                block.x = block_data["x"]
                block.y = block_data["y"]
                block.proteome = block_data["proteome"]
                block.energy = block_data["energy"]
                block.metabolome = block_data["metabolome"]
                blocks.append(block)
            else:
                block = {}
            env[i][j]["block"] = block
    create_maps(loadfile=True)

def place_blocks(env, blocks):
    for block in blocks:
        placed = False
        while not placed:
            # Generate random coordinates within the environment
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Place the block if the spot is not occupied
            if not env[y][x]["block"]:
                block.x = x
                block.y = y
                env[y][x]["block"] = block
                placed = True

def randomly_move_blocks():
    moves = []  # Store intended moves here

    # First, determine all moves without actually moving anything
    for y in range(height):
        for x in range(width):
            if env[y][x]["block"]:
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random direction
                x2, y2 = x + dx, y + dy

                # Check if the new position is valid and add to the moves list
                if 0 <= x2 < width and 0 <= y2 < height and not env[y2][x2]["block"]:
                    moves.append((x, y, x2, y2))  # Add the current and new positions
                    env[y][x]["block"].energy -= moving_base_cost

    # Now, execute all collected moves
    for x1, y1, x2, y2 in moves:
        move_block(x1, y1, x2, y2)

def move_block(x1, y1, x2, y2):
    if (x2 < 0 or x2 > width - 1 or y2 < 0 or y2 > height - 1):
        return

    if (not env[y2][x2]["block"]):
        env[y2][x2]["block"] = env[y1][x1]["block"]
        env[y2][x2]["block"].x = x2
        env[y2][x2]["block"].y = y2
        env[y1][x1]["block"] = {}
    
def print_blocks():
    for row in env:
        for unit in row:
            if unit["block"]:
                print("x", end="")
            else:
                print(".", end="")
        print()

def blocks_eat():
    for i in range(len(env)):
        for j in range(len(env[0])):
            block = env[i][j]["block"]
            chemicals = env[i][j]["chemicals"]
            
            if block and chemicals:
                for chemical, amount in chemicals.items():
                    if (not chemical in block.probs_summary):
                        continue
                    # Determine the amount to consume, limited by the eat_rate and available amount
                    consume_amount = min(eat_rate * block.probs_summary[chemical], amount)
                    # Update the chemical amount in the environment
                    chemicals[chemical] -= consume_amount
                    if (chemicals[chemical] == 0):
                        chemicals = {}
                    
                    # Increase the block's energy based on the consumed amount and conversion rate
                    block.energy += consume_amount * energy_conversion_rate
                    # By-product
                    if "BB" not in block.metabolome:
                        block.metabolome["BB"] = consume_amount
                    else:
                        block.metabolome["BB"] += consume_amount

def kill():
    for i in range(len(env)):
        for j in range(len(env[0])):
            block = env[i][j]["block"]
            
            if block:
                block.energy -= step_base_cost
                if block.energy <= 0:
                    env[i][j]["block"] = {}

def clone(block):
    inherited_genome = mutate_genome(block.genome, mitosis_base_mutation_rate)
    daughter = Block(genome=inherited_genome)
    daughter.colour = block.colour
    daughter.x = block.x
    daughter.y = block.y
    daughter.proteome = block.proteome
    return daughter

def mutate_genome(genome, mutation_rate):
    mutated_genome = ""
    for base in genome:
        chance = random.random()
        if (chance < mutation_rate):
            mutated_base = random.choice([str(base) for base in range(0, genomic_base_num)])
            mutated_genome += mutated_base
        else:
            mutated_genome += base
    return mutated_genome

def mitosis():
    new_blocks = []
    for y in range(height):
        for x in range(width):
            block = env[y][x]["block"]
            if block:
                if "Replicase" in block.activities:
                    for row in block.activities["Replicase"]:
                        chance = pfs.replicase(row["protein"], row["sequence_index"], binding_map, binding_exponent, block.metabolome, proteomic_base_num)
                        if chance:
                            # Check surrounding cells for an empty space
                            for dy in [-1, 0, 1]:
                                for dx in [-1, 0, 1]:
                                    if not (dx == 0 and dy == 0):  # Skip the current block's position
                                        new_x, new_y = x + dx, y + dy
                                        # Check if the new position is within the grid and empty
                                        if 0 <= new_x < width and 0 <= new_y < height and not env[new_y][new_x]["block"]:
                                            block.energy -= mitosis_base_cost
                                            # Create a daughter block
                                            daughter_block = clone(block)
                                            # Divide resources
                                            block.energy /= 2  # Split energy into 2
                                            # Split metabolome into 2
                                            for metabolite in block.metabolome:
                                                block.metabolome[metabolite] /= 2

                                            # Inherit devided resources
                                            daughter_block.energy = block.energy
                                            daughter_block.metabolome = block.metabolome

                                            new_blocks.append((new_y, new_x, daughter_block))
                                            break  # Stop looking for empty spaces after one is found
                                if new_blocks and new_blocks[-1][2] == daughter_block:  # If a daughter block was just added
                                    break  # Stop checking other surrounding cells
                        else:
                            continue

    # Add new blocks to the environment
    for y, x, new_block in new_blocks:
        new_block.x = x
        new_block.y = y
        env[y][x]["block"] = new_block

def digest():
    pass

def step():
    create_maps(loadfile=True)
    single_chemical_count = {}
    for row in env:
        for unit in row:
            # Count chemicals
            if unit["chemicals"]:
                for chemical_string, chemical_value in unit["chemicals"].items():
                    if chemical_string in single_chemical_count:
                        single_chemical_count[chemical_string] += chemical_value
                    else:
                        single_chemical_count[chemical_string] = chemical_value
    total_concs.append(single_chemical_count)
    for row in env:
        for unit in row:
            if unit["block"]:
                block = unit["block"]
                # Mutate genome
                block.genome = mutate_genome(block.genome, base_mutation_rate)
                # Create proteome
                transcriptome = block.find_transcriptions()
                block.create_proteome(transcriptome, codon_map)
                block.function_proteome()
                # Chemical functions
                if unit["chemicals"]:
                    chemicals = unit["chemicals"]
                    # block.probs = {}
                    block.probs_summary = {}
                    for chemical in chemicals:
                        # Generate protein-chemical interaction porbabilities
                        summary_none = 1
                        for protein in block.proteome:
                            binding_outcome = binding_formula(chemical, protein)
                            # block.probs[f"{protein}-{chemical}"] = binding_outcome
                            summary_none *= (1 - binding_outcome["__total__"])
                        block.probs_summary[chemical] = (1 - summary_none)
                    # Absorb surrounding chemicals
                    if "Transportase" in block.activities:
                        for row in block.activities["Transportase"]:
                            chemical_changes = pfs.transportase(row["protein"], row["sequence_index"], chemicals, block.metabolome, proteomic_base_num)
                            for chemical_structure, amount in chemical_changes.items():
                                if chemical_structure in chemicals:
                                    chemicals[chemical_structure] = max(amount + chemicals[chemical_structure], 0)
                                else:
                                    chemicals[chemical_structure] = max(amount, 0)
                                if chemical_structure in block.metabolome:
                                    block.metabolome[chemical_structure] = max(block.metabolome[chemical_structure] - amount, 0)
                                else:
                                    block.metabolome[chemical_structure] = max(amount, 0)
                # Conver metabolites
                if "Convertase" in block.activities:
                    for row in block.activities["Convertase"]:
                        convertase_sequence = row["protein"]
                        convertase_index = row["sequence_index"]
                        new_metabolome, new_energy = pfs.convertase(convertase_sequence, convertase_index, block.metabolome, proteomic_base_num, [chr(64 + i) for i in range(1, chemical_base_num + 1)], conversion_rates, binding_map, binding_exponent)
                        block.metabolome = new_metabolome
                        block.energy += new_energy
                # Digest metabolites
                if "Digestase" in block.activities:
                    new_metabolome, new_energy = pfs.digestase(block.activities["Digestase"][0]["protein"], block.activities["Digestase"][0]["sequence_index"], block.metabolome, proteomic_base_num, a_conversion_rate)
                    block.metabolome = new_metabolome
                    block.energy += new_energy
                # # Slightly leak metabolites        
                # if block.metabolome:
                #     chemicals = unit["chemicals"]
                #     for metabolite, amount in block.metabolome.items():
                #         removal_amount = amount * 0.1
                #         if not metabolite in chemicals:
                #             chemicals[metabolite] = 0
                #         chemicals[metabolite] += removal_amount
                #         block.metabolome[metabolite] -= removal_amount


                

    # print_blocks()
    # move blocks
    randomly_move_blocks()
    # diffuse chemicals
    diffuse()
    # spawn new food
    food_rand_num = random.random()
    if food_rand_num < food_spawn_rate:
        spawn_food()
    # check death
    kill()
    # mitosis
    mitosis()
    return

def number_string_to_color(num_range, length, num_string):
    # Ensure the string length matches the expected length
    if len(num_string) != length:
        raise ValueError("The length of the number string does not match the expected length.")
    
    # Convert the string to a single number
    base = num_range  # The base depends on the number range
    num = int(num_string, base)

    # Normalize and scale the number
    max_num = base**length - 1
    normalized = num / max_num
    color_int = int(normalized * 0xFFFFFF)

    # Convert to a hexadecimal color code
    color_code = f"#{color_int:06x}"
    return color_code

def generate_dna_codons():
    # Generate all possible combinations of DNA bases
    bases = map(str, range(genomic_base_num))  # Convert each base to string for concatenation
    all_codons = [''.join(codon) for codon in product(bases, repeat=codon_length)]
    
    # Start from the second base (index 1) and get x codons
    return all_codons[1:1 + (proteomic_base_num * protein_codon_factor)]

def generate_intervals(upper, lower, intervals):
    # Calculate the step size
    step = (upper - lower) / (intervals + 1)

    # Generate the numbers using a list comprehension
    # The step needs to be negative if upper is greater than lower
    numbers = [upper - step * i for i in range(intervals + 2)]

    return numbers

import json

def save_interactions(interactions):
    with open(file_path, 'w') as file:
        json.dump(interactions, file)

def load_interactions():
    with open(file_path, 'r') as file:
        return json.load(file)

def create_maps(loadfile = False):
    global binding_map, binding_intervals, chemical_bases
    protein_bases = [chr(96 + i) for i in range(1, proteomic_base_num + 1)]
    counter = 0
    dna_codons = generate_dna_codons()
    for codon in dna_codons:
        codon_map[codon] = protein_bases[counter]
        if(counter == len(protein_bases) - 1):
            counter = -1
        counter += 1

    if len(binding_intervals) == 0:
        binding_intervals = generate_intervals(upper_binding_prob, lower_binding_prob, num_of_binding_intervals)
    chemical_bases = [chr(64 + i) for i in range(1, chemical_base_num + 1)]

    if loadfile:
        binding_map = load_interactions()
        return

    for chemical in chemical_bases:
        # Initialize all protein bases for this chemical with a binding probability of 0
        binding_map[chemical] = {protein: 0 for protein in protein_bases}

        # Create a randomly ordered list of protein bases
        randomized_proteins = random.sample(protein_bases, len(protein_bases))

        # Assign the binding probabilities to the first n protein bases in the randomized list
        for i, protein in enumerate(randomized_proteins):
            if i < len(binding_intervals):
                binding_map[chemical][protein] = binding_intervals[i]

    save_interactions(binding_map)

def binding_formula(chemical, protein):
    binding_sequences = {}
    total_prob_none = 1
    for i in range(len(protein) - (len(chemical) - 1)):
        sum_of_probs = 0
        protein_binding_site = f"{i}-"
        for j in range(len(chemical)):
            sum_of_probs += binding_map[chemical[j]][protein[i + j]]
        protein_binding_site += f"{i + (len(chemical) - 1)}"
        prob = (sum_of_probs / len(chemical)) ** binding_exponent
        binding_sequences[protein_binding_site] = prob
        total_prob_none *= (1 - prob)
    binding_sequences["__total__"] = 1 - total_prob_none
    return binding_sequences

def find_binding_chance(concentration_, binding_affinity, num_of_binders=1, k=1, x0=100):

    # Base activation probability based on concentration
    base_probability = 1 / (1 + math.exp(-k * (concentration_ - x0)))

    # Adjust the probability based on the binding affinity and number of binders
    adjusted_probability = 1 - (1 - (base_probability * binding_affinity)) ** num_of_binders

    # Ensure the probability does not exceed 1
    return min(adjusted_probability, 1)


if __name__ == "__main__":
    print("running main")