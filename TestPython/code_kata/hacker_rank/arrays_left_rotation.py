__author__ = 'R.Azh'

# When we perform  left rotations, the array undergoes the following sequence of changes:
# Thus, we print the array's final state as a single line of space-separated values, which is 5 1 2 3 4.


def array_left_rotation(a, n, k):
    return [a[(i+k) % n] for i in range(0, n)]

# n = int(input().strip())
# k = int(input().strip())
# # n, k = map(int, input().strip().split(' '))
#
# a = []
# for i in (1, n):
#     a.append(int(input().strip()))
# # a = map(int, input().strip().split(' '))
#
# answer = array_left_rotation(a, n, k)
answer = array_left_rotation([1, 2, 3, 4, 5], 5, 1)
print(['{} '.format(i) for i in answer])
print(*answer, sep=' ')








