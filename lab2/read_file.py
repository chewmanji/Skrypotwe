def read_file():
    while True:
        try:
            print(input())
        except EOFError:
            break

if __name__ == "__main__":
    read_file()
