__author__ = 'R.Azh'


# (, ), {, }, [,]


input = '4  ' \
        '{[()]}' \
        ' {[(])} ' \
        '{{[[(())]]}}' \
        '{([]([]){})}'


def is_matched(expression):
    char_pair_dict = {')': '(', '}': '{', ']': '['}
    str = list(expression)
    print(str)
    stack = []
    for char in str:
        print(char)
        if char in char_pair_dict.values():
            stack.append(char)
        elif stack and char_pair_dict[char] != stack.pop(len(stack)-1):
            return False
    return True

# t = int(input().strip())
input_l = input.split()
t = int(input_l[0])
for a0 in range(t):
    # expression = input().strip()
    print(input_l[a0+1])
    expression = input_l[a0+1].strip()
    if is_matched(expression) == True:
        print("YES")
    else:
        print("NO")


