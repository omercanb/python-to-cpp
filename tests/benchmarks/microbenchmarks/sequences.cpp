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
void list_slicing();
void in_list();
void in_tuple();
void list_append_small();
void list_append_large();
void list_from_range();
void list_copy();
ptr<list<_int>> __list_comprehension_0(ptr<list<ptr<list<_int>>>> a);
void list_remove();
void list_insert();
void list_index();
void list_add_in_place();
void list_concatenate();
void list_equality();
void tuple_equality();
void multiple_assignment();
void list_for_reversed();
void sieve();
_int num_primes(_int n);
ptr<list<tuple<str, _int>>> __list_comprehension_1();
void sorted_with_key();
void __init_module__();

void __init_module__() {
}

void list_slicing() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_0 = 1000LL;
    for (i = 0; i < __stop_0; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    _int __stop_1 = 100LL;
    for (i = 0; i < __stop_1; ++i) {
        for (auto __iter_0 = iter(a); !__iter_0.done();) {
            s = next(__iter_0);
            n += len(s->__getitem__(slice(2LL, (-2LL), std::nullopt)));
            if (to_bool(((len(s->__getitem__(slice(std::nullopt, 2LL, std::nullopt))) < 2LL)))) {
                n += 1LL;
            }
            if (to_bool(((s->__getitem__(slice((-2LL), std::nullopt, std::nullopt)) == ptr(new list<_int>({0LL})))))) {
                n += 1LL;
            }
            if (to_bool(((s == s->__getitem__(slice(std::nullopt, std::nullopt, (-1LL))))))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 600200LL))))) throw AssertionError(to_str(n));
}

void in_list() {
    ptr<list<ptr<list<_int>>>> a;
    _int j;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_2 = 100LL;
    for (j = 0; j < __stop_2; ++j) {
        _int __stop_3 = 10LL;
        for (i = 0; i < __stop_3; ++i) {
            a->append(ptr(new list<_int>({(i * 2LL)})));
            a->append(ptr(new list<_int>({i, (i + 2LL)})));
            a->append(ptr(new list<_int>({i})));
            a->append(ptr(new list<_int>()));
        }
    }
    n = 0LL;
    _int __stop_4 = 1000LL;
    for (i = 0; i < __stop_4; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            s = next(__iter_1);
            if (to_bool((s->__contains__(6LL)))) {
                n += 1LL;
            }
            if (to_bool((ptr(new list<_int>({3LL, 4LL, 5LL}))->__contains__(i)))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 412000LL))))) throw AssertionError(to_str(n));
}

void in_tuple() {
    ptr<list<tuple<_int, _int>>> a;
    _int j;
    _int i;
    _int n;
    tuple<_int, _int> s;
    a = ptr(new list<tuple<_int, _int>>());
    _int __stop_5 = 100LL;
    for (j = 0; j < __stop_5; ++j) {
        _int __stop_6 = 10LL;
        for (i = 0; i < __stop_6; ++i) {
            a->append(tuple((i * 2LL), 2LL));
            a->append(tuple(i, (i + 2LL)));
            a->append(tuple(i, 2LL));
            a->append(tuple(2LL, 2LL));
        }
    }
    n = 0LL;
    _int __stop_7 = 1000LL;
    for (i = 0; i < __stop_7; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            s = next(__iter_2);
            if (to_bool((s.__contains__(6LL)))) {
                n += 1LL;
            }
            if (to_bool((tuple(3LL, 4LL, 5LL).__contains__(i)))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 412000LL))))) throw AssertionError(to_str(n));
}

void list_append_small() {
    _int n;
    _int i;
    ptr<list<_int>> a;
    _int j;
    n = 0LL;
    _int __stop_8 = (200LL * 1000LL);
    for (i = 0; i < __stop_8; ++i) {
        a = ptr(new list<_int>());
        _int __stop_9 = mod(i, 10LL);
        for (j = 0; j < __stop_9; ++j) {
            a->append((j + i));
        }
        n += len(a);
    }
    if (!(to_bool(((n == 900000LL))))) throw AssertionError(to_str(n));
}

void list_append_large() {
    _int n;
    _int i;
    ptr<list<_int>> a;
    _int j;
    n = 0LL;
    _int __stop_10 = 2000LL;
    for (i = 0; i < __stop_10; ++i) {
        a = ptr(new list<_int>());
        _int __stop_11 = i;
        for (j = 0; j < __stop_11; ++j) {
            a->append((j + i));
        }
        n += len(a);
    }
    if (!(to_bool(((n == 1999000LL))))) throw AssertionError(to_str(n));
}

