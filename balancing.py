import numpy as np
from sympy import Matrix, lcm, nsimplify

# Parsing chemical compounds into its elements and counts
def parse_compound(compound):
    import re
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', compound)
    return {el: int(count) if count else 1 for el, count in elements}

# Parsing chemical equations into left and right sides with compounds
def parse_equation(reactants, products):
    return reactants, products

# Building a matrix for the system of linear equations
def build_matrix(reactants, products):
    left_compounds, right_compounds = parse_equation(reactants, products)
    compounds = left_compounds + right_compounds
    elements = set()
    for compound in compounds:
        elements.update(parse_compound(compound).keys())

    element_list = sorted(elements)
    num_elements = len(element_list)
    num_compounds = len(compounds)
    
    matrix = np.zeros((num_elements, num_compounds))
    
    for j, compound in enumerate(compounds):
        counts = parse_compound(compound)
        for i, element in enumerate(element_list):
            matrix[i, j] = counts.get(element, 0) * (-1 if j >= len(left_compounds) else 1)
    
    return matrix, len(left_compounds), len(right_compounds)

# Performing Gaussian elimination and return the coefficients
def gaussian_elimination(matrix):
    aug_matrix = Matrix(matrix).rref()[0]
    coefficients = [float(aug_matrix[i, -1]) for i in range(aug_matrix.rows)]

    if len(coefficients) < matrix.shape[1]:
        coefficients = list(coefficients) + [-1] * (matrix.shape[1] - len(coefficients))
    
    coefficients = [nsimplify(coef) for coef in coefficients]
    denom_lcm = lcm([coef.as_numer_denom()[1] for coef in coefficients])
    coefficients = [int(coef * denom_lcm) for coef in coefficients]
    
    return coefficients

# Balancing the chemical equation
def balance_equation(reactants, products):
    matrix, num_left, num_right = build_matrix(reactants, products)
    coefficients = gaussian_elimination(matrix)

    if any(coef < 0 for coef in coefficients):
        coefficients = [-coef for coef in coefficients]

    left_balanced = ' + '.join(f"{coef if coef != 1 else ''}{compound}" 
                               for coef, compound in zip(coefficients[:num_left], reactants))
    right_balanced = ' + '.join(f"{coef if coef != 1 else ''}{compound}" 
                                for coef, compound in zip(coefficients[num_left:], products))

    return f"{left_balanced.strip()} -> {right_balanced.strip()}"

# The new input format using lists for reactants and products
def send_equation(reactants, products):
    balanced_equation = balance_equation(reactants, products)
    print(f"Balanced: {balanced_equation}")

# Example
#reactants = ["H2", "O2"]
#products = ["H2O"]

# Call the send_equation function
#send_equation(reactants, products)
