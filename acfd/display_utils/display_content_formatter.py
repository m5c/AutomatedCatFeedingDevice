"""
Helper module to format raw values into something that renders nicely on a digit display_utils.
"""


def to_zero_padded_number(number: int, padding: int) -> str:
    """
    Converts a provided integer below 10k to a zero padded display_utils content
    :param number: a number in 4 digit range.
    :param padding: as the total length expected as output number.
    """
    if number >= 10000:
        raise Exception("Number cannot be converted to padded display_utils content. Out of bounds.")
    padded_content: str = '0' * padding + str(number)
    length = len(padded_content)
    padded_content = padded_content[length - padding:length]
    return padded_content
