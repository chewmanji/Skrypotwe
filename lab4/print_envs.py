from os import environ
from sys import argv


def main():
    if len(argv) == 1:
        for env in environ:
            print(f"{env} = {environ[env]}")

    else:
        argv.sort()
        for arg in argv:#filtered z lambdą zamiast zwyklego iterowania
            for env in environ:
                if arg in env.lower():
                    print(f"{env}:\n\t{environ[env]}")


if __name__ == "__main__":
    main()