void list_from_range() {
    ptr<list<_int>> a;
    _int j;
    _int i;
    _int n;
    ptr<list<_int>> lst;
    a = ptr(new list<_int>());
    _int __stop_12 = 100LL;
    for (j = 0; j < __stop_12; ++j) {
        _int __stop_13 = 23LL;
        for (i = 0; i < __stop_13; ++i) {
            a->append(mod((i * 7LL), 9LL));
        }
    }
    n = 0LL;
    _int __stop_14 = 1000LL;
    for (i = 0; i < __stop_14; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            j = next(__iter_3);
            lst = ptr(new list<_int>(range(j)));
            n += len(lst);
        }
    }
    if (!(to_bool(((n == 8800000LL))))) throw AssertionError(to_str(n));
}

void list_copy() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> s;
    ptr<list<_int>> s2;
    ptr<list<_int>> s3;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_15 = 100LL;
    for (i = 0; i < __stop_15; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    _int __stop_16 = 1000LL;
    for (i = 0; i < __stop_16; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            s = next(__iter_4);
            s2 = s->copy();
            s3 = s->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt));
            if (!(to_bool(((s2 == s3))))) throw AssertionError("");
        }
    }
}

ptr<list<_int>> __list_comprehension_0(ptr<list<ptr<list<_int>>>> a) {
    ptr<list<_int>> __tmp_0;
    ptr<list<_int>> s;
    __tmp_0 = ptr(new list<_int>());
    for (auto __iter_5 = iter(a); !__iter_5.done();) {
        s = next(__iter_5);
        __tmp_0->append(len(s));
    }
    return __tmp_0;
}

void list_remove() {
    _int j;
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> s;
    _int total;
    _int __stop_17 = (10LL * 1000LL);
    for (j = 0; j < __stop_17; ++j) {
        a = ptr(new list<ptr<list<_int>>>());
        _int __stop_18 = 10LL;
        for (i = 0; i < __stop_18; ++i) {
            a->append(ptr(new list<_int>(range((11LL + i)))));
        }
        _int __stop_19 = 10LL;
        for (i = 0; i < __stop_19; ++i) {
            for (auto __iter_6 = iter(a); !__iter_6.done();) {
                s = next(__iter_6);
                s->remove(i);
            }
        }
        total = sum(__list_comprehension_0(a));
        if (!(to_bool(((total == 55LL))))) throw AssertionError(to_str(total));
    }
}

void list_insert() {
    _int j;
    ptr<list<_int>> a;
    _int i;
    _int __stop_20 = (10LL * 1000LL);
    for (j = 0; j < __stop_20; ++j) {
        a = ptr(new list<_int>());
        _int __stop_21 = 10LL;
        for (i = 0; i < __stop_21; ++i) {
            a->insert(0LL, i);
        }
        _int __stop_22 = 5LL;
        for (i = 0; i < __stop_22; ++i) {
            a->insert(5LL, i);
        }
        if (!(to_bool(((len(a) == 15LL))))) throw AssertionError("");
    }
}

void list_index() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> s;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_23 = 100LL;
    for (i = 0; i < __stop_23; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL), 44LL})));
        a->append(ptr(new list<_int>({44LL, i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i, 44LL})));
        a->append(ptr(new list<_int>({44LL})));
    }
    n = 0LL;
    _int __stop_24 = 1000LL;
    for (i = 0; i < __stop_24; ++i) {
        for (auto __iter_7 = iter(a); !__iter_7.done();) {
            s = next(__iter_7);
            n += s->index(44LL);
        }
    }
    if (!(to_bool(((n == 198000LL))))) throw AssertionError(to_str(n));
}

void list_add_in_place() {
    _int i;
    ptr<list<_int>> a;
    ptr<list<_int>> n;
    _int l;
    _int j;
    _int __stop_25 = (100LL * 1000LL);
    for (i = 0; i < __stop_25; ++i) {
        a = ptr(new list<_int>());
        n = a;
        l = (5LL + mod(i, 10LL));
        _int __stop_26 = l;
        for (j = 0; j < __stop_26; ++j) {
            a += ptr(new list<_int>({j}));
        }
        if (!(to_bool(((len(a) == l))))) throw AssertionError("");
        if (!(to_bool(((a == n))))) throw AssertionError("");
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
    _int __stop_27 = (1000LL * 1000LL);
    for (i = 0; i < __stop_27; ++i) {
        a = x;
        if (to_bool(flag)) {
            b = (a + a);
        } else {
            b = ((y + a) + y);
        }
        n += len((a + b));
        flag = (!to_bool(flag));
    }
    if (!(to_bool(((n == 8500000LL))))) throw AssertionError(to_str(n));
}

void list_equality() {
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int j;
    a = ptr(new list<_int>({1LL, 2LL}));
    n = 0LL;
    _int __stop_28 = 10000LL;
    for (i = 0; i < __stop_28; ++i) {
        _int __stop_29 = 100LL;
        for (j = 0; j < __stop_29; ++j) {
            if (to_bool(((a == ptr(new list<_int>({1LL, j})))))) {
                n += 1LL;
            }
            if (to_bool(((a == ptr(new list<_int>({i, 2LL})))))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 10100LL))))) throw AssertionError(to_str(n));
}

