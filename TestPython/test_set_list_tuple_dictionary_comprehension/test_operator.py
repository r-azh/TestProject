from operator import itemgetter

li = [1, 3, 5, 7]

f = itemgetter(2)       # f(l) returns li[2]
print(f(li))

ff = itemgetter(0, 3)      # f(l) returns (li[0], li[3])
print(ff(li))