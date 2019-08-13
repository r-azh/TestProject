# It is better to not directly model the discrete classes, but rather the probability that a feature value belongs to
# class 1, P(X). Once we possess such a model, we could then predict class 1 if P(X)>0.5, and class 0 otherwise.
# p112 of book
# log_reg_example.py from book