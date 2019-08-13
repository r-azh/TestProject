import sys

num = 64901940227604506886490484088242176130

byte = bytes(str(num).encode())
print(byte)
print(len(byte))

print(byte[:8])

binary = bin(num)
print(binary)

print('\n##### concat two eight byte digits: ####\n')
num1 = 6490194022760450688
num2 = 6490484088242176130
print(num1, bin(num1))
print(num2, bin(num2))

# shift left part to the left by 8** bits
result = num1 << (8 * 8)
print(bin(result))

# "or" it with above number
result = result | num2

print(bin(result))
print(result)

print('\n#####  split one 16 byte digit to two eight byte digits ####\n')

num = result
# first 8 bytes just shift it to the right by 8*8 bits
left_eight_bytes = num >> (8 * 8)
print(bin(left_eight_bytes))
print('left_eight_bytes:', left_eight_bytes)
assert left_eight_bytes == num1

# To get the last 8 bits, mask it with 0b11111111, i.e. 255.
# To get the last 8 bytes, mask it with 0b1111111111111111111111111111111111111111111111111111111111111111, i.e. 255.
mask = ''.join(['1' for i in range(8*8)])
assert len(mask) == 8*8
mask_int = int(mask, 2)
print(mask_int)
right_eight_bytes = num & mask_int
print(bin(right_eight_bytes))
assert right_eight_bytes == num2
print('right_eight_bytes:', right_eight_bytes)


print(sys.getsizeof(result))


INBOX_REPORT_MEMBERSHIP_ID_LENGTH = 64
INBOX_REPORT_MEMBERSHIP_ID_MASK = 2 ** INBOX_REPORT_MEMBERSHIP_ID_LENGTH - 1


def make_inbox_report_membership_id(membership_id, inbox_id):
    masked_result = int(membership_id) << INBOX_REPORT_MEMBERSHIP_ID_LENGTH
    return masked_result | int(inbox_id)


def get_inbox_id_and_membership_id_from_inbox_report_membership_id(inbox_report_membership_id):
    inbox_report_membership_id = int(inbox_report_membership_id)
    membership_id = inbox_report_membership_id >> INBOX_REPORT_MEMBERSHIP_ID_LENGTH

    inbox_id = inbox_report_membership_id & INBOX_REPORT_MEMBERSHIP_ID_MASK
    return membership_id, inbox_id
