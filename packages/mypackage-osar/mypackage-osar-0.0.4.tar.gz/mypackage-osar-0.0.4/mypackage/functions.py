def add_numbers(*args, multiply=None):
    sum_num = 0
    for num in args:
        sum_num = sum_num + num
    if multiply is not None:
        return sum_num * multiply
    return sum_num
