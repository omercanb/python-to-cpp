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
    for (_int j = 0; j < 100LL; ++j) {
        for (_int i = 0; i < 10LL; ++i) {
            a->append(tuple((i * 2LL)));
            a->append(tuple(i, (i + 2LL)));
            a->append((tuple(i) * 6LL));
            a->append(tuple());
        }
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            s = next(__iter_1);
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
    for (_int _ = 0; _ < 1000LL; ++_) {
        for (_int _ = 0; _ < 10LL; ++_) {
            for (auto __iter_2 = iter(ptr(new set<_int>({1LL, 2LL, 3LL, 4LL, 5LL, 6LL, 7LL, 8LL, 9LL, 10LL}))); !__iter_2.done();) {
                i = next(__iter_2);
            }
            for (auto __iter_3 = iter(ptr(new set<str>({str("yes"), str("no")}))); !__iter_3.done();) {
                s = next(__iter_3);
                if (to_bool(((s == str("yes"))))) {
                }
            }
            for (auto __iter_4 = iter(ptr(new set<bool>({true, false}))); !__iter_4.done();) {
                a = next(__iter_4);
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
    