__author__ = 'R.Azh'


# class Customer:
#     def __init__(self, first_name, last_name):
#         self._first_name = first_name
#         self._last_name = last_name
#
#     @property
#     def first_name(self):
#         return self._first_name
#
#     @first_name.setter
#     def first_name(self, first_name):
#         self.first_name = first_name
#
#     @property
#     def last_name(self):
#         return self._last_name
#
#     @last_name.setter
#     def last_name(self, last_name):
#         self._last_name = last_name


class ChangeNameCommand:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self.first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name


class Customer:
    _first_name = None
    _last_name = None

    def change_name(self, change_name_command):
        self._first_name = change_name_command.first_name
        self._last_name = change_name_command.last_name

# The issue with an entity validating itself is twofold:
#   - You’re mutating state before validation, so your entity is allowed to be in an invalid state.
#   - There is no context of what the user was trying to do


# Instead of relying on an entity/aggregate to perform command validation, I entrust it solely with invariants.
# Invariants are all about making sure I can transition from one state to the next wholly and completely, not partially.
#  It’s not actually about validating a request, but performing a state transition.
# With this in mind, my validation centers around commands and actions, not entities.
# I could do something like this instead:

# public class ChangeNameCommand {
#   [Required]
#   public string FirstName { get; set; }
#   [Required]
#   public string LastName { get; set; }
# }
#
# public class Customer
# {
#   public string FirstName { get; private set; }
#   public string LastName { get; private set; }
#
#   public void ChangeName(ChangeNameCommand command) {
#     FirstName = command.FirstName;
#     LastName = command.LastName;
#   }
# }

#  or using FluentValidation library

# using FluentValidation;
# public class ChangeNameCommand {
#   public string FirstName { get; set; }
#   public string LastName { get; set; }
# }
#
# public class ChangeNameValidator : AbstractValidator<ChangeNameCommand> {
#   public ChangeNameValidator() {
#     RuleFor(m => m.FirstName).NotNull().Length(3, 50);
#     RuleFor(m => m.LastName).NotNull().Length(3, 50);
#   }
# }
#
# public class Customer
# {
#   public string FirstName { get; private set; }
#   public string LastName { get; private set; }
#
#   public void ChangeName(ChangeNameCommand command) {
#     FirstName = command.FirstName;
#     LastName = command.LastName;
#   }
# }
# ChangeNameCommand change_name_cmd = new ChangeNameCommand();
# ChangeNameValidator validator = new ChangeNameValidator();
# ValidationResult results = validator.Validate(change_name_cmd);
#
# bool validationSucceeded = results.IsValid;
# IList<ValidationFailure> failures = results.Errors;

# The key difference here is that I’m validating a command, not an entity. And since entities themselves are not
# validation libraries, it’s much, much cleaner to validate at the command level. Because the command is the form I’m
#  presenting to the user, any validation errors are easily correlated to the UI since the command was used to build
# the form in the first place.
# Validate commands, not entities, and perform the validation at the edges.

# normal way of using FluentValidation (without command) is:

# using FluentValidation;
#
# public class CustomerValidator: AbstractValidator<Customer> {
#   public CustomerValidator() {
#     RuleFor(customer => customer.Surname).NotEmpty();
#     RuleFor(customer => customer.Forename).NotEmpty().WithMessage("Please specify a first name");
#     RuleFor(customer => customer.Discount).NotEqual(0).When(customer => customer.HasDiscount);
#     RuleFor(customer => customer.Address).Length(20, 250);
#     RuleFor(customer => customer.Postcode).Must(BeAValidPostcode).WithMessage("Please specify a valid postcode");
#   }
#
#   private bool BeAValidPostcode(string postcode) {
#     // custom postcode validating logic goes here
#   }
# }
#
# Customer customer = new Customer();
# CustomerValidator validator = new CustomerValidator();
# ValidationResult results = validator.Validate(customer);
#
# bool validationSucceeded = results.IsValid;
# IList<ValidationFailure> failures = results.Errors;



