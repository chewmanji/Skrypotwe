import sys
import argparse


def tail(filename, lines=10):
    lines_to_read = lines
    if filename is None:
        file = sys.stdin
    else:
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print(f"Błąd: Plik '{filename}' nie istnieje.")
            return

    data = file.readlines()

    lines_to_read = min(len(data), lines)

    for line in data[-lines_to_read:]:  # slice'owanie listy
        print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wypisuje ostatnie linie pliku lub danych przekazanych na wejście standardowe."
    )
    parser.add_argument("filename", help="Ścieżka do pliku.")
    parser.add_argument(
        "--lines", type=int, default=10, help="Liczba linii do wyświetlenia."
    )
    args = parser.parse_args()

    tail(args.filename, args.lines)
