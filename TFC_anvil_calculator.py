"""TFC anvil calculator

This module calculates combinations of modifier values to reach a target total,
likely inspired by TFC (Terrafirmacraft) anvil mechanics. It identifies how 
modifiers (e.g., hammer hits or rules) can sum to a specific value.

Functions:
- detect_multiplier
- generate_multiplier_first_moves
- multiplier_calibration
- expand_modifiers
- main
"""

def detect_multiplier(target: int, modifiers: list[int]) -> tuple[int, int]:
    """
    Estimates how many times the strongest available modifier (positive or negative)
    needs to be applied to approach the target value.

    Parameters:
    target (int): The target value to reach.
    modifiers (list[int]): List of possible modifier values.

    Returns:
    tuple[int, int]: A tuple containing:
        - r (int): Estimated number of repetitions of the strongest modifier.
        - p (int): The strongest modifier used for the estimation.
    """
    if target > 0:
        base_modifier = max(modifiers)
        temp = target - sum([_ for _ in modifiers if _ > 0])

    else:
        base_modifier = min(modifiers)
        temp = target + sum([_ for _ in modifiers if _ < 0])
    
    base_modifier_multiplier = (temp//base_modifier)

    return base_modifier_multiplier, base_modifier 

def generate_multiplier_first_moves(base_modifier_multiplier: int, base_modifier: int, modifiers: list[int]) -> set:
    """
    Generates initial move combinations based on the estimated multiplier.

    Parameters:
    r (int): Repetition count for strongest/weakest modifier.
    p (int): The modifier value to be repeated.
    modifiers (list[int]): List of available modifiers.

    Returns:
    set[tuple[int]]: A set of initial move combinations (as tuples).
    """
    if base_modifier_multiplier <= 1:
        combinations = {tuple([i]) for i in modifiers}
    else:
        combinations = {tuple([base_modifier]*base_modifier_multiplier)}
        
    return combinations

def multiplier_calibration(target: int, modifiers: list[int]) -> set[tuple[int]]:
    """
    Calibrates the starting combinations based on target value and modifiers.

    Parameters:
    target (int): The target value.
    modifiers (list[int]): List of available modifiers.

    Returns:
    set[tuple[int]]: Initial set of combinations.
    """
    base_modifier_multiplier, base_modifier = detect_multiplier(target, modifiers)
    combinations = generate_multiplier_first_moves(base_modifier_multiplier, base_modifier, modifiers) 
    return combinations
    
def expand_modifiers(a, modifiers) -> set[tuple[int]]:
    """
    Expands each existing combination by adding every possible modifier.

    Parameters:
    a (set[tuple[int]]): Current set of combinations.
    modifiers (list[int]): List of possible modifiers to add.

    Returns:
    set[tuple[int]]: New set of expanded combinations.
    """
    return {tuple(sorted([*x, y])) for x in a for y in modifiers}

def main(target, *must_include) -> list[int]|ValueError:
    """
    Main function to find a combination of modifiers that sums to the target value.

    Parameters:
    k (int): Target value to reach (e.g., forging rule value).
    *must_include (int): One or more values that must be part of the final combination.

    Returns:
    list[int]: The final answer.
    """
    modifiers = [-5, -6, -9, -15, 2, 7, 13, 16]
    for include in must_include:
        if include not in modifiers:
            raise ValueError("One or more of the (must include) value(s) is not included in the available modifiers.")
    target -= sum(must_include)

    combinations = multiplier_calibration(target, modifiers)

    count = 0
    while True:
        for i in combinations:
            count += 1
            if sum(i) == target:
                answer = [x for _ in [tuple(must_include), i] for x in _]
                print(f'Times iterated thourgh each potential candiate: {count}')
                print(f'Answer Check: {(target+sum(must_include)) == sum(answer)}')
                print(f"Calculated {len(combinations)} different combinations. The answer has {len(i)} numbers. answer is {answer}. ")
                return answer
        combinations = expand_modifiers(combinations, modifiers)

if __name__ == "__main__":
    print(main(70, -5, -9, 2))