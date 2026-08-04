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
void in_set() {
    ptr<list<ptr<tuple>>> a;
    _int j;
    _int i;
    _int n;
    ptr<tuple> s;
    a = ptr(new list<ptr<tuple>>());
    _int __stop_1 = 100LL;
    for (j = 0; j < __stop_1; ++j) {
        _int __stop_2 = 10LL;
        for (i = 0; i < __stop_2; ++i) {
            a->append(tuple((i * 2LL)));
            a->append(tuple(i, (i + 2LL)));
            a->append((tuple(i) * 6LL));
            a->append(tuple());
        }
    }
    n = 0LL;
    _int __stop_3 = 1000LL;
    for (i = 0; i < __stop_3; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            s = next(__iter_4);
            if (to_bool((s->__contains__(6LL)))) {
            }
            if (to_bool((ptr(new set<_int>({3LL, 4LL, 5LL}))->__contains__(i)))) {
            }
        }
    }
}

void set_literal_iteration() {
    _int n;
    auto _;
    _int i;
    str s;
    bool a;
    n = 0LL;
    _int __stop_5 = 1000LL;
    for (_ = 0; _ < __stop_5; ++_) {
        _int __stop_6 = 10LL;
        for (_ = 0; _ < __stop_6; ++_) {
            for (auto __iter_7 = iter(ptr(new set<_int>({1LL, 2LL, 3LL, 4LL, 5LL, 6LL, 7LL, 8LL, 9LL, 10LL}))); !__iter_7.done();) {
                i = next(__iter_7);
            }
            for (auto __iter_8 = iter(ptr(new set<str>({str("yes"), str("no")}))); !__iter_8.done();) {
                s = next(__iter_8);
                if (to_bool(((s == str("yes"))))) {
                }
            }
            for (auto __iter_9 = iter(ptr(new set<bool>({true, false}))); !__iter_9.done();) {
                a = next(__iter_9);
            }
        }
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        set_literal_iteration(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    