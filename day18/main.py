import sys
import re

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

def evaluate(exp):
    if not ' ' in exp:
        return int(exp)

    other, op, f = exp.rsplit(' ', 2)
    arg = int(f)

    if op == '*':
        res = arg * evaluate(other)
    else:
        res = arg + evaluate(other)

    return res

def replace_fun(m):
    return str(evaluate(m[1]))

p = re.compile('\(([^\(\)]+)\)')
def solve(l):
    has_par = True
    while has_par:
        has_par = False
        l2 = p.sub(replace_fun, l)

        if l2 != l:
            has_par = True
        
        l = l2

    return evaluate(l)

def evaluate2(exp):
    parts = [evaluate(m) for m in exp.split(' * ')]

    res = 1
    for m in parts:
        res *= m
    
    return res

def replace_fun2(m):
    return str(evaluate2(m[1]))

p = re.compile('\(([^\(\)]+)\)')
def solve2(l):
    has_par = True
    while has_par:
        has_par = False
        l2 = p.sub(replace_fun2, l)

        if l2 != l:
            has_par = True
        
        l = l2

    return evaluate2(l)

print("Part 1: %d" % sum([solve(l.rstrip()) for l in lines]))
print("Part 2: %d" % sum([solve2(l.rstrip()) for l in lines]))