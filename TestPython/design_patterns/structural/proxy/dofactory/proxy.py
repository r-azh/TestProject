import abc

__author__ = 'R.Azh'

# Provide a surrogate or placeholder for another object to control access to it.


# Subject: defines the common interface for RealSubject and Proxy so that a Proxy can be used anywhere a RealSubject
# is expected.
class IMath:
    @abc.abstractmethod
    def add(self, x, y):
        ''' add '''

    @abc.abstractmethod
    def sub(self, x, y):
        ''' sub '''

    @abc.abstractmethod
    def mul(self, x, y):
        ''' mul '''

    @abc.abstractmethod
    def div(self, x, y):
        ''' div '''


# RealSubject: defines the real object that the proxy represents.
class Math(IMath):
    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y

    def div(self, x, y):
        return x / y


# Proxy: maintains a reference that lets the proxy access the real subject. Proxy may refer to a Subject if the
#  RealSubject and Subject interfaces are the same.
# provides an interface identical to Subject's so that a proxy can be substituted for for the real subject.
# controls access to the real subject and may be responsible for creating and deleting it.
# other responsibilites depend on the kind of proxy:
# - remote proxies are responsible for encoding a request and its arguments and for sending the encoded request to
#   the real subject in a different address space.
# - virtual proxies may cache additional information about the real subject so that they can postpone accessing it. For
#    example, the ImageProxy from the Motivation caches the real images's extent.
# - protection proxies check that the caller has the access permissions required to perform a request.
class MathProxy(IMath):
    _math = None

    def __init__(self):
        self._math = Math()

    def add(self, x, y):
        return self._math.add(x, y)

    def sub(self, x, y):
        return self._math.sub(x, y)

    def mul(self, x, y):
        return self._math.mul(x, y)

    def div(self, x, y):
        return self._math.div(x, y)


# usage
proxy = MathProxy()
print(" 4 + 2 = {}".format(proxy.add(4, 2)))
print(" 4 - 2 = {}".format(proxy.sub(4, 2)))
print(" 4 * 2 = {}".format(proxy.mul(4, 2)))
print(" 4 / 2 = {}".format(proxy.div(4, 2)))

