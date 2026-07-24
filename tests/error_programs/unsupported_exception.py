def main() -> int:
    try:
        print(int("x"))
    except LookupError:
        print("bad")
    return 0
