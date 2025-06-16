import math

def find_binding_chance(concentration_, binding_affinity, num_of_binders=1, k=1, x0=10):

    # Base activation probability based on concentration
    base_probability = 1 / (1 + math.exp(-k * (concentration_ - x0)))

    # Adjust the probability based on the binding affinity and number of binders
    adjusted_probability = 1 - (1 - (base_probability * binding_affinity)) ** num_of_binders

    # Ensure the probability does not exceed 1
    return min(adjusted_probability, 1)

def string_to_normalized_number(s, base_num):
    decimal_value = 0
    for i, char in enumerate(reversed(s)):
        # Convert char to its numerical equivalent (e.g., 'a' -> 0, 'b' -> 1, ...)
        num = ord(char) - ord('a')
        decimal_value += num * (base_num ** i)
    
    # Calculate the maximum possible value for a string of this length in the given base
    max_value = (base_num ** len(s)) - 1
    
    # Normalize the decimal value to a float between 0 and 1
    normalized_value = decimal_value / max_value
    
    return normalized_value

def string_to_number(s, base_num):
    decimal_value = 0
    for i, char in enumerate(reversed(s)):
        # Convert char to its numerical equivalent (e.g., 'a' -> 0, 'b' -> 1, ...)
        num = ord(char) - ord('a')
        decimal_value += num * (base_num ** i)
    
    return decimal_value

def remove_a(s, num_a_to_remove):
    result = []  # Using a list for efficient string concatenation
    removed_count = 0  # Keep track of how many 'A's have been removed

    for char in s:
        if char == 'A' and removed_count < num_a_to_remove:
            # Skip this character and increment the count
            removed_count += 1
        else:
            # Append non-'A' characters and 'A's once we've removed enough
            result.append(char)

    return ''.join(result)  # Convert the list of characters back to a string

def change_chemical(string, num_to_remove, chemical, converted_chemical):
    result = []
    removed_count = 0

    for char in string:
        if char == chemical and removed_count < num_to_remove:
            # Convert this character and increment the count
            result.append(converted_chemical)
            removed_count += 1
        else:
            # Append non-'A' characters and 'A's once we've removed enough
            result.append(char)

    return ''.join(result)


def reverse_transcript_proteins(proteins, codon_map, stop_codon, start_codon, strict_search = False, join_genes = False):
    if (join_genes):
        strict_search = True
    genes = []
    for protein in proteins:
        gene = ""
        for protein_base_index, protein_base in enumerate(protein):
            if protein_base == "_":
                matching_genomic_bases = [key for key, value in codon_map.items()]
            else:
                matching_genomic_bases = [key for key, value in codon_map.items() if value == protein_base]
            for codon_index, codon in enumerate(matching_genomic_bases):
                if codon_index == len(matching_genomic_bases) - 1:
                    gene += codon
                    break 
                base_condition = gene.join(codon).find(stop_codon) == -1 and gene.join(codon).find(start_codon) == -1
                if strict_search and len(genes) != 0 and (protein_base_index == 0 or protein_base_index == len(protein) -1):
                    if protein_base_index ==  0:
                        if base_condition and genes[-1].join(codon).find(stop_codon) != -1 and genes[-1].join(codon).find(start_codon) != -1:
                            gene += codon
                            break
                    if protein_base_index == len(protein) - 1:
                        if base_condition and genes[-1].join(codon).find(stop_codon) != -1 and genes[-1].join(codon).find(start_codon) != -1 and codon[:-1].join(stop_codon[1:]) != stop_codon:
                            gene += codon
                            break
                else:
                    if base_condition:
                        gene += codon
                        break
        genes.append(gene)
    

    if (join_genes):
        new_genes = ""
        for gene in genes:
            new_genes += (start_codon + gene + stop_codon)
        return new_genes
    
    return genes

