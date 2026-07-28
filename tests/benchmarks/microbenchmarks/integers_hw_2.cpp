#include <cassert>
#include <cstdint>
#include <vector>

void int_bitwise_ops() {
    std::vector<int64_t> a;
    for (int i = 0; i < 1000; i++)
        a.push_back((int64_t)i * i * 12753 % ((1 << 20) - 1));
    std::vector<int64_t> b;
    for (int t = 0; t < 40; t++)
        b.push_back(a[10 + t]);
    int64_t n = 0;
    for (int i = 0; i < 50; i++)
        for (int64_t j : a)
            for (int64_t k : b) {
                j |= k;
                j &= ~(j ^ k);
                int64_t x = j >> 5;
                n += x;
                n += x << 1;
                n &= 0xFFFFFF;
            }
    assert(n == 4867360);
}

void int_bitwise_ops2() {
    std::vector<int64_t> a;
    for (int i = 0; i < 1000; i++)
        a.push_back((int64_t)i * i * 2654435761LL & 0xFFFFFFFF);
    std::vector<int64_t> b;
    for (int t = 0; t < 49; t++)
        b.push_back(a[10 + t * 10]);
    int64_t n = 0;
    for (int i = 0; i < 10; i++)
        for (int64_t j : a)
            for (int64_t k : b) {
                j |= k;
                j &= ~(j ^ k);
                if ((1LL << (i * 3)) & j)
                    n += 1;
                n += j & 1;
            }
    assert(n == 183000);
}
