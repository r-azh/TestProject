__author__ = 'R.Azh'


# public interface IValidator<T>
# {
#     bool IsValid(T entity);
#     IEnumerable<string> BrokenRules(T entity);
# }

# public interface IValidatable<T>
# {
#     bool Validate(IValidator<T> validator, out IEnumerable<string> brokenRules);
# }
#
# public class Order
# {
#     public int Id { get; set; }
#     public string Customer { get; set; }
# }
#
# public class Order : IValidatable<Order>
# {
#     public int Id { get; set; }
#     public string Customer { get; set; }
#
#     public bool Validate(IValidator<Order> validator, out IEnumerable<string> brokenRules)
#     {
#         brokenRules = validator.BrokenRules(this);
#         return validator.IsValid(this);
#     }
# }
#
#  I also created the “IValidatable” interface so I can keep track of what can be validated and what can’t.
# public class OrderPersistenceValidator : IValidator<Order>
# {
#     public bool IsValid(Order entity)
#     {
#         return BrokenRules(entity).Count() > 0;
#     }
#
#     public IEnumerable<string> BrokenRules(Order entity)
#     {
#         if (entity.Id < 0)
#             yield return "Id cannot be less than 0.";
#
#         if (string.IsNullOrEmpty(entity.Customer))
#             yield return "Must include a customer.";
#
#         yield break;
#     }
# }

# Order order = new Order();
# OrderPersistenceValidator validator = new OrderPersistenceValidator();
#
# IEnumerable<string> brokenRules;
# bool isValid = order.Validate(validator, out brokenRules);

# I can use an extension method for the Order type to wrap the creation of the validator class

#  public static bool ValidatePersistence(this Order entity, out IEnumerable<string> brokenRules)
# {
#     IValidator<Order> validator = new OrderPersistenceValidator();
#
#     return entity.Validate(validator, brokenRules);
# }
# Now my client code is a little more bearable:
#
# Order order = new Order();
#
# IEnumerable<string> brokenRules;
# bool isValid = order.ValidatePersistence(out brokenRules);

# Taking this one step further, I can use a Registry to register validators based on types, and create a more generic
#  extension method that relies on constraints:
#
# public class Validator
# {
#     private static Dictionary<Type, object> _validators = new Dictionary<Type, object>();
#
#     public static void RegisterValidatorFor<T>(T entity, IValidator<T> validator)
#         where T : IValidatable<T>
#     {
#         _validators.Add(entity.GetType(), validator);
#     }
#
#     public static IValidator<T> GetValidatorFor<T>(T entity)
#         where T : IValidatable<T>
#     {
#         return _validators[entity.GetType()] as IValidator<T>;
#     }
#
#     public static bool Validate<T>(this T entity, out IEnumerable<string> brokenRules)
#         where T : IValidatable<T>
#     {
#         IValidator<T> validator = Validator.GetValidatorFor(entity);
#
#         return entity.Validate(validator, out brokenRules);
#     }
# }
