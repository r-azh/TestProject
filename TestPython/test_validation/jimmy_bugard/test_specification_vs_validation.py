__author__ = 'R.Azh'


class Order:
    id = None
    customer = None
    total = None

    def __init__(self, id, customer, total):
        self.id = id
        self.customer = customer
        self.total = total


class ISpecification:
    t = None

    def is_satisfied_by(self, t):
        raise NotImplementedError


class OrderTotalSpec(ISpecification):
    min_total = None

    def __init__(self, min_total):
        self.min_total = min_total

    def is_satisfied_by(self, order):
        return order.total >= self.min_total


class NameStartsWithSpec(ISpecification):
    start_char = None

    def __init__(self, start_char):
        self.start_char = start_char

    def is_satisfied_by(self, order):
        return order.customer.startswith(self.start_char)


# specification + Composite pattern
class AndSpec(ISpecification):
    _augends = None

    def __init__(self, augend1, augend2):
        self._augends = []
        self._augends.append(augend1)
        self._augends.append(augend2)

    def add(self, augend):
        self._augends.append(augend)

    def is_satisfied_by(self, t):
        is_satisfied = True
        for augend in self._augends:
            is_satisfied = is_satisfied and augend.is_satisfied_by(t)
        return is_satisfied


class OrSpec(ISpecification):
    _augends = None

    def __init__(self, augend1, augend2):
        self._augends = []
        self._augends.append(augend1)
        self._augends.append(augend2)

    def add(self, augend):
        self._augends.append(augend)

    def is_satisfied_by(self, t):
        is_satisfied = True
        for augend in self._augends:
            is_satisfied = is_satisfied or augend.is_satisfied_by(t)
        return is_satisfied


order = Order(1, 'Joe smith', 150)
spec = AndSpec(OrderTotalSpec(100), NameStartsWithSpec("Joe"))

print(spec.is_satisfied_by(order))


# Specification
# - Matches a single aspect on a single entity
# - Performs positive matching (i.e., return true if it matches)
# - Executed against a repository or a collection
# - Can be composed into an arbitrarily complex search context, where a multitude of specifications compose one search
#  context
# - “I’m looking for something”

# Validator
# - Matches as many aspects as needed on a single entity
# - Performs negative matching (i.e., returns false if it matches)
# - Executed against a single entity
# - Is intentionally not composable, a single validator object represents a single validation context
# - “I’m validating this”
#
# So although validation and specifications are doing similar boolean operations internally, they have very
# different contexts on which they are applied.  Keeping these separate ensures that your validation concerns don’t bleed over into your searching concerns.