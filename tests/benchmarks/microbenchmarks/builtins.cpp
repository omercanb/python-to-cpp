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
void min_max_pair();
void min_max_sequence();
_int inc(_int x);
void __init_module__();

void __init_module__() {
}

void min_max_pair() {
    ptr<list<_int>> a;
    _int i;
    _int expected_min;
    _int expected_max;
    _int n;
    _int m;
    _int j;
    a = ptr(new list<_int>());
    _int __stop_1 = 20LL;
    for (i = 0; i < __stop_1; ++i) {
        a->append(mod((i * 12753LL), (pow(2LL, 15LL) - 1LL)));
    }
    expected_min = min(a);
    expected_max = max(a);
    n = 0LL;
    _int __stop_2 = (100LL * 1000LL);
    for (i = 0; i < __stop_2; ++i) {
        n = 1000000000LL;
        m = 0LL;
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            j = next(__iter_3);
            n = min(n, j);
            m = max(m, j);
        }
        if (!(to_bool(((n == expected_min))))) throw AssertionError("");
        if (!(to_bool(((m == expected_max))))) throw AssertionError("");
    }
}

void min_max_sequence() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    _int x;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_4 = 1000LL;
    for (i = 0; i < __stop_4; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append((ptr(new list<_int>({i})) * 15LL));
    }
    n = 0LL;
    _int __stop_5 = 100LL;
    for (i = 0; i < __stop_5; ++i) {
        for (auto __iter_6 = iter(a); !__iter_6.done();) {
            s = next(__iter_6);
            x = min(s);
            n += x;
            x = max(s);
            n += x;
        }
    }
    if (!(to_bool(((n == 399800000LL))))) throw AssertionError(to_str(n));
}

_int inc(_int x) {
    return (x + 1LL);
}


    int main() {
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        min_max_sequence(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    