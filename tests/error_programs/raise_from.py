def main() -> int:
    try:
        print(int("x"))
    except ValueError as error:
        raise KeyError("missing") from error
    return 0