void tuple_equality() {
    tuple<_int, _int> t;
    _int n;
    _int i;
    ptr<list<tuple<_int, _int>>> a;
    _int j;
    t = tuple(1LL, 2LL);
    n = 0LL;
    _int __stop_30 = 10000LL;
    for (i = 0; i < __stop_30; ++i) {
        a = ptr(new list<tuple<_int, _int>>());
        a->append(tuple(i, 5LL));
        _int __stop_31 = 100LL;
        for (j = 0; j < __stop_31; ++j) {
            if (to_bool(((t == tuple(1LL, j))))) {
                n += 1LL;
            }
            if (to_bool(((t == tuple(i, 2LL))))) {
                n += 1LL;
            }
            if (to_bool(((a->__getitem__(0LL) == tuple(j, 5LL))))) {
                a->append(tuple(j, 6LL));
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 10200LL))))) throw AssertionError(to_str(n));
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
    _int __stop_32 = 1000000LL;
    for (i = 0; i < __stop_32; ++i) {
        destructure(x, y) = tuple(y, x);
        destructure(a->__getitem__(0LL), a->__getitem__(1LL)) = tuple(a->__getitem__(1LL), a->__getitem__(0LL));
        destructure(xx, yy) = tuple(a->__getitem__(0LL), a->__getitem__(1LL));
        n += (x + xx);
    }
    if (!(to_bool(((n == 3000000LL))))) throw AssertionError(to_str(n));
}

void list_for_reversed() {
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    _int n;
    ptr<list<_int>> aa;
    _int s;
    a = ptr(new list<ptr<list<_int>>>());
    _int __stop_33 = 1000LL;
    for (i = 0; i < __stop_33; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append((ptr(new list<_int>({i})) * 12LL));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    _int __stop_34 = 100LL;
    for (i = 0; i < __stop_34; ++i) {
        for (auto __iter_8 = iter(a); !__iter_8.done();) {
            aa = next(__iter_8);
            for (auto __iter_9 = iter(reversed(aa)); !__iter_9.done();) {
                s = next(__iter_9);
                n += s;
            }
        }
    }
    if (!(to_bool(((n == 799400000LL))))) throw AssertionError(to_str(n));
}

void sieve() {
    _int n;
    _int i;
    n = 0LL;
    _int __stop_35 = 1000LL;
    for (i = 0; i < __stop_35; ++i) {
        n += num_primes(1000LL);
    }
    if (!(to_bool(((n == 168000LL))))) throw AssertionError(to_str(n));
}

_int num_primes(_int n) {
    ptr<list<bool>> is_prime;
    _int i;
    _int j;
    _int count;
    bool b;
    is_prime = (ptr(new list<bool>({true})) * (n + 1LL));
    is_prime->__setitem__(0LL, false);
    is_prime->__setitem__(1LL, false);
    _int __stop_36 = (n + 1LL);
    for (i = 2LL; i < __stop_36; ++i) {
        if ((to_bool(is_prime->__getitem__(i)) && to_bool((((i * i) <= n))))) {
            j = (i * i);
            while (to_bool(((j <= n)))) {
                is_prime->__setitem__(j, false);
                j += i;
            }
        }
    }
    count = 0LL;
    for (auto __iter_10 = iter(is_prime); !__iter_10.done();) {
        b = next(__iter_10);
        if (to_bool(b)) {
            count += 1LL;
        }
    }
    return count;
}

ptr<list<tuple<str, _int>>> __list_comprehension_1() {
    ptr<list<tuple<str, _int>>> __tmp_1;
    _int i;
    __tmp_1 = ptr(new list<tuple<str, _int>>());
    _int __stop_37 = 20LL;
    for (i = 0; i < __stop_37; ++i) {
        __tmp_1->append(tuple(to_str(i), mod((i * 5LL), 11LL)));
    }
    return __tmp_1;
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
    _int __stop_38 = n;
    for (i = 0; i < __stop_38; ++i) {
        aa = ptr(new list<_int>());
        _int __stop_39 = i;
        for (j = 0; j < __stop_39; ++j) {
            aa->append(mod((j * 971LL), 11LL));
        }
        a->append(aa);
    }
    _int __stop_40 = n;
    for (i = 0; i < __stop_40; ++i) {
        print(i);
    }
    a2 = __list_comprehension_1();
    c = 0LL;
    _int __stop_41 = 20000LL;
    for (i = 0; i < __stop_41; ++i) {
        for (auto __iter_11 = iter(a); !__iter_11.done();) {
            seq = next(__iter_11);
            c += len(_sorted_kwargs(false, seq));
        }
        a3 = _sorted_kwargs(false, a2);
        c += len(_sorted_kwargs(false, a3));
    }
    if (!(to_bool(((c == 1300000LL))))) throw AssertionError(to_str(c));
}


    int main() {
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        sorted_with_key(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    