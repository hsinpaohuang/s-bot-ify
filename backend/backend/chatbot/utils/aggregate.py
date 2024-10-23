def aggregate(data: list[str]):
    """
    Aggregates the given data using the following rule:

    If the length of data is 1, simply return it

    If the length of data is 2, return "1 and 2"

    Otherwise, return "1, 2, ..., and n"

    :param data: a list of strings to be aggregated

    :returns: aggregated_string the aggregated result
    """

    match len(data):
        case 0:
            raise ValueError('Data must have at least 1 item')
        case 1:
            return data[0]
        case 2:
            return f'{data[0]} and {data[1]}'
        case _:
            return  f"{', '.join(data[:-1])}, and {data[-1]}"
