grammar = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']],
}

def remove_direct_left_recursion(nt, productions):
    recursive = [p for p in productions if p[0] == nt]
    non_recursive = [p for p in productions if p[0] != nt]

    if not recursive:
        return {nt: productions}, None

    nt_prime = nt + "'"
    new_productions = [p + [nt_prime] for p in non_recursive]
    prime_productions = [p[1:] + [nt_prime] for p in recursive] + [['ε']]

    return {nt: new_productions}, {nt_prime: prime_productions}


def remove_left_recursion(grammar):
    nts = list(grammar.keys())
    result = {nt: grammar[nt] for nt in nts}

    for i, Ai in enumerate(nts):
        # Substitute earlier non-terminals into Ai's productions
        for j in range(i):
            Aj = nts[j]
            new_prods = []
            for prod in result[Ai]:
                if prod[0] == Aj:
                    for aj_prod in result[Aj]:
                        new_prods.append(aj_prod + prod[1:])
                else:
                    new_prods.append(prod)
            result[Ai] = new_prods

        updated, prime = remove_direct_left_recursion(Ai, result[Ai])
        result.update(updated)
        if prime:
            result.update(prime)
            nts.append(list(prime.keys())[0])

    return result


def print_grammar(grammar):
    for nt, prods in grammar.items():
        rhs = ' | '.join(' '.join(p) for p in prods)
        print(f"  {nt} -> {rhs}")


print("Original Grammar:")
print_grammar(grammar)

result = remove_left_recursion(grammar)

print("\nAfter Removing Left Recursion:")
print_grammar(result)