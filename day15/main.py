import sys

if len(sys.argv) <= 1:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

nums = list(map(int, lines[0].rstrip().split(',')))

def what_number(nums, target):
    memo = {}
    last = None
    for i in range(0, len(nums)):
        if last is not None:
            memo[last] = i
        last = nums[i]

    # print(memo, last)
    
    for i in range(len(nums), target):
        if last not in memo:
            n = 0
        else:
            n = i - memo[last]

        memo[last] = i
        last = n

    return last




print("Part 1: %d" % (what_number(nums, 2020)))
print("Part 2: %d" % (what_number(nums, 30000000)))
