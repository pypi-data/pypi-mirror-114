import datetime
import re


def parse_date(value, multiple):
    """
    Checks if the given value is a date of the required format. Throws an error if invalid
    :param value: string - The input value
    :param multiple: bool - Indicates whether to return in array format or just the value
    :return: string|array - The value which represents the date
    """
    date_format = "%Y-%m-%d"

    try:
        datetime.datetime.strptime(value, date_format)
        # hack for returning array for custom properties
        if multiple:
            return [value]
        else:
            return value
    except ValueError:
        raise ValueError("Incorrect date format")


def parse_type(data_type, value, multiple):
    """
    Converts and check if the value provided matches the datatype provided. Throws an error if invalid.
    :param data_type: str|int|float - the type of the data to check
    :param value: string - The input value
    :param multiple: bool - Indicate whether are multiple values in the value field
    :return: value|array -  The value/values converted to that data type
    """
    try:
        if multiple:
            parsed_values = []
            value_parts = value.split(",")
            for part in value_parts:
                parsed_values.append(data_type(part.strip()))

            return parsed_values
        else:
            return data_type(value)
    except ValueError:
        raise ValueError("Incorrect date format")


type_map = {
    "string": lambda data, multiple: parse_type(str, data, multiple),
    "int": lambda data, multiple: parse_type(int, data, multiple),
    "float": lambda data, multiple: parse_type(float, data, multiple),
    "date": lambda data, multiple: parse_date(data, multiple)
}


def clean_data(text):
    return re.sub(r"\r\n\t", "", text)