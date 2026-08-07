def main() -> int:
    b = b"Hello World"
    print(b)
    print(len(b))
    print(b[0], b[-1])

    print(b.upper())
    print(b.lower())
    print(b.swapcase())
    print(b.capitalize())
    print(b"hello world".title())

    print(b.find(b"o"))
    print(b.find(b"o", 5))
    print(b.rfind(b"o"))
    print(b.find(b"zz"))
    print(b.index(b"World"))
    print(b.count(b"l"))
    print(b.count(b"zz"))
    print(b.startswith(b"Hello"))
    print(b.startswith(b"World"))
    print(b.endswith(b"World"))

    print(b.replace(b"l", b"L"))
    print(b.replace(b"l", b"L", 2))
    print(b.removeprefix(b"Hello "))
    print(b.removesuffix(b" World"))

    padded = b"  spaced  "
    print(padded.strip())
    print(padded.lstrip())
    print(padded.rstrip())
    print(b"xxhixx".strip(b"x"))

    print(b"hi".ljust(5, b"."))
    print(b"hi".rjust(5, b"."))
    print(b"hi".center(6, b"."))
    print(b"42".zfill(5))
    print(b"-42".zfill(5))

    print(b"abc".isalpha(), b"a1".isalpha())
    print(b"123".isdigit(), b"12a".isdigit())
    print(b"a1".isalnum(), b"a-1".isalnum())
    print(b"  ".isspace(), b"a ".isspace())
    print(b"ABC".isupper(), b"Abc".isupper())
    print(b"abc".islower(), b"Abc".islower())

    print(b.split())
    print(b"a,b,c".split(b","))
    print(b"a,,b".split(b","))
    print(b"-".join(b"a,b,c".split(b",")))
    print(b"one\ntwo".splitlines())

    a = b"foo"
    c = b"bar"
    print(a + c)
    print(a * 3)
    print(a == b"foo", a == c)
    print(a < c, a > c)

    print(b"World" in b)
    print(87 in b)
    print(90 in b)

    print(bytes(3))
    print(bytes([65, 66, 67]))

    total = 0
    for byte in b"abc":
        total += byte
    print(total)

    joined = b""
    for byte in b"abc":
        joined = joined + bytes([byte]) + b"."
    print(joined)

    return 0
