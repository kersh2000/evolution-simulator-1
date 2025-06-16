import math

def find_binding_chance(concentration_, binding_affinity, num_of_binders=1, k=1, x0=100):

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

# Test the function
print(string_to_normalized_number("ab", 2))  # Expected output: 0.333...


if __name__ == "__main__":
    # binding_affinity_to_BB = 0.8  # Let's assume 'bd' has a high affinity to 'BB'
    # concentration_BB = 100  # Example concentration of 'BB'
    # num_of_binders = 10

    # # Calculate the activation probability, including the sequence's binding affinity to 'BB'
    # activation_probability = find_binding_chance(concentration_BB, binding_affinity_to_BB, num_of_binders=num_of_binders)
    # print(f"Activation Probability: {activation_probability}")
    proteomic_base_num = 10
    print(string_to_normalized_number("gf", 10))