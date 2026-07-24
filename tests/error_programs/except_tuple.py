def main() -> int:
    try:
        print(int("x"))
    except (ValueError, KeyError):
        print("bad")
    return 0
