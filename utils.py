from typing import List, Dict, Tuple, Union, Callable, Optional
from constants import OPS, AGGS


def parse_cond(cond: str, sup_ops: Dict[str, Callable]) -> Tuple[str, str, str]:
    for op in sup_ops:
        if op in cond:
            parts = cond.split(op, 1)
            if len(parts) == 2:
                return parts[0].strip(), op, parts[1].strip()
    raise ValueError(f"Неправильный формат условия: '{cond}'")


def check_column_type(data: List[Dict[str, str]], column: str) -> str:
    for row in data:
        value = row.get(column, '')
        if value:
            try:
                float(value)
                return 'number'
            except ValueError:
                pass
    return 'string'


def convert_value(value: str, col_type: str) -> Union[float, str]:
    try:
        return float(value) if col_type == 'number' else value
    except ValueError:
        raise ValueError(f"Значение '{value}' не является допустимым числом")


def filter_data(data: List[Dict[str, str]], where: str) -> List[Dict[str, str]]:
    col_name, operator, value_str = parse_cond(where, OPS)

    if col_name not in data[0]:
        raise ValueError(f"Столбец '{col_name}' не найден в CSV")

    col_type = check_column_type(data, col_name)
    value = convert_value(value_str, col_type)

    op_func = OPS[operator]
    filtered = []
    for row in data:
        cell = row[col_name]
        try:
            cell_val = float(cell) if col_type == 'number' else cell
            if op_func(cell_val, value):
                filtered.append(row)
        except ValueError:
            continue
    return filtered


def aggregate_data(data: List[Dict[str, str]], aggregate: str) -> float:
    col_name, operation, agg = parse_cond(aggregate, {'=': None})

    if operation != '=':
        raise ValueError("Формат аггрегации должен быть 'столбец=оператор'")

    if col_name not in data[0]:
        raise ValueError(f"Столбец '{col_name}' не найден в CSV")

    values = []
    for row in data:
        try:
            values.append(float(row[col_name]))
        except (ValueError, TypeError):
            raise ValueError(f"Нечисловое значение в столбце '{col_name}'")

    if not values:
        return 0.0

    return AGGS[agg](values)
