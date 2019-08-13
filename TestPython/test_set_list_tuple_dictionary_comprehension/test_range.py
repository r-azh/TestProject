__author__ = 'R.Azh'

# You can form a range with one, two, or three arguments. The expression range(a,b)
# represents the sequence of integers a, a + 1, a + 2,...,b % 1. The expression range(a,b,c)
# represents a, a + c, a + 2c, . . . (stopping just before b).

print(range(10))
print(list(range(10)))
print(list(range(2, 8)))
print(list(range(0, 20, 3)))

print(sum({i*i for i in range(10)}))


vps_dict = {'Extreme': [{'rtt': (0, 0.25), 'plr': (250, 1000)},
                        {'rtt': (0.25, 100), 'plr': (100, 1000)}],

            'Bad': [{'rtt': (0, 0.25), 'plr': (100, 250)},
                    {'rtt': (0.25, 2.5), 'plr': (50, 100)}],

            'Good': [{'rtt': (0, 0.25), 'plr': (0, 100)},
                     {'rtt': (0.25, 100), 'plr': (0, 50)}]
                        # ((1, 2.5), (0, 50)),
                        # ((2.5, 100), (0, 50))

            }

x = {'rtt': 0.1, 'plr': 50}
print(vps_dict)
for key, value in vps_dict.items():
    for ranges in value:
        if x['rtt'] in range(*ranges['rtt']) and x['plr'] in range(*ranges['plr']):
            print(key)