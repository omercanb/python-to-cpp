def main() -> int:
    SAMPLE = "tests/test_files/sample.txt"
    handle = open(SAMPLE)
    text = handle.read()
    print(len(text))
    print(text.splitlines())
    # a second read starts from where the first stopped
    print(len(handle.read()))
    handle.close()

    # readline keeps the newline and advances the position
    stepped = open(SAMPLE)
    print(stepped.readline().strip())
    print(stepped.readline().strip())
    rest = stepped.readlines()
    print(len(rest), rest[0].strip())
    print(len(stepped.readlines()))

    # iterating a file yields its lines
    lines = open(SAMPLE)
    for line in lines:
        print(len(line), line.strip())

    # writing, then reading it back
    out = open("tests/test_files/sample_out.txt", "w")
    print(out.write("alpha\n"))
    print(out.write("beta\n"))
    out.close()
    written = open("tests/test_files/sample_out.txt").read()
    print(written.splitlines(), len(written))

    try:
        open("tests/test_files/no_such_file.txt")
    except FileNotFoundError:
        print("missing file raised")

    return 0
