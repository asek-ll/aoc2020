import sys

if len(sys.argv) <= 2:
    raise Exception("No inputs")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

preamble = int(sys.argv[2])
nums = [int(l.rstrip()) for l in lines]


def is_sum_of_two(num, window):
    for n in window:
        if (num - n) in window:
            return True

    return False

def find_invalid(nums, preamble):

    for i in range(preamble, len(nums)):
        window = set([])
        for j in range(0, preamble):
            window.add(nums[i-preamble+j])

        num = nums[i]
        if not is_sum_of_two(num, window):
            return num

    return -1



def find_range_for_num(nums, target):
    sums = {0: -1}
    s = 0
    for i in range(0, len(nums)):
        n = nums[i]
        s += n
        to_s = s - target
        if to_s in sums:
            return (sums[to_s]+1,i)

        sums[s] = i

    return -1





invalid = find_invalid(nums, preamble)
print("Part 1: %d" % invalid)
r = find_range_for_num(nums, invalid)
part = nums[r[0]:r[1]+1]
weakness = min(part) + max(part)
print("Part 2: %d" % weakness)
