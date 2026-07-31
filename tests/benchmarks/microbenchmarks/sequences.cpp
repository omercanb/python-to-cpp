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
void list_slicing() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            s = next(__iter_1);
            if (to_bool(((len(s->__getitem__(slice(std::nullopt, 2LL, std::nullopt))) < 2LL)))) {
            }
            if (to_bool(((s->__getitem__(slice((-2LL), std::nullopt, std::nullopt)) == ptr(new list<_int>({0LL})))))) {
            }
            if (to_bool(((s == s->__getitem__(slice(std::nullopt, std::nullopt, (-1LL))))))) {
            }
        }
    }
}

void in_list() {
    ptr<list<ptr<list<_int>>>> a;
    _int j;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int j = 0; j < 100LL; ++j) {
        for (_int i = 0; i < 10LL; ++i) {
            a->append(ptr(new list<_int>({(i * 2LL)})));
            a->append(ptr(new list<_int>({i, (i + 2LL)})));
            a->append(ptr(new list<_int>({i})));
            a->append(ptr(new list<_int>()));
        }
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            s = next(__iter_2);
            if (to_bool((s->__contains__(6LL)))) {
            }
            if (to_bool((ptr(new list<_int>({3LL, 4LL, 5LL}))->__contains__(i)))) {
            }
        }
    }
}

void in_tuple() {
    ptr<list<tuple<_int, _int>>> a;
    _int j;
    _int i;
    _int n;
    tuple<_int, _int> s;
    a = ptr(new list<tuple<_int, _int>>());
    for (_int j = 0; j < 100LL; ++j) {
        for (_int i = 0; i < 10LL; ++i) {
            a->append(tuple((i * 2LL), 2LL));
            a->append(tuple(i, (i + 2LL)));
            a->append(tuple(i, 2LL));
            a->append(tuple(2LL, 2LL));
        }
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            s = next(__iter_3);
            if (to_bool((s.__contains__(6LL)))) {
            }
            if (to_bool((tuple(3LL, 4LL, 5LL).__contains__(i)))) {
            }
        }
    }
}

void list_append_small() {
    _int n;
    _int i;
    ptr<list<_int>> a;
    _int j;
    n = 0LL;
    for (_int i = 0; i < (200LL * 1000LL); ++i) {
        a = ptr(new list<_int>());
        for (_int j = 0; j < mod(i, 10LL); ++j) {
            a->append((j + i));
        }
    }
}

void list_append_large() {
    _int n;
    _int i;
    ptr<list<_int>> a;
    _int j;
    n = 0LL;
    for (_int i = 0; i < 2000LL; ++i) {
        a = ptr(new list<_int>());
        for (_int j = 0; j < i; ++j) {
            a->append((j + i));
        }
    }
}

void list_from_range() {
    ptr<list<_int>> a;
    _int j;
    _int i;
    _int n;
    ptr<list<_int>> lst;
    a = ptr(new list<_int>());
    for (_int j = 0; j < 100LL; ++j) {
        for (_int i = 0; i < 23LL; ++i) {
            a->append(mod((i * 7LL), 9LL));
        }
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            j = next(__iter_4);
            lst = ptr(new list<_int>(range(j)));
        }
    }
}

void list_copy() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> s;
    ptr<list<_int>> s2;
    ptr<list<_int>> s3;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < 100LL; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_5 = iter(a); !__iter_5.done();) {
            s = next(__iter_5);
            s2 = s->copy();
            s3 = s->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt));
        }
    }
}

ptr<list<_int>> comprehension_6() {
    ptr<list<_int>> __result_7 = ptr(new list<_int>());
    ptr<list<_int>> s;
    for (auto __iter_8 = iter(a); !__iter_8.done();) {
        s = next(__iter_8);
        __result_7->append(len(s));
    }
    return __result_7;
}

void list_remove() {
    _int j;
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> s;
    _int total;
    for (_int j = 0; j < (10LL * 1000LL); ++j) {
        a = ptr(new list<ptr<list<_int>>>());
        for (_int i = 0; i < 10LL; ++i) {
            a->append(ptr(new list<_int>(range((11LL + i)))));
        }
        for (_int i = 0; i < 10LL; ++i) {
            for (auto __iter_9 = iter(a); !__iter_9.done();) {
                s = next(__iter_9);
                s->remove(i);
            }
        }
        total = sum(comprehension_6());
    }
}

void list_insert() {
    _int j;
    ptr<list<_int>> a;
    _int i;
    for (_int j = 0; j < (10LL * 1000LL); ++j) {
        a = ptr(new list<_int>());
        for (_int i = 0; i < 10LL; ++i) {
            a->insert(0LL, i);
        }
        for (_int i = 0; i < 5LL; ++i) {
            a->insert(5LL, i);
        }
    }
}

void list_index() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < 100LL; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL), 44LL})));
        a->append(ptr(new list<_int>({44LL, i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i, 44LL})));
        a->append(ptr(new list<_int>({44LL})));
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_10 = iter(a); !__iter_10.done();) {
            s = next(__iter_10);
        }
    }
}

void list_add_in_place() {
    _int i;
    ptr<list<_int>> a;
    ptr<list<_int>> n;
    _int l;
    _int j;
    for (_int i = 0; i < (100LL * 1000LL); ++i) {
        a = ptr(new list<_int>());
        n = a;
        l = (5LL + mod(i, 10LL));
        for (_int j = 0; j < l; ++j) {
        }
    }
}

