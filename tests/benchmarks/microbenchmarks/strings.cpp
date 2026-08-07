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
void __init_module__();

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

void __init_module__() {
}

void str_methods() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    a = ptr(new list<str>());
    _int __stop_0 = 1000LL;
    for (i = 0; i < __stop_0; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_1 = 100LL;
    for (i = 0; i < __stop_1; ++i) {
        for (auto __iter_0 = iter(a); !__iter_0.done();) {
            s = next(__iter_0);
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
    a = ptr(new list<str>());
    _int __stop_2 = 1000LL;
    for (i = 0; i < __stop_2; ++i) {
        a->append(str("").join(ptr(new list<str>({str("FOOBAR-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_3 = 100LL;
    for (i = 0; i < __stop_3; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            s = next(__iter_1);
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
    _int __stop_4 = 1000LL;
    for (i = 0; i < __stop_4; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_5 = 100LL;
    for (i = 0; i < __stop_5; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            s = next(__iter_2);
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
    _int __stop_6 = 1000LL;
    for (i = 0; i < __stop_6; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    _int __stop_7 = 1000LL;
    for (i = 0; i < __stop_7; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            s = next(__iter_3);
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
    _int __stop_8 = 1000LL;
    for (i = 0; i < __stop_8; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_9 = 100LL;
    for (i = 0; i < __stop_9; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            s = next(__iter_4);
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
    _int __stop_10 = 1000LL;
    for (i = 0; i < __stop_10; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_11 = 100LL;
    for (i = 0; i < __stop_11; ++i) {
        for (auto __iter_5 = iter(a); !__iter_5.done();) {
            s = next(__iter_5);
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
    _int __stop_12 = 100LL;
    for (i = 0; i < __stop_12; ++i) {
        a->append(ptr(new Cls(i)));
    }
    n = 0LL;
    _int __stop_13 = (10LL * 1000LL);
    for (i = 0; i < __stop_13; ++i) {
        for (auto __iter_6 = iter(a); !__iter_6.done();) {
            obj = next(__iter_6);
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
    _int __stop_14 = 1000LL;
    for (i = 0; i < __stop_14; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    _int __stop_15 = 50LL;
    for (i = 0; i < __stop_15; ++i) {
        for (auto __iter_7 = iter(a); !__iter_7.done();) {
            s = next(__iter_7);
            _int __len_0 = len(s);
            for (j = 0; j < __len_0; ++j) {
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
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        ord_builtin(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    