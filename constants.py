OPS = {
    '=': lambda a, b: a == b,
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b
}

AGGS = {
    'avg': lambda values: sum(values) / len(values) if values else 0,
    'min': min,
    'max': max
}