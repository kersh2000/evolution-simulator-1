import math
import random
from ..functions.functions import find_binding_chance, string_to_number, string_to_normalized_number, remove_a, change_chemical

class PFS():

    map = [
        {
            "function": "Replicase",
            "sequence": "abc",
            "params_upstream_range": 8,
        },
        {
            "function": "Transportase",
            "sequence": "bdb",
            "params_upstream_range": 8
        },
        {
            "function": "Digestase",
            "sequence": "cac",
            "params_upstream_range": 5
        },
        {
            "function": "Convertase",
            "sequence": "cba",
            "params_upstream_range": 14
        }
    ]

    sequence_list = [item["sequence"] for item in map]


    @staticmethod
    def set_codons(genomic_base_num, codon_length):
        PFS.start_codon = "0" * codon_length

    @staticmethod
    def binding_formula(chemical, protein, binding_map, binding_exponent):
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


    def __init__(self):
        self.genome = ""
        
        pass

    
    def replicase(self, sequence, index, binding_map, binding_exponent, metabolome, proteomic_base_num):
        param_length = next((item['params_upstream_range'] for item in PFS.map if item['function'] == "Replicase"), None)
        param = sequence[index-param_length:index]
        p1 = param[0:4] # Substrate sequence for binding
        p2 = param[4:5] # Binding threshold
        p3 = param[5:8] # Amount threshold

        # Convert p2 and p3 to their respective numerical values
        binding_prob_limit = string_to_normalized_number(p2, proteomic_base_num)
        binding_amount_limit = string_to_number(p3, proteomic_base_num)

        for metabolite, amount in metabolome.items():
            metabolite_binding_prob = PFS.binding_formula(metabolite, p1, binding_map, binding_exponent)
            binding_chance = metabolite_binding_prob["__total__"]
            if binding_chance > binding_prob_limit and amount > binding_amount_limit:
                # print(f"Replicase condition met: \nBinding (actual > threshold): {binding_chance} > {binding_prob_limit}\nAmount (actual > threshold): {amount} > {binding_amount_limit}")
                return True  # Replication proceeds if conditions are met

        return False  # Replication does not proceed if no metabolite meets the criteria
    
    def transportase(self, sequence, index, chemicals, metabolome, proteomic_base_num):
        param_length = next((item['params_upstream_range'] for item in PFS.map if item['function'] == "Transportase"), None)
        param = sequence[index-param_length:index]
        p1 = param[0:1] # Substrate length entering
        p2 = param[1:4] # Max substrate amount entering
        p3 = param[4:5] # Substrate length exiting
        p4 = param[5:8] # Max substrate amount exiting

        substrate_length_entering = string_to_number(p1, proteomic_base_num)
        substrate_max_amount_entering = string_to_number(p2, proteomic_base_num)
        substrate_length_exiting = string_to_number(p3, proteomic_base_num)
        substrate_max_amount_exiting = string_to_number(p4, proteomic_base_num)

        substrate_changes = {}
        chemicals_entering = {}
        metabolites_exiting = {}

        chemicals_entering_names = []
        metabolites_exiting_names = []


        for chemical, amount in chemicals.items():
            if (substrate_length_entering >= len(chemical)):
                chemicals_entering_names.append(chemical)
                chemicals_entering[chemical] = min(amount, substrate_max_amount_entering)/2

        for metabolite, amount in metabolome.items():
            if (substrate_length_exiting >= len(metabolite)):
                metabolites_exiting_names.append(metabolite)
                metabolites_exiting[metabolite] = min(amount, substrate_max_amount_exiting)/2
        
        for chemical in chemicals_entering_names:
            if chemical in metabolites_exiting_names:
                chemical_change_amount = metabolites_exiting[chemical] - chemicals_entering[chemical]
                metabolites_exiting_names[:] = [string for string in metabolites_exiting_names if string != chemical]
            else:
                chemical_change_amount = chemicals_entering[chemical] * -1
            substrate_changes[chemical] = chemical_change_amount

        for metabolite in metabolites_exiting_names:
            metabolite_change_amount = metabolites_exiting[metabolite]
            substrate_changes[metabolite] = metabolite_change_amount


        return substrate_changes
    
    def digestase(self, sequence, index, metabolome, proteomic_base_num, a_conversion_rate):
        param_length = next((item['params_upstream_range'] for item in PFS.map if item['function'] == "Digestase"), None)
        param = sequence[index-param_length:index]
        p1 = param[0:1] # Efficiency of energy conversion
        p2 = param[1:2] # Amount of 'A's able to digest into energy
        p3 = param[2:5] # Max substrate amount
        conversion_efficiency = string_to_normalized_number(p1, proteomic_base_num)
        a_number = string_to_number(p2, proteomic_base_num)
        substrate_max_amount = string_to_number(p3, proteomic_base_num)

        new_metabolome = {}
        total_new_energy = 0

        for metabolite, amount in metabolome.items():
            amount_of_a = metabolite.count('A')
            if amount_of_a == 0:
                if not metabolite in new_metabolome:
                    new_metabolome[metabolite] = amount
                new_metabolome[metabolite] += amount
                continue

            new_metabolite = remove_a(metabolite, a_number)
            new_a_amount = new_metabolite.count('A')
            a_removed = amount_of_a - new_a_amount
            new_metabolite_amount = min(amount, substrate_max_amount)
            energy_produced = new_metabolite_amount * a_removed * a_conversion_rate * conversion_efficiency
            total_new_energy += energy_produced
            
            if len(new_metabolite) != 0:
                if not new_metabolite in new_metabolome:
                    new_metabolome[new_metabolite] = new_metabolite_amount
                new_metabolome[new_metabolite] += new_metabolite_amount
            if not metabolite in new_metabolome:
                new_metabolome[metabolite] = amount - new_metabolite_amount
            new_metabolome[metabolite] += amount - new_metabolite_amount
        
        return new_metabolome, total_new_energy

    def convertase(self, sequence, index, metabolome, proteomic_base_num, chemical_bases, conversion_rates, binding_map, binding_exponent):
        param_length = next((item['params_upstream_range'] for item in PFS.map if item['function'] == "Convertase"), None)
        param = sequence[index-param_length:index]
        p1 = param[0:5] # binding sequence
        p2 = param[5:6] # binding threshold
        p3 = param[6:9] # amount threshold
        p4 = param[9:10] # activator
        p5 = param[10:11] # chemical to convert
        p6 = param[11:12] # the converted chemical
        p7 = param[12:13] # number of chemicals can convert
        p8 = param[13:14] # energy efficiency

        conversion_efficiency = string_to_normalized_number(p8, proteomic_base_num)

        chemical_index_chosen = math.floor(string_to_normalized_number(p5, proteomic_base_num) * len(chemical_bases))
        if chemical_index_chosen >= len(chemical_bases):
            chemical_index_chosen = len(chemical_bases) - 1
        chemical = chemical_bases[chemical_index_chosen]

        converted_chemical_index_chosen = math.floor(string_to_normalized_number(p6, proteomic_base_num) * len(chemical_bases))
        if converted_chemical_index_chosen >= len(chemical_bases):
            converted_chemical_index_chosen = len(chemical_bases) - 1
        converted_chemical = chemical_bases[converted_chemical_index_chosen]

        energy_conversion = 0.1
        found = False

        for string, value in conversion_rates.items():
            parts = string.split('-')
            left = parts[0][0]
            right = parts[1][0]
            if chemical == left and converted_chemical == right:
                energy_conversion = value
                found = True
                break
        

        binding_prob_limit = string_to_normalized_number(p2, proteomic_base_num)
        binding_amount_limit = string_to_number(p3, proteomic_base_num)

        active = False
        activator_factor = string_to_normalized_number(p4, proteomic_base_num) > 0.5

        for metabolite, amount in metabolome.items():
            metabolite_binding_prob = PFS.binding_formula(metabolite, p1, binding_map, binding_exponent)
            binding_chance = metabolite_binding_prob["__total__"]
            if activator_factor:
                if binding_chance > binding_prob_limit and amount > binding_amount_limit:
                    active = True
                    break
            else:
                if binding_chance < binding_prob_limit and amount < binding_amount_limit:
                    active = True
                    break
        
        new_metabolome = {}
        total_new_energy = 0

        if not active or not found:
            return metabolome, 0

        for metabolite, amount in metabolome.items():
            amount_of_chemical = metabolite.count(chemical)
            if amount_of_chemical == 0:
                if not metabolite in new_metabolome:
                    new_metabolome[metabolite] = 0
                new_metabolome[metabolite] += amount
                continue

            new_metabolite = change_chemical(metabolite, string_to_number(p7, proteomic_base_num), chemical, converted_chemical)
            new_chemical_amount = new_metabolite.count(chemical)
            amount_removed = amount_of_chemical - new_chemical_amount
            energy_produced = amount * amount_removed * energy_conversion * conversion_efficiency
            total_new_energy += energy_produced
            
            if not new_metabolite in new_metabolome:
                new_metabolome[new_metabolite] = 0
            new_metabolome[new_metabolite] += amount
        return new_metabolome, total_new_energy