def main() -> int:
    a = 2.0
    b = int(a)
    c = float(b)
    float_str = "  0.10 "
    f1 = float(float_str)
    int_str = "100"
    i1 = int(int_str)
    i2 = int(int_str, 2)
    print(a, b, c, f1, i1, i2)
    return 0
