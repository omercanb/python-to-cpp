def main() -> int:
    try:
        print(int("x"))
    except* ValueError as error:
        print("bad")
    return 0
