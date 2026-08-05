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
class Cls;

void str_methods();
void str_methods_2();
void str_format();
void str_slicing();
void split_and_join();
void str_searching();
void str_call();
void ord_builtin();
bool is_upper_case_letter(str ch);

class Cls {
  public:
    _int x;

    Cls(_int x) { __init__(x); }

    void __init__(_int x);
    str __str__();
};

void Cls::__init__(_int x) {
    this->x = x;
}

str Cls::__str__() {
    return to_str(this->x);
}

void str_methods() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    str("Use a mix of popular str methods (but not split/join).");
    a = ptr(new list<str>());
    _int __stop_1 = 1000LL;
    for (i = 0; i < __stop_1; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_2 = 100LL;
    for (i = 0; i < __stop_2; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            s = next(__iter_3);
            if (to_bool(s.startswith(str("foo")))) {
                n += 1LL;
            }
            if (to_bool(s.endswith(str("r")))) {
                n += 1LL;
            }
            if (to_bool(((s.replace(str("-"), str("/")) != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.strip() != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.rstrip() != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.lower() == s)))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 400000LL))))) throw AssertionError(to_str(n));
}

void str_methods_2() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    str x;
    str y;
    str z;
    str("Use a mix of popular str methods.");
    a = ptr(new list<str>());
    _int __stop_4 = 1000LL;
    for (i = 0; i < __stop_4; ++i) {
        a->append(str("").join(ptr(new list<str>({str("FOOBAR-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_5 = 100LL;
    for (i = 0; i < __stop_5; ++i) {
        for (auto __iter_6 = iter(a); !__iter_6.done();) {
            s = next(__iter_6);
            if (to_bool(s.startswith(str("  1")))) {
                n += 1LL;
            }
            if (to_bool(s.endswith(str("4")))) {
                n += 1LL;
            }
            if (to_bool(((s.lstrip() != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.lstrip(str(" ")) != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.rstrip(str("123")) != s)))) {
                n += 1LL;
            }
            if (to_bool(((s.upper() == s)))) {
                n += 1LL;
            }
            destructure(x, y, z) = s.partition(str("-"));
            if (to_bool(y)) {
                n += 1LL;
            }
            destructure(x, y, z) = s.rpartition(str("-"));
            if (to_bool(y)) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 551100LL))))) throw AssertionError(to_str(n));
}

void str_format() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    str ss;
    a = ptr(new list<str>());
    _int __stop_7 = 1000LL;
    for (i = 0; i < __stop_7; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_8 = 100LL;
    for (i = 0; i < __stop_8; ++i) {
        for (auto __iter_9 = iter(a); !__iter_9.done();) {
            s = next(__iter_9);
            n += len(str("foobar {} stuff").format(s));
            ss = str("").join(ptr(new list<str>({str("foobar "), str("{:{}}").format(s, str("")), str(" stuff")})));
            n += len(str("").join(ptr(new list<str>({str("{:{}}").format(s, str("")), str("-"), str("{:{}}").format(ss, str(""))}))));
        }
    }
    if (!(to_bool(((n == 10434000LL))))) throw AssertionError(to_str(n));
}

void str_slicing() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    a = ptr(new list<str>());
    _int __stop_10 = 1000LL;
    for (i = 0; i < __stop_10; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_11 = 1000LL;
    for (i = 0; i < __stop_11; ++i) {
        for (auto __iter_12 = iter(a); !__iter_12.done();) {
            s = next(__iter_12);
            n += len(s.__getitem__(slice(2LL, (-2LL), std::nullopt)));
            if (to_bool(((s.__getitem__(slice(std::nullopt, 3LL, std::nullopt)) == str("Foo"))))) {
                n += 1LL;
            }
            if (to_bool(((s.__getitem__(slice((-2LL), std::nullopt, std::nullopt)) == str("00"))))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 9789000LL))))) throw AssertionError(to_str(n));
}

void split_and_join() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    ptr<list<str>> items;
    a = ptr(new list<str>());
    _int __stop_13 = 1000LL;
    for (i = 0; i < __stop_13; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_14 = 100LL;
    for (i = 0; i < __stop_14; ++i) {
        for (auto __iter_15 = iter(a); !__iter_15.done();) {
            s = next(__iter_15);
            items = s.split(str("-"));
            if (to_bool(((str("-").join(items) == s)))) {
                n += 1LL;
            }
        }
    }
    if (!(to_bool(((n == 300000LL))))) throw AssertionError(to_str(n));
}

void str_searching() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    a = ptr(new list<str>());
    _int __stop_16 = 1000LL;
    for (i = 0; i < __stop_16; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_17 = 100LL;
    for (i = 0; i < __stop_17; ++i) {
        for (auto __iter_18 = iter(a); !__iter_18.done();) {
            s = next(__iter_18);
            if (to_bool((s.__contains__(str("i"))))) {
                n += 1LL;
            }
            if (to_bool(((s.find(str("asd")) >= 0LL)))) {
                n += 1LL;
            }
            n += s.index(str("a"));
        }
    }
    if (!(to_bool(((n == 1089000LL))))) throw AssertionError(to_str(n));
}

void str_call() {
    ptr<list<ptr<Cls>>> a;
    _int i;
    _int n;
    ptr<Cls> obj;
    str s1;
    str s2;
    a = ptr(new list<ptr<Cls>>());
    _int __stop_19 = 100LL;
    for (i = 0; i < __stop_19; ++i) {
        a->append(ptr(new Cls(i)));
    }
    n = 0LL;
    _int __stop_20 = (10LL * 1000LL);
    for (i = 0; i < __stop_20; ++i) {
        for (auto __iter_21 = iter(a); !__iter_21.done();) {
            obj = next(__iter_21);
            s1 = to_str(obj);
            s2 = to_str(s1);
            n += len(s2);
        }
    }
    if (!(to_bool(((n == 1900000LL))))) throw AssertionError(to_str(n));
}

void ord_builtin() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    _int j;
    a = ptr(new list<str>());
    _int __stop_22 = 1000LL;
    for (i = 0; i < __stop_22; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_23 = 50LL;
    for (i = 0; i < __stop_23; ++i) {
        for (auto __iter_24 = iter(a); !__iter_24.done();) {
            s = next(__iter_24);
            _int __len_25 = len(s);
            for (j = 0; j < __len_25; ++j) {
                if (to_bool(((97LL <= ord(s.__getitem__(j))) && (ord(s.__getitem__(j)) <= 122LL)))) {
                    n += 1LL;
                }
                if (to_bool(is_upper_case_letter(s.__getitem__(j)))) {
                    n += 2LL;
                }
                if (to_bool(((s.__getitem__(j) == str("a"))))) {
                    n += 3LL;
                }
            }
        }
    }
    if (!(to_bool(((n == 1950000LL))))) throw AssertionError(to_str(n));
}

bool is_upper_case_letter(str ch) {
    return ((65LL <= ord(ch)) && (ord(ch) <= 90LL));
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        ord_builtin(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    