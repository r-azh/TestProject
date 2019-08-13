__author__ = 'R.Azh'
# from vtc design patterns (java)


class AceInterface:
    _name = None

    @property
    def name(self):
        raise NotImplementedError

    @name.setter
    def name(self, value):
        raise NotImplementedError


class AceClass(AceInterface):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class AcmeInterface:
    _first_name = None
    _last_name = None

    @property
    def first_name(self):
        raise NotImplementedError

    @first_name.setter
    def first_name(self, value):
        raise NotImplementedError

    @property
    def last_name(self):
        raise NotImplementedError

    @last_name.setter
    def last_name(self, value):
        raise NotImplementedError


class AcmeClass(AcmeInterface):
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value


class AceToAcmeAdapter(AcmeInterface):
    ace_object = None

    def __init__(self, ace_object):
        self.ace_object = ace_object
        self._first_name = ace_object.name.split()[0]
        self._last_name = ace_object.name.split()[1]

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

# TestAdapter
ace_object = AceClass()
ace_object.name = "Cary Grant"

adapter = AceToAcmeAdapter(ace_object)
print("Customer's first name: ", adapter.first_name)
print("Customer's last name: ", adapter.last_name)
