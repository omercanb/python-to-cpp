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
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(mod(((i * i) * 12753LL), (pow(2LL, 20LL) - 1LL)));
    }
    b = ptr(new list<_int>());
    for (_int t = 0; t < 40LL; ++t) {
        b->append(a->__getitem__((10LL + t)));
    }
    n = 0LL;
    for (_int i = 0; i < 50LL; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            j = next(__iter_1);
            for (auto __iter_2 = iter(b); !__iter_2.done();) {
                k = next(__iter_2);
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
    for (_int i = 0; i < 1000LL; ++i) {
        a->append((((i * i) * 2654435761LL) & 4294967295LL));
    }
    b = ptr(new list<_int>());
    for (_int t = 0; t < 49LL; ++t) {
        b->append(a->__getitem__((10LL + (t * 10LL))));
    }
    n = 0LL;
    for (_int i = 0; i < 10LL; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            j = next(__iter_3);
            for (auto __iter_4 = iter(b); !__iter_4.done();) {
                k = next(__iter_4);
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
    