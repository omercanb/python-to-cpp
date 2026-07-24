def num() -> int:
    return 0


def main() -> int:
    try:
        int("no")
    except Exception as e:
        print(e)
    else:
        print("yes")
    try:
        int("no")
    except Exception as e:
        print(e)
    else:
        print("yes")
    step = 2
    return 0
