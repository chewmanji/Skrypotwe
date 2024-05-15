from typing import Iterable

def forall(pred: callable, iterable: Iterable) -> bool:
    """Checks if all elements in the iterable satisfy the predicate.

    Args:
        pred: A callable function that takes an element from the iterable and
              returns True if the element satisfies the condition, False otherwise.
        iterable: An iterable object (e.g., list, tuple, string) to check.

    Returns:
        True if all elements in the iterable satisfy the predicate, False otherwise.
    """
    return all(pred(el) for el in iterable)


def exists(pred: callable, iterable: Iterable) -> bool:
    """Checks if any element in the iterable satisfy the predicate.

    Args:
        pred: A callable function that takes an element from the iterable and
              returns True if the element satisfies the condition, False otherwise.
        iterable: An iterable object (e.g., list, tuple, string) to check.

    Returns:
        True if any element in the iterable satisfy the predicate, False otherwise.
    """
    return any(pred(el) for el in iterable)


def atleast(n: int, pred: callable, iterable: Iterable) -> bool:
    return sum(map(pred, iterable)) >= n

def atmost(n: int, pred: callable, iterable: Iterable) -> bool:
    return sum(map(pred, iterable)) <= n


if __name__ == "__main__":
    print(forall(lambda x: x > 1, [2, 3, 5]))
    print(forall(lambda x: x > 1, [1, 2, 3, 5]))
    print(forall(lambda x: x > 1, []), "\n")

    print(exists(lambda x: x > 1, [-2, -1, 0]))
    print(exists(lambda x: x > 1, [-2, -1, 0, 2]))
    print(exists(lambda x: x > 1, []), "\n")

    print(atleast(3, lambda x: x > 1, [1, 2, 3, 5]))
    print(atleast(3, lambda x: x > 1, [1, 3, 5]))
    print(atleast(3, lambda x: x > 1, []), "\n")

    print(atmost(3, lambda x: x > 1, [1, 2, 3, 4, 5]))
    print(atmost(3, lambda x: x > 1, [1, 3, 5]))
    print(atmost(3, lambda x: x > 1, []), "\n")
