__author__ = 'R.Azh'

# separate object construction from its representation:
#   Separate the construction of a complex object from its representation so that the
#   same construction process can create different representations.


# Director: constructs an object using the Builder interface
class Shop:
    def construct(self, vehicle_builder):
        vehicle_builder.build_frame()
        vehicle_builder.build_engine()
        vehicle_builder.build_wheels()
        vehicle_builder.build_doors()


# Builder: specifies an abstract interface for creating parts of a Product object
class VehicleBuilder:
    vehicle = None

    def build_frame(self):
        pass

    def build_engine(self):
        pass

    def build_wheels(self):
        pass

    def build_doors(self):
        pass


# ConcreteBuilder: constructs and assembles parts of the product by implementing the Builder interface
# defines and keeps track of the representation it creates
# provides an interface for retrieving the product
class MotorCycleBuilder(VehicleBuilder):
    def __init__(self):
        self.vehicle = Vehicle("MotorCycle")

    def build_frame(self):
        self.vehicle["frame"] = "MotorCycle Frame"

    def build_engine(self):
        self.vehicle["engine"] = "500 cc"

    def build_wheels(self):
        self.vehicle["wheels"] = "2"

    def build_doors(self):
        self.vehicle["doors"] = "0"


# ConcreteBuilder
class CarBuilder(VehicleBuilder):
    def __init__(self):
        self.vehicle = Vehicle("Car")

    def build_frame(self):
        self.vehicle["frame"] = "Car Frame"

    def build_engine(self):
        self.vehicle["engine"] = "2500 cc"

    def build_wheels(self):
        self.vehicle["wheels"] = "4"

    def build_doors(self):
        self.vehicle["doors"] = "4"


# ConcreteBuilder
class ScooterBuilder(VehicleBuilder):
    def __init__(self):
        self.vehicle = Vehicle("Scooter")

    def build_frame(self):
        self.vehicle["frame"] = "Scooter Frame"

    def build_engine(self):
        self.vehicle["engine"] = "50 cc"

    def build_wheels(self):
        self.vehicle["wheels"] = "2"

    def build_doors(self):
        self.vehicle["doors"] = "0"


# Product: represents the complex object under construction. ConcreteBuilder builds the product's internal
# representation and defines the process by which it's assembled
# includes classes that define the constituent parts, including interfaces for assembling the parts into the
#  final result
class Vehicle:
    vehicle_type = None
    parts = None

    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        self.parts = {}

    def __setitem__(self, key, value):
        self.parts[key] = value

    def __getitem__(self, item):
        return self.parts[item]

    def show(self):
        print("\n---------------------------")
        print("Vehicle Type: {0}".format(self.vehicle_type))
        print(" Frame : {0}".format(self["frame"]))
        print(" Engine : {0}".format(self["engine"]))
        print(" #Wheels: {0}".format(self["wheels"]))
        print(" #Doors : {0}".format(self["doors"]))


######### usage ###########

# builder = VehicleBuilder()
shop = Shop()

builder = ScooterBuilder()
shop.construct(builder)
builder.vehicle.show()

builder = CarBuilder()
shop.construct(builder)
builder.vehicle.show()

builder = MotorCycleBuilder()
shop.construct(builder)
builder.vehicle.show()