from string import whitespace
from typing import List, Any


def acronym(words: list[str]) -> str:
    """
    Creates an acronym from the first letters of non-empty words in the input list.

    Args:
        words: A list of strings.

    Returns:
        A string containing the acronym, or an empty string if the input list is empty
        or contains only empty strings.
    """
    return "".join([word[0] for word in words if word])


def median(numbers: list[int]) -> int | float | None:
    """
    Calculates the median of a list of numbers.

    Args:
        numbers: A list of integers.

    Returns:
        The median of the list, or None if the list is empty.
    """

    def median_helper(numbers: list[int]) -> int | float:
        numbers.sort()
        size = len(numbers)
        is_odd = size % 2 != 0
        n = size - 1
        return (
            numbers[((n + 1) // 2)]
            if is_odd
            else (numbers[n // 2] + numbers[(n // 2) + 1]) / 2
        )

    return median_helper(numbers) if numbers else None


def square(x: float, epsilon: float) -> float | None:
    """
    Approximates the square of a positive number using the Newton's method.

    Args:
        x: The positive number to find the square of.
        epsilon: The desired tolerance for the approximation. A smaller epsilon value means a more accurate approximation but also requires more iterations.

    Returns:
        The approximate square of x, or None if x is not positive.
    """

    def square_helper(result: float) -> float:
        return (
            result
            if abs(result**2 - x) < epsilon
            else square_helper((result + (x / result)) / 2)
        )

    return square_helper(x - x / 2) if x > 0 else None


def make_alpha_dict(string: str) -> dict[str, list[str]]:
    """
    Creates a dictionary mapping each unique alphabetical character in a string to a list of words in the string that contain that character.

    Args:
        string: The input string.

    Returns:
        A dictionary mapping alphabet characters to lists of words containing those characters.
    """
    chars = set(filter(lambda char: char not in whitespace, string))
    words = string.split()
    return {char: [word for word in words if char in word] for char in chars}


def flatten(data: List[Any]) -> List[Any]:
    return (
        [data]
        if not isinstance(data, list)
        else [lst for sublst in map(flatten, data) for lst in sublst]
    )

if __name__ == "__main__":
    print(acronym(["Zaklad", "", "Społe"]))
    print(acronym([]))

    print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))
    print(median([1, 2, 3, 4]))
    print(median([1, 2, 3]))
    print(median([]))

    print(square(9, 0.1))
    print(square(9, 0.000000001))
    print(square(2, 0.001))
    print(square(-3, 0.001))

    print(make_alpha_dict("on i ona"))
    print(make_alpha_dict("cyfry2 2 i $pecjalne! !!!"))
    print(make_alpha_dict(""))

    print(flatten([1, [2, 3], [[4, 5], 6]]))
    print(flatten([1, 2, 3, 4, 5, 6]))
    print(flatten([]))
