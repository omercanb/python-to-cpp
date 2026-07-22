def main() -> int:
    s = "Hello World"
    print(s)
    print(len(s))
    print(s[0], s[-1])

    print(s.upper())
    print(s.lower())
    print(s.swapcase())
    print(s.capitalize())
    print("hello world".title())
    print(s.casefold())

    print(s.find("o"))
    print(s.find("o", 5))
    print(s.rfind("o"))
    print(s.find("zz"))
    print(s.index("World"))
    print(s.count("l"))
    print(s.count("zz"))
    print(s.startswith("Hello"))
    print(s.startswith("World"))
    print(s.endswith("World"))

    print(s.replace("l", "L"))
    print(s.replace("l", "L", 2))
    print(s.removeprefix("Hello "))
    print(s.removesuffix(" World"))

    padded = "  spaced  "
    print(padded.strip())
    print(padded.lstrip())
    print(padded.rstrip())
    print("xxhixx".strip("x"))

    print("hi".ljust(5, "."))
    print("hi".rjust(5, "."))
    print("hi".center(6, "."))
    print("42".zfill(5))
    print("-42".zfill(5))

    print("abc".isalpha(), "a1".isalpha())
    print("123".isdigit(), "12a".isdigit())
    print("a1".isalnum(), "a-1".isalnum())
    print("  ".isspace(), "a ".isspace())
    print("ABC".isupper(), "Abc".isupper())
    print("abc".islower(), "Abc".islower())

    print(s.split())
    print("a,b,c".split(","))
    print("a,,b".split(","))
    print("-".join("a,b,c".split(",")))
    print("one\ntwo".splitlines())

    a = "foo"
    b = "bar"
    print(a + b)
    print(a * 3)
    print(a == "foo", a == b)
    print(a < b, a > b)

    print(str(42))
    print(str(3.5))
    print(str(True))
    print(int("100"))
    print(float("0.5"))

    joined = ""
    for c in "abc":
        joined = joined + c + "."
    print(joined)

    return 0
