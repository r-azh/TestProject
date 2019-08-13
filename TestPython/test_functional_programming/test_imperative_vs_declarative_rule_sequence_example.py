__author__ = 'R.Azh'


def zero(s):
    if s[0] == "0":
        return s[1:]


def one(s):
    if s[0] == "1":
        return s[1:]


print('\n############### imperative #######################')


def rule_sequence(s, rules):
    for rule in rules:
        s = rule(s)
        if s == None:
            break

    return s

print(rule_sequence('0101', [zero, one, zero]))
print(rule_sequence('0101', [zero, zero]))


print('\n############### declarative #######################')
# more declarative by rewriting it as a recursion.


def rule_sequence_(s, rules):
    if s is None or not rules:
        return s
    else:
        return rule_sequence_(rules[0](s), rules[1:])

print(rule_sequence_('0101', [zero, one, zero]))
print(rule_sequence_('0101', [zero, zero]))
