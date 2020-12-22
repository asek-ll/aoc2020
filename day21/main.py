import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

def parse_food(l):
    ingredients, allergens = l.rstrip()[:-1].split(" (contains ")

    i = ingredients.split(" ")
    a = allergens.split(", ")
    return (i, a)

def parse_foods(ll):
    return [parse_food(l) for l in ll]

foods = parse_foods(lines)

def get_ingredient_by_allergen(fs):
    res = {}
    for f in fs:
        for a in f[1]:
            if a not in res:
                res[a] = set(f[0])
            else:
                res[a] = res[a].intersection(set(f[0]))

    return res

def get_non_allergen(fs):
    i = set([])
    for f in fs:
        i = i.union(set(f[0]))

    i_by_a = get_ingredient_by_allergen(foods)
    for a in i_by_a:
        i = i.difference(i_by_a[a])

    return i

def get_count_in_foods(fs, ings):
    c = 0
    for f in fs:
        c += len(set(f[0]).intersection(ings))

    return c

def part_1(fs):
    return get_count_in_foods(fs, get_non_allergen(fs))

def optimize(i_by_a):
    result = []

    optimized = False
    while not optimized:
        optimized = True

        to_remove = None 
        for a in i_by_a:
            ings = i_by_a[a]
            if len(ings) == 1:
                ing = next(iter(ings))
                result.append((a, ing))
                to_remove = ings
                optimized = False
                break
        
        if to_remove is not None:
            ni_by_a = {}
            for a in i_by_a:
                ings = i_by_a[a].difference(to_remove)
                if len(ings) > 0:
                    ni_by_a[a] = ings

            i_by_a = ni_by_a

    return result



def part_2(fs):
    i_by_a = get_ingredient_by_allergen(foods)
    i_by_a = optimize(i_by_a)
    return ",".join([x[1] for x in sorted(i_by_a, key=lambda x: x[0])])

print("Part 1: %d" % part_1(foods))
print("Part 2: %s" % part_2(foods))
