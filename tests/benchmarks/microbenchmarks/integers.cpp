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
#include "dict.h"
#include "set.h"
#include "file.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
#include "builtins.h"
using namespace py;
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
    _int __stop_1 = 1000LL;
    for (i = 0; i < __stop_1; ++i) {
        a->append(mod(((i * i) * 12753LL), (pow(2LL, 20LL) - 1LL)));
    }
    b = ptr(new list<_int>());
    _int __stop_2 = 40LL;
    for (t = 0; t < __stop_2; ++t) {
        b->append(a->__getitem__((10LL + t)));
    }
    n = 0LL;
    _int __stop_3 = 50LL;
    for (i = 0; i < __stop_3; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            j = next(__iter_4);
            for (auto __iter_5 = iter(b); !__iter_5.done();) {
                k = next(__iter_5);
                x = (j >> 5LL);
            }
        }
    }
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
    _int __stop_6 = 1000LL;
    for (i = 0; i < __stop_6; ++i) {
        a->append((((i * i) * 2654435761LL) & 4294967295LL));
    }
    b = ptr(new list<_int>());
    _int __stop_7 = 49LL;
    for (t = 0; t < __stop_7; ++t) {
        b->append(a->__getitem__((10LL + (t * 10LL))));
    }
    n = 0LL;
    _int __stop_8 = 10LL;
    for (i = 0; i < __stop_8; ++i) {
        for (auto __iter_9 = iter(a); !__iter_9.done();) {
            j = next(__iter_9);
            for (auto __iter_10 = iter(b); !__iter_10.done();) {
                k = next(__iter_10);
                if (to_bool(((1LL << (i * 3LL)) & j))) {
                }
            }
        }
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        int_bitwise_ops2(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    