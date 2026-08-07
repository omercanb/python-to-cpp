#include <chrono>
#include "types.h"
#include "exceptions.h"
#include "finally.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "slice.h"
#include "list.h"
#include "strops.h"
#include "bytes.h"
#include "dict.h"
#include "set.h"
#include "file.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
#include "builtins.h"
using namespace py;
void int_bitwise_ops();
void int_bitwise_ops2();
void __init_module__();

void __init_module__() {
}

void int_bitwise_ops() {
    ptr<list<_int>> a;
    _int i;
    ptr<list<_int>> b;
    _int t;
    _int n;
    _int j;
    _int k;
    _int x;
    a = ptr(new list<_int>());
    _int __stop_0 = 1000LL;
    for (i = 0; i < __stop_0; ++i) {
        a->append(mod(((i * i) * 12753LL), (pow(2LL, 20LL) - 1LL)));
    }
    b = ptr(new list<_int>());
    _int __stop_1 = 40LL;
    for (t = 0; t < __stop_1; ++t) {
        b->append(a->__getitem__((10LL + t)));
    }
    n = 0LL;
    _int __stop_2 = 50LL;
    for (i = 0; i < __stop_2; ++i) {
        for (auto __iter_0 = iter(a); !__iter_0.done();) {
            j = next(__iter_0);
            for (auto __iter_1 = iter(b); !__iter_1.done();) {
                k = next(__iter_1);
                j |= k;
                j &= (~(j ^ k));
                x = (j >> 5LL);
                n += x;
                n += (x << 1LL);
                n &= 16777215LL;
            }
        }
    }
    if (!(to_bool(((n == 4867360LL))))) throw AssertionError("");
}

void int_bitwise_ops2() {
    ptr<list<_int>> a;
    _int i;
    ptr<list<_int>> b;
    _int t;
    _int n;
    _int j;
    _int k;
    a = ptr(new list<_int>());
    _int __stop_3 = 1000LL;
    for (i = 0; i < __stop_3; ++i) {
        a->append((((i * i) * 2654435761LL) & 4294967295LL));
    }
    b = ptr(new list<_int>());
    _int __stop_4 = 49LL;
    for (t = 0; t < __stop_4; ++t) {
        b->append(a->__getitem__((10LL + (t * 10LL))));
    }
    n = 0LL;
    _int __stop_5 = 10LL;
    for (i = 0; i < __stop_5; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            j = next(__iter_2);
            for (auto __iter_3 = iter(b); !__iter_3.done();) {
                k = next(__iter_3);
                j |= k;
                j &= (~(j ^ k));
                if (to_bool(((1LL << (i * 3LL)) & j))) {
                    n += 1LL;
                }
                n += (j & 1LL);
            }
        }
    }
    if (!(to_bool(((n == 183000LL))))) throw AssertionError("");
}


    int main() {
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        int_bitwise_ops2(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    