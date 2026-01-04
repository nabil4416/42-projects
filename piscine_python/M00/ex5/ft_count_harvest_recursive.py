def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    _count(days, 1)

def _count(days, current):
    if current > days:
        print("Harvest time!")
    else:
        print("Day", current)
        _count(days, current + 1)
