from collections import defaultdict
import sys
from hashlib import sha256


def same_bytes(left, right):
    left_bytes = open(left, "rb").read()
    right_bytes = open(right, "rb").read()
    return left_bytes == right_bytes


def brute_force_find_duplicates(filenames):
    """brute force O(N^2) solution"""
    matches = []
    for i_left, left in enumerate(filenames):
        for i_right in range(i_left):
            right = filenames[i_right]
            if same_bytes(left, right):
                matches.append((left, right))
    return matches


def find_groups(filenames):
    groups = defaultdict(set)
    for fn in filenames:
        with open(fn, "rb") as f:
            data = f.read()
        hash_code = sha256(data).hexdigest()
        groups[hash_code].add(fn)
    return groups


if __name__ == "__main__":
    groups = find_groups(sys.argv[1:])
    for filenames in groups.values():
        print(", ".join(sorted(filenames)))
        print(brute_force_find_duplicates(list(filenames)))

