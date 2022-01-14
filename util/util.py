def normalize(value: float, lower_bound: int, upper_bound: int):
    bound_range = upper_bound - lower_bound
    return (value - lower_bound) / bound_range
