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
void str_methods() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    str("Use a mix of popular str methods (but not split/join).");
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_1 = iter(a); !__iter_1.done();) {
            s = next(__iter_1);
            if (to_bool(s.startswith(str("foo")))) {
            }
            if (to_bool(s.endswith(str("r")))) {
            }
            if (to_bool(((s.replace(str("-"), str("/")) != s)))) {
            }
            if (to_bool(((s.strip() != s)))) {
            }
            if (to_bool(((s.rstrip() != s)))) {
            }
            if (to_bool(((s.lower() == s)))) {
            }
        }
    }
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
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("FOOBAR-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("  "), str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_2 = iter(a); !__iter_2.done();) {
            s = next(__iter_2);
            if (to_bool(s.startswith(tuple(str("  1"), str("  2"), str("  3"))))) {
            }
            if (to_bool(s.endswith(tuple(str("4"), str("5"), str("6"))))) {
            }
            if (to_bool(((s.lstrip() != s)))) {
            }
            if (to_bool(((s.lstrip(str(" ")) != s)))) {
            }
            if (to_bool(((s.rstrip(str("123")) != s)))) {
            }
            if (to_bool(((s.upper() == s)))) {
            }
            destructure(x, y, z) = s.partition(str("-"));
            if (to_bool(y)) {
            }
            destructure(x, y, z) = s.rpartition(str("-"));
            if (to_bool(y)) {
            }
        }
    }
}

void str_format() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    str ss;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_3 = iter(a); !__iter_3.done();) {
            s = next(__iter_3);
            ss = str("").join(ptr(new list<str>({str("foobar "), str("{:{}}").format(s, str("")), str(" stuff")})));
        }
    }
}

void str_slicing() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str(" str")}))));
    }
    n = 0LL;
    for (_int i = 0; i < 1000LL; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            s = next(__iter_4);
            if (to_bool(((s.__getitem__(slice(std::nullopt, 3LL, std::nullopt)) == str("Foo"))))) {
            }
            if (to_bool(((s.__getitem__(slice((-2LL), std::nullopt, std::nullopt)) == str("00"))))) {
            }
        }
    }
}

void split_and_join() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    ptr<list<str>> items;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_5 = iter(a); !__iter_5.done();) {
            s = next(__iter_5);
            items = s.split(str("-"));
            if (to_bool(((str("-").join(items) == s)))) {
            }
        }
    }
}

void encode_decode() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    ptr<bytes> b;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_6 = iter(a); !__iter_6.done();) {
            s = next(__iter_6);
            b = s.encode(str("ascii"));
            if (to_bool(((b->decode(str("ascii")) != s)))) {
            }
            b = s.encode(str("utf8"));
            if (to_bool(((b->decode(str("utf8")) == s)))) {
            }
        }
    }
}

void str_searching() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    for (_int i = 0; i < 100LL; ++i) {
        for (auto __iter_7 = iter(a); !__iter_7.done();) {
            s = next(__iter_7);
            if (to_bool((s.__contains__(str("i"))))) {
            }
            if (to_bool(((s.find(str("asd")) >= 0LL)))) {
            }
        }
    }
}

void str_call() {
    ptr<list<ptr<Cls>>> a;
    _int i;
    _int n;
    ptr<Cls> obj;
    str s1;
    str s2;
    a = ptr(new list<ptr<Cls>>());
    for (_int i = 0; i < 100LL; ++i) {
        a->append(ptr(new Cls(i)));
    }
    n = 0LL;
    for (_int i = 0; i < (10LL * 1000LL); ++i) {
        for (auto __iter_8 = iter(a); !__iter_8.done();) {
            obj = next(__iter_8);
            s1 = to_str(obj);
            s2 = to_str(s1);
        }
    }
}

class Cls {
  public:
    _int x;

    Cls(_int x) { __init__(x); }

    void __init__(_int x) {
        this->x = x;
    }

    str __str__() {
        return to_str(this->x);
    }

};

void ord_builtin() {
    ptr<list<str>> a;
    _int i;
    _int n;
    str s;
    _int j;
    a = ptr(new list<str>());
    for (_int i = 0; i < 1000LL; ++i) {
        a->append(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(i, str(""))}))));
        a->append(str("").join(ptr(new list<str>({str("{:{}}").format(i, str("")), str("-ab-asdfsdf-asdf")}))));
        a->append(str("yeah"));
    }
    n = 0LL;
    for (_int i = 0; i < 50LL; ++i) {
        for (auto __iter_9 = iter(a); !__iter_9.done();) {
            s = next(__iter_9);
            for (size_t j = 0; j < len(s); ++j) {
                if (to_bool(((97LL <= ord(s.__getitem__(j))) && (ord(s.__getitem__(j)) <= 122LL)))) {
                }
                if (to_bool(is_upper_case_letter(s.__getitem__(j)))) {
                }
                if (to_bool(((s.__getitem__(j) == str("a"))))) {
                }
            }
        }
    }
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
    