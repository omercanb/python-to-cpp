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
str("Benchmarks for built-in functions (that don't fit elsewhere).");
void min_max_pair() {
    ptr<list<_int>> a;
    _int i;
    _int expected_min;
    _int expected_max;
    _int n;
    _int m;
    _int j;
    a = ptr(new list<_int>());
    for (_int i = 0; i < 20LL; ++i) {
        a->append(mod((i * 12753LL), (pow(2LL, 15LL) - 1LL)));
    }
    expected_min = min(a);
    expected_max = max(a);
    n = 0LL;
    for (_int i = 0; i < (100LL * 1000LL); ++i) {
        n = 1000000000LL;
        m = 0LL;
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            j = next(__iter_1);
            n = min(n, j);
            m = max(m, j);
        }
    }
}

void min_max_sequence() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    _int x;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append((ptr(new list<_int>({i})) * 15LL));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            s = next(__iter_2);
            x = min(s);
            x = max(s);
        }
    }
}

void map_builtin() {
    ptr<list<ptr<list<_int>>>> a;
    _int j;
    _int i;
    _int n;
    _int k;
    ptr<list<_int>> lst;
    ptr<list<_int>> x;
    str y;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int j = 0; j < 100LL; ++j) {
        for (_int i = 0; i < 10LL; ++i) {
            a->append(ptr(new list<_int>({(i * 2LL)})));
            a->append(ptr(new list<_int>({i, (i + 2LL)})));
            a->append((ptr(new list<_int>({i})) * 6LL));
        }
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        k = 0LL;
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            lst = next(__iter_3);
            x = ptr(new list<_int>(map(inc, lst)));
            if (to_bool(((k == 0LL)))) {
                y = str("").join(map(str, lst));
            }
            if (to_bool(((k == 3LL)))) {
                k = 0LL;
            }
        }
    }
}

_int inc(_int x) {
    return (x + 1LL);
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        min_max_pair(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    