void list_concatenate() {
    bool flag;
    ptr<list<str>> x;
    ptr<list<str>> y;
    _int n;
    _int i;
    ptr<list<str>> a;
    ptr<list<str>> b;
    flag = false;
    x = ptr(new list<str>({str("x"), str("y"), str("z")}));
    y = ptr(new list<str>({str("1, 2")}));
    n = 0LL;
    for (_int i = 0; i < (1000LL * 1000LL); ++i) {
        a = x;
        if (to_bool(flag)) {
            b = (a + a);
        } else {
            b = ((y + a) + y);
        }
        flag = (!to_bool(flag));
    }
}

void list_equality() {
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int j;
    a = ptr(new list<_int>({1LL, 2LL}));
    n = 0LL;
    for (_int i = 0; i < 10000LL; ++i) {
        for (_int j = 0; j < 100LL; ++j) {
            if (to_bool(((a == ptr(new list<_int>({1LL, j})))))) {
            }
            if (to_bool(((a == ptr(new list<_int>({i, 2LL})))))) {
            }
        }
    }
}

void tuple_equality() {
    tuple<_int, _int> t;
    _int n;
    _int i;
    ptr<list<tuple<_int, _int>>> a;
    _int j;
    t = tuple(1LL, 2LL);
    n = 0LL;
    for (_int i = 0; i < 10000LL; ++i) {
        a = ptr(new list<tuple<_int, _int>>());
        a->append(tuple(i, 5LL));
        for (_int j = 0; j < 100LL; ++j) {
            if (to_bool(((t == tuple(1LL, j))))) {
            }
            if (to_bool(((t == tuple(i, 2LL))))) {
            }
            if (to_bool(((a->__getitem__(0LL) == tuple(j, 5LL))))) {
                a->append(tuple(j, 6LL));
            }
        }
    }
}

ptr<list<_int>> comprehension_11() {
    ptr<list<_int>> __result_12 = ptr(new list<_int>());
    _int x;
    for (auto __iter_13 = iter(a); !__iter_13.done();) {
        x = next(__iter_13);
        if (to_bool(((x < j)))) {
            __result_12->append(x);
        }
    }
    return __result_12;
}

void list_comprehension() {
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int j;
    ptr<list<_int>> b;
    a = ptr(new list<_int>({1LL, 2LL, 4LL, 6LL, 8LL, 13LL, 17LL}));
    n = 0LL;
    for (_int i = 0; i < 100000LL; ++i) {
        for (_int j = 0; j < 20LL; ++j) {
            b = comprehension_11();
        }
    }
}

void multiple_assignment() {
    _int x;
    _int y;
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int xx;
    _int yy;
    x = 0LL;
    y = 1LL;
    a = ptr(new list<_int>({2LL, 3LL}));
    n = 0LL;
    for (_int i = 0; i < 1000000LL; ++i) {
        destructure(x, y) = tuple(y, x);
        destructure(a->__getitem__(0LL), a->__getitem__(1LL)) = tuple(a->__getitem__(1LL), a->__getitem__(0LL));
        destructure(xx, yy) = tuple(a->__getitem__(0LL), a->__getitem__(1LL));
    }
}

void list_for_reversed() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> aa;
    _int s;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append((ptr(new list<_int>({i})) * 12LL));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_14 = iter(a); !__iter_14.done();) {
            aa = next(__iter_14);
            for (auto __iter_15 = iter(reversed(aa)); !__iter_15.done();) {
                s = next(__iter_15);
            }
        }
    }
}

void sieve() {
    _int n;
    _int i;
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
    }
}

_int num_primes(_int n) {
    ptr<list<bool>> is_prime;
    _int i;
    _int j;
    _int count;
    bool b;
    is_prime = (ptr(new list<bool>({true})) * (n + 1LL));
    is_prime->__setitem__(0LL, false);
    for (_int i = 2LL; i < (n + 1LL); ++i) {
        if ((to_bool(is_prime->__getitem__(i)) && to_bool((((i * i) <= n))))) {
            j = (i * i);
            // While loop
            while (to_bool(((j <= n)))) {
                is_prime->__setitem__(j, false);
            }
        }
    }
    count = 0LL;
    for (auto __iter_16 = iter(is_prime); !__iter_16.done();) {
        b = next(__iter_16);
        if (to_bool(b)) {
        }
    }
    return count;
}

ptr<list<tuple<str, _int>>> comprehension_17() {
    ptr<list<tuple<str, _int>>> __result_18 = ptr(new list<tuple<str, _int>>());
    _int i;
    for (_int i = 0; i < 20LL; ++i) {
        __result_18->append(tuple(to_str(i), mod((i * 5LL), 11LL)));
    }
    return __result_18;
}

void sorted_with_key() {
    _int n;
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> aa;
    _int j;
    ptr<list<tuple<str, _int>>> a2;
    _int c;
    ptr<list<_int>> seq;
    ptr<list<tuple<str, _int>>> a3;
    n = 10LL;
    a = ptr(new list<ptr<list<_int>>>());
    for (_int i = 0; i < n; ++i) {
        aa = ptr(new list<_int>());
        for (_int j = 0; j < i; ++j) {
            aa->append(mod((j * 971LL), 11LL));
        }
        a->append(aa);
    }
    a2 = comprehension_17();
    c = 0LL;
    for (_int i = 0; i < 20000LL; ++i) {
        for (auto __iter_19 = iter(a); !__iter_19.done();) {
            seq = next(__iter_19);
                return (-x);
        }
        a3 = _sorted_kwargs(false, a2);
            return x.get<0>();
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        multiple_assignment(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    