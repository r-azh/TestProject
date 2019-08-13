__author__ = 'R.Azh'

# Convert the interface of a class into another interface clients expect.
#  Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.


# Target: defines the domain-specific interface that Client uses.
class Compound:
    _chemical = None
    _boiling_point = None
    _melting_point = None
    _molecular_weight = None
    _molecular_formula = None

    def __init__(self, chemical):
        self._chemical = chemical

    def display(self):
        print("\nCompound: {} ------ ".format(self._chemical))


# Adaptee: defines an existing interface that needs adapting
class ChemicalDataBank(object):
    def get_critical_point(self, compound, point):
        melting_point_switcher = {"water": 0.0,
                                  "benzene": 5.5,
                                  "ethanol": -114.1}

        boiling_point_switcher = {"water": 100.0,
                                  "benzene": 80.1,
                                  "ethanol": 78.3}

        if point == "M":
            if compound.lower() in melting_point_switcher:
                return melting_point_switcher[compound.lower()]
            else:
                return 0
        else:
            if compound.lower() in boiling_point_switcher:
                return boiling_point_switcher[compound.lower()]
            else:
                return 0

    def get_molecular_structure(self, compound):
        molecular_structure_switcher = {"water": "H20",
                                        "benzene": "C6H6",
                                        "ethanol": "C2H50H"}
        if compound.lower() in molecular_structure_switcher:
            return molecular_structure_switcher[compound.lower()]
        else:
            return ""

    def get_molecular_weight(self, compound):
        molecular_weight_switcher = {"water": 18.015,
                                     "benzene": 78.1134,
                                     "ethanol": 46.0688}
        if compound.lower() in molecular_weight_switcher:
            return molecular_weight_switcher[compound.lower()]
        else:
            return 0


# Adapter: adapts the interface Adaptee to the Target interface
class RichCompound(Compound):
    _bank = None

    def __init__(self, name):
        super().__init__(name)

    def display(self):
        self._bank = ChemicalDataBank()
        self._boiling_point = self._bank.get_critical_point(self._chemical, "B")
        self._melting_point = self._bank.get_critical_point(self._chemical, "M")
        self._molecular_formula = self._bank.get_molecular_structure(self._chemical)
        self._molecular_weight = self._bank.get_molecular_weight(self._chemical)

        super().display()
        print('Formula: {}'.format(self._molecular_formula))
        print('weight: {}'.format(self._molecular_weight))
        print('Melting pt: {}'.format(self._melting_point))
        print('Boinling pt: {}'.format(self._boiling_point))


# client: collaborates with objects conforming to the Target interface

unknown_compound = RichCompound("unknown")
unknown_compound.display()

water_compound = RichCompound("water")
water_compound.display()

benzene_compound = RichCompound("benzene")
benzene_compound.display()

ethanol_compound = RichCompound("ethanol")
ethanol_compound.display()
