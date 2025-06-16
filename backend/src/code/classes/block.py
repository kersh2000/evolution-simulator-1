from .pfs import PFS
import random


class Block():

    start_codon = ""
    end_codon = ""


    @staticmethod
    def set_codons(genomic_base_num, codon_length):
        Block.start_codon = "0" * codon_length
        Block.end_codon = str(genomic_base_num - 1) * codon_length
        Block.codon_length = codon_length


    def __init__(self, genome_length = None, genomic_base_num = None, genome = ""):
        self.genome = genome
        self.proteome = []
        self.metabolome = {}
        self.probs_summary = {}
        self.colour = ""
        self.energy = 0
        self.x = None
        self.y = None
        if genome_length:
            self.create_genome(genome_length, genomic_base_num)
        pass

    def create_genome(self, genome_length, genomic_base_num):
        bases = [str(base) for base in range(0, genomic_base_num)]
        genome = self.genome
        for i in range(genome_length):
            if i < len(genome):
                base = genome[i]
                if (base!="x"):
                    continue
                else:
                    random_base = random.choice(bases)
                    genome = genome[:i] + random_base + genome[i + 1:]
            random_base = random.choice(bases)
            genome += random_base
        self.genome = genome
    
    def find_transcriptions(self):
        transcriptions = []
        start_pos = 0

        while start_pos < len(self.genome):
            # Find the start codon if present
            start_index = self.genome.find(Block.start_codon, start_pos)
            
            # If there's no start codon, break out of the loop
            if start_index == -1:
                break
            
            # Find the end codon following the start codon
            end_index = self.genome.find(Block.end_codon, start_index + len(Block.start_codon))
            
            # If there's no end codon, break out of the loop
            if end_index == -1:
                break
            
            # Extract the segment from the start codon to the end codon
            transcription = self.genome[start_index:end_index + len(Block.end_codon)]
            
            # Append the found transcription to the results list
            if (len(transcription) <= (len(Block.start_codon) + len(Block.end_codon) + (Block.codon_length - 1))):
                start_pos = start_index + 1
                continue

            characters_to_remove = (len(transcription) - (len(Block.start_codon) + len(Block.end_codon))) % Block.codon_length
            transcriptions.append(transcription[len(Block.start_codon):(-1 * (len(Block.end_codon) + characters_to_remove))])
            
            # Update the starting position for the next search
            start_pos = start_index + 1

        return transcriptions
    
    def create_proteome(self, transcriptions, codon_map):
        proteome = []
        for transcription in transcriptions:
            protein = ""
            for index in range(0, len(transcription), 3):
                codon = transcription[index:index+3]
                if codon not in codon_map:
                    continue
                protein_base = codon_map[codon]
                protein += protein_base
            if len(protein) == 0:
                continue
            proteome.append(protein)
        self.proteome = proteome
    
    def function_proteome(self):
        self.activities = {}
        for protein in self.proteome:
            if any(seq in protein for seq in PFS.sequence_list):
                for item in PFS.map:
                    if item["sequence"] in protein and protein.find(item["sequence"]) >= item["params_upstream_range"]:
                        if not item["function"] in self.activities:
                            self.activities[item["function"]] = []
                        self.activities[item["function"]].append({
                            "protein": protein,
                            "sequence_index": protein.find(item["sequence"])
                        })
        return
    