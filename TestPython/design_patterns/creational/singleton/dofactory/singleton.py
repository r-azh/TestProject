__author__ = 'R.Azh'

# Ensure a class has only one instance and provide a global point of access to it.


class LoadBalancer:
    _servers = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            # print('new')
            cls._inst = super(LoadBalancer, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def __init__(self):
        # print('init')
        self._servers = []
        self._servers.append("ServerI")
        self._servers.append("ServerII")
        self._servers.append("ServerIII")
        self._servers.append("ServerIV")
        self._servers.append("ServerV")

    def server(self):
        import random
        s = random.sample(self._servers, 1)
        return s


b1 = LoadBalancer()
b2 = LoadBalancer()
b3 = LoadBalancer()
b4 = LoadBalancer()

# if b1 == b2 and b2 == b3 and b3 == b4: # always gives true
if b1 is b2 and b2 is b3 and b3 is b4:
    print('same instance')

balancer = LoadBalancer()
for i in range(10):
    print('Dispatch Request to: {}'.format(balancer.server()))

