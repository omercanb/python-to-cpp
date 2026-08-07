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
ptr<list<_int>> __list_comprehension_34(ptr<list<ptr<list<_int>>>> a);
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
ptr<list<tuple<str, _int>>> __list_comprehension_35();
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
    _int __stop_714 = 1000LL;
    for (i = 0; i < __stop_714; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    _int __stop_715 = 100LL;
    for (i = 0; i < __stop_715; ++i) {
        for (auto __iter_204 = iter(a); !__iter_204.done();) {
            s = next(__iter_204);
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
    _int __stop_716 = 100LL;
    for (j = 0; j < __stop_716; ++j) {
        _int __stop_717 = 10LL;
        for (i = 0; i < __stop_717; ++i) {
            a->append(ptr(new list<_int>({(i * 2LL)})));
            a->append(ptr(new list<_int>({i, (i + 2LL)})));
            a->append(ptr(new list<_int>({i})));
            a->append(ptr(new list<_int>()));
        }
    }
    n = 0LL;
    _int __stop_718 = 1000LL;
    for (i = 0; i < __stop_718; ++i) {
        for (auto __iter_205 = iter(a); !__iter_205.done();) {
            s = next(__iter_205);
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
    _int __stop_719 = 100LL;
    for (j = 0; j < __stop_719; ++j) {
        _int __stop_720 = 10LL;
        for (i = 0; i < __stop_720; ++i) {
            a->append(tuple((i * 2LL), 2LL));
            a->append(tuple(i, (i + 2LL)));
            a->append(tuple(i, 2LL));
            a->append(tuple(2LL, 2LL));
        }
    }
    n = 0LL;
    _int __stop_721 = 1000LL;
    for (i = 0; i < __stop_721; ++i) {
        for (auto __iter_206 = iter(a); !__iter_206.done();) {
            s = next(__iter_206);
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
    _int __stop_722 = (200LL * 1000LL);
    for (i = 0; i < __stop_722; ++i) {
        a = ptr(new list<_int>());
        _int __stop_723 = mod(i, 10LL);
        for (j = 0; j < __stop_723; ++j) {
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
    _int __stop_724 = 2000LL;
    for (i = 0; i < __stop_724; ++i) {
        a = ptr(new list<_int>());
        _int __stop_725 = i;
        for (j = 0; j < __stop_725; ++j) {
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
    _int __stop_726 = 100LL;
    for (j = 0; j < __stop_726; ++j) {
        _int __stop_727 = 23LL;
        for (i = 0; i < __stop_727; ++i) {
            a->append(mod((i * 7LL), 9LL));
        }
    }
    n = 0LL;
    _int __stop_728 = 1000LL;
    for (i = 0; i < __stop_728; ++i) {
        for (auto __iter_207 = iter(a); !__iter_207.done();) {
            j = next(__iter_207);
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
    _int __stop_729 = 100LL;
    for (i = 0; i < __stop_729; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i})));
        a->append(ptr(new list<_int>()));
    }
    _int __stop_730 = 1000LL;
    for (i = 0; i < __stop_730; ++i) {
        for (auto __iter_208 = iter(a); !__iter_208.done();) {
            s = next(__iter_208);
            s2 = s->copy();
            s3 = s->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt));
            if (!(to_bool(((s2 == s3))))) throw AssertionError("");
        }
    }
}

ptr<list<_int>> __list_comprehension_34(ptr<list<ptr<list<_int>>>> a) {
    ptr<list<_int>> __tmp_34;
    ptr<list<_int>> s;
    __tmp_34 = ptr(new list<_int>());
    for (auto __iter_209 = iter(a); !__iter_209.done();) {
        s = next(__iter_209);
        __tmp_34->append(len(s));
    }
    return __tmp_34;
}

void list_remove() {
    _int j;
    ptr<list<ptr<list<_int>>>> a;
    _int i;
    ptr<list<_int>> s;
    _int total;
    _int __stop_731 = (10LL * 1000LL);
    for (j = 0; j < __stop_731; ++j) {
        a = ptr(new list<ptr<list<_int>>>());
        _int __stop_732 = 10LL;
        for (i = 0; i < __stop_732; ++i) {
            a->append(ptr(new list<_int>(range((11LL + i)))));
        }
        _int __stop_733 = 10LL;
        for (i = 0; i < __stop_733; ++i) {
            for (auto __iter_210 = iter(a); !__iter_210.done();) {
                s = next(__iter_210);
                s->remove(i);
            }
        }
        total = sum(__list_comprehension_34(a));
        if (!(to_bool(((total == 55LL))))) throw AssertionError(to_str(total));
    }
}

void list_insert() {
    _int j;
    ptr<list<_int>> a;
    _int i;
    _int __stop_734 = (10LL * 1000LL);
    for (j = 0; j < __stop_734; ++j) {
        a = ptr(new list<_int>());
        _int __stop_735 = 10LL;
        for (i = 0; i < __stop_735; ++i) {
            a->insert(0LL, i);
        }
        _int __stop_736 = 5LL;
        for (i = 0; i < __stop_736; ++i) {
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
    _int __stop_737 = 100LL;
    for (i = 0; i < __stop_737; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL), 44LL})));
        a->append(ptr(new list<_int>({44LL, i, (i + 2LL)})));
        a->append(ptr(new list<_int>({i, 44LL})));
        a->append(ptr(new list<_int>({44LL})));
    }
    n = 0LL;
    _int __stop_738 = 1000LL;
    for (i = 0; i < __stop_738; ++i) {
        for (auto __iter_211 = iter(a); !__iter_211.done();) {
            s = next(__iter_211);
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
    _int __stop_739 = (100LL * 1000LL);
    for (i = 0; i < __stop_739; ++i) {
        a = ptr(new list<_int>());
        n = a;
        l = (5LL + mod(i, 10LL));
        _int __stop_740 = l;
        for (j = 0; j < __stop_740; ++j) {
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
    _int __stop_741 = (1000LL * 1000LL);
    for (i = 0; i < __stop_741; ++i) {
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
    _int __stop_742 = 10000LL;
    for (i = 0; i < __stop_742; ++i) {
        _int __stop_743 = 100LL;
        for (j = 0; j < __stop_743; ++j) {
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
    _int __stop_744 = 10000LL;
    for (i = 0; i < __stop_744; ++i) {
        a = ptr(new list<tuple<_int, _int>>());
        a->append(tuple(i, 5LL));
        _int __stop_745 = 100LL;
        for (j = 0; j < __stop_745; ++j) {
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
    _int __stop_746 = 1000000LL;
    for (i = 0; i < __stop_746; ++i) {
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
    _int __stop_747 = 1000LL;
    for (i = 0; i < __stop_747; ++i) {
        a->append(ptr(new list<_int>({(i * 2LL)})));
        a->append(ptr(new list<_int>({i, (i + 2LL)})));
        a->append((ptr(new list<_int>({i})) * 12LL));
        a->append(ptr(new list<_int>()));
    }
    n = 0LL;
    _int __stop_748 = 100LL;
    for (i = 0; i < __stop_748; ++i) {
        for (auto __iter_212 = iter(a); !__iter_212.done();) {
            aa = next(__iter_212);
            for (auto __iter_213 = iter(reversed(aa)); !__iter_213.done();) {
                s = next(__iter_213);
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
    _int __stop_749 = 1000LL;
    for (i = 0; i < __stop_749; ++i) {
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
    _int __stop_750 = (n + 1LL);
    for (i = 2LL; i < __stop_750; ++i) {
        if ((to_bool(is_prime->__getitem__(i)) && to_bool((((i * i) <= n))))) {
            j = (i * i);
            while (to_bool(((j <= n)))) {
                is_prime->__setitem__(j, false);
                j += i;
            }
        }
    }
    count = 0LL;
    for (auto __iter_214 = iter(is_prime); !__iter_214.done();) {
        b = next(__iter_214);
        if (to_bool(b)) {
            count += 1LL;
        }
    }
    return count;
}

ptr<list<tuple<str, _int>>> __list_comprehension_35() {
    ptr<list<tuple<str, _int>>> __tmp_35;
    _int i;
    __tmp_35 = ptr(new list<tuple<str, _int>>());
    _int __stop_751 = 20LL;
    for (i = 0; i < __stop_751; ++i) {
        __tmp_35->append(tuple(to_str(i), mod((i * 5LL), 11LL)));
    }
    return __tmp_35;
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
    _int __stop_752 = n;
    for (i = 0; i < __stop_752; ++i) {
        aa = ptr(new list<_int>());
        _int __stop_753 = i;
        for (j = 0; j < __stop_753; ++j) {
            aa->append(mod((j * 971LL), 11LL));
        }
        a->append(aa);
    }
    _int __stop_754 = n;
    for (i = 0; i < __stop_754; ++i) {
        print(i);
    }
    a2 = __list_comprehension_35();
    c = 0LL;
    _int __stop_755 = 20000LL;
    for (i = 0; i < __stop_755; ++i) {
        for (auto __iter_215 = iter(a); !__iter_215.done();) {
            seq = next(__iter_215);
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
    