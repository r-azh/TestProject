__author__ = 'R.Azh'


def number_needed(a, b):
    x = set(a+b)
    del_count = sum([0 if a.count(c) == b.count(c) else abs(a.count(c)-b.count(c)) for c in x])
    # del_count = del_count + sum([1 for c in a if c not in b])
    # del_count = del_count + sum([1 for c in b if c not in a])
    return del_count


# a = input().strip()
# b = input().strip()
a = 'cde'
b = 'abc'

a = 'bacdc'
b = 'dcbad'

print(number_needed(a, b))



# intersection = [c for c in a if c in b]
# import difflib
# print(difflib.SequenceMatcher(None, a, b).get_matching_blocks())
