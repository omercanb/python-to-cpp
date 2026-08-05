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
ptr<_SpecialForm> Tuple;
void in_set();
void set_literal_iteration();

void in_set() {
    ptr<list<tuple<_int, _int>>> a;
    _int j;
    _int i;
    _int n;
    tuple<_int, _int> s;
    a = ptr(new list<tuple<_int, _int>>());
    _int __stop_1 = 100LL;
    for (j = 0; j < __stop_1; ++j) {
        _int __stop_2 = 10LL;
        for (i = 0; i < __stop_2; ++i) {
            a->append(tuple((i * 2LL), i));
            a->append(tuple(i, (i + 2LL)));
            a->append(tuple(i, i));
            a->append(tuple(i, i));
        }
    }
    n = 0LL;
    _int __stop_3 = 1000LL;
    for (i = 0; i < __stop_3; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            s = next(__iter_4);
            if (to_bool((s.__contains__(6LL)))) {
                n += 1LL;
            }
            if (to_bool((ptr(new set<_int>({3LL, 4LL, 5LL}))->__contains__(i)))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 612000LL))))) throw AssertionError(to_str(n));
}

void set_literal_iteration() {
    _int n;
    _int p;
    _int l;
    _int i;
    str s;
    bool a;
    n = 0LL;
    _int __stop_5 = 1000LL;
    for (p = 0; p < __stop_5; ++p) {
        _int __stop_6 = 10LL;
        for (l = 0; l < __stop_6; ++l) {
            for (auto __iter_7 = iter(ptr(new set<_int>({1LL, 2LL, 3LL, 4LL, 5LL, 6LL, 7LL, 8LL, 9LL, 10LL}))); !__iter_7.done();) {
                i = next(__iter_7);
                n += i;
            }
            for (auto __iter_8 = iter(ptr(new set<str>({str("yes"), str("no")}))); !__iter_8.done();) {
                s = next(__iter_8);
                if (to_bool(((s == str("yes"))))) {
                    n += 1LL;
                }
            }
            for (auto __iter_9 = iter(ptr(new set<bool>({true, false}))); !__iter_9.done();) {
                a = next(__iter_9);
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 580000LL))))) throw AssertionError(to_str(n));
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        set_literal_iteration(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    