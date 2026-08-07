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
void dict_iteration();
void dict_to_list();
void dict_set_default();
void dict_clear();
void dict_copy();
ptr<list<tuple<str, str>>> __list_comprehension_0(ptr<list<tuple<str, str>>> s);
void dict_call_generator();
void dict_del_item();
void __init_module__();

void __init_module__() {
}

void dict_iteration() {
    ptr<list<ptr<dict<str, _int>>>> a;
    _int j;
    ptr<dict<str, _int>> d;
    _int i;
    _int n;
    str k;
    _int v;
    a = ptr(new list<ptr<dict<str, _int>>>());
    _int __stop_0 = 1000LL;
    for (j = 0; j < __stop_0; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_1 = mod(j, 10LL);
        for (i = 0; i < __stop_1; ++i) {
            d->__setitem__(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(j, str(""))}))), j);
            d->__setitem__(str("").join(ptr(new list<str>({str("{:{}}").format(j, str("")), str(" str")}))), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_2 = 1000LL;
    for (i = 0; i < __stop_2; ++i) {
        for (auto __iter_0 = iter(a); !__iter_0.done();) {
            d = next(__iter_0);
            for (auto __iter_1 = iter(d); !__iter_1.done();) {
                k = next(__iter_1);
                if (to_bool(((k == str("0 str"))))) {
                    n += 1LL;
                }
            }
            for (auto __iter_2 = iter(d->keys()); !__iter_2.done();) {
                k = next(__iter_2);
                if (to_bool(((k == str("0 str"))))) {
                    n += 1LL;
                }
            }
            for (auto __iter_3 = iter(d->values()); !__iter_3.done();) {
                v = next(__iter_3);
                if (to_bool(((v == 0LL)))) {
                    n += 1LL;
                }
            }
            for (auto __iter_4 = iter(d->items()); !__iter_4.done();) {
                destructure(k, v) = next(__iter_4);
                if ((to_bool(((v == 1LL))) || to_bool(((k == str("1 str")))))) {
                    n += 1LL;
                }
            }
        }
    }
    if (!(to_bool(((n == 202000LL))))) throw AssertionError(to_str(n));
}

void dict_to_list() {
    ptr<list<ptr<dict<str, _int>>>> a;
    _int j;
    ptr<dict<str, _int>> d;
    _int i;
    _int n;
    a = ptr(new list<ptr<dict<str, _int>>>());
    _int __stop_3 = 1000LL;
    for (j = 0; j < __stop_3; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_4 = mod(j, 10LL);
        for (i = 0; i < __stop_4; ++i) {
            d->__setitem__(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(j, str(""))}))), j);
            d->__setitem__(str("").join(ptr(new list<str>({str("{:{}}").format(j, str("")), str(" str")}))), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_5 = 1000LL;
    for (i = 0; i < __stop_5; ++i) {
        for (auto __iter_5 = iter(a); !__iter_5.done();) {
            d = next(__iter_5);
            (n + (+len(ptr(new list<str>(d)))));
            n += len(ptr(new list<str>(d->keys())));
            n += len(ptr(new list<_int>(d->values())));
            n += len(ptr(new list<tuple<str, _int>>(d->items())));
        }
    }
    if (!(to_bool(((n == 5400000LL))))) throw AssertionError(to_str(n));
}

void dict_set_default() {
    _int n;
    _int i;
    ptr<dict<_int, ptr<list<_int>>>> d;
    _int j;
    _int k;
    n = 0LL;
    _int __stop_6 = (100LL * 1000LL);
    for (i = 0; i < __stop_6; ++i) {
        d = ptr(new dict<_int, ptr<list<_int>>>());
        _int __stop_7 = mod(i, 10LL);
        for (j = 0; j < __stop_7; ++j) {
            _int __stop_8 = mod(i, 11LL);
            for (k = 0; k < __stop_8; ++k) {
                d->setdefault(j, ptr(new list<_int>()))->append(k);
            }
        }
        n += len(d);
    }
    if (!(to_bool(((n == 409095LL))))) throw AssertionError(to_str(n));
}

void dict_clear() {
    _int n;
    _int i;
    ptr<dict<_int, str>> d;
    _int j;
    n = 0LL;
    _int __stop_9 = (1000LL * 1000LL);
    for (i = 0; i < __stop_9; ++i) {
        d = ptr(new dict<_int, str>());
        _int __stop_10 = mod(i, 4LL);
        for (j = 0; j < __stop_10; ++j) {
            d->__setitem__(j, str("x"));
        }
        d->clear();
        if (!(to_bool(((len(d) == 0LL))))) throw AssertionError("");
    }
}

void dict_copy() {
    ptr<list<ptr<dict<str, _int>>>> a;
    _int j;
    ptr<dict<str, _int>> d;
    _int i;
    _int n;
    ptr<dict<str, _int>> d2;
    ptr<dict<str, _int>> d3;
    ptr<dict<str, _int>> d4;
    a = ptr(new list<ptr<dict<str, _int>>>());
    _int __stop_11 = 100LL;
    for (j = 0; j < __stop_11; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_12 = mod(j, 10LL);
        for (i = 0; i < __stop_12; ++i) {
            d->__setitem__(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(j, str(""))}))), j);
            d->__setitem__(str("").join(ptr(new list<str>({str("{:{}}").format(j, str("")), str(" str")}))), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_13 = (10LL * 1000LL);
    for (i = 0; i < __stop_13; ++i) {
        for (auto __iter_6 = iter(a); !__iter_6.done();) {
            d = next(__iter_6);
            d2 = d->copy();
            d3 = d2->copy();
            d4 = d3->copy();
            if (!(to_bool(((len(d4) == len(d)))))) throw AssertionError("");
        }
    }
}

ptr<list<tuple<str, str>>> __list_comprehension_0(ptr<list<tuple<str, str>>> s) {
    ptr<list<tuple<str, str>>> __tmp_0;
    str key;
    str value;
    __tmp_0 = ptr(new list<tuple<str, str>>());
    for (auto __iter_7 = iter(s); !__iter_7.done();) {
        destructure(key, value) = next(__iter_7);
        __tmp_0->append(tuple(key, value));
    }
    return __tmp_0;
}

void dict_call_generator() {
    ptr<list<ptr<list<tuple<str, str>>>>> a;
    _int j;
    ptr<list<tuple<str, str>>> items;
    _int n;
    _int i;
    ptr<list<tuple<str, str>>> s;
    ptr<dict<str, str>> d;
    a = ptr(new list<ptr<list<tuple<str, str>>>>());
    _int __stop_14 = 1000LL;
    for (j = 0; j < __stop_14; ++j) {
        items = ptr(new list<tuple<str, str>>({tuple(str("").join(ptr(new list<str>({str("Foobar-"), str("{:{}}").format(j, str(""))}))), to_str(j)), tuple(str("").join(ptr(new list<str>({str("{:{}}").format(j, str("")), str(" str")}))), str("x"))}));
        if (to_bool(((mod(j, 2LL) == 0LL)))) {
            items->append(tuple(str("blah"), str("bar")));
        }
        a->append(items);
    }
    n = 0LL;
    _int __stop_15 = 1000LL;
    for (i = 0; i < __stop_15; ++i) {
        for (auto __iter_8 = iter(a); !__iter_8.done();) {
            s = next(__iter_8);
            d = ptr(new dict<str, str>(__list_comprehension_0(s)));
            if (!(to_bool(((len(d) == len(s)))))) throw AssertionError("");
        }
    }
}

void dict_del_item() {
    ptr<dict<str, str>> d;
    _int j;
    d = ptr(new dict<str, str>({{str("long_lived"), str("value")}}));
    _int __stop_16 = (1000LL * 1000LL);
    for (j = 0; j < __stop_16; ++j) {
        d->__setitem__(str("xyz"), str("asdf"));
        d->__setitem__(str("asdf"), str("lulz"));
        d->__setitem__(str("foobar"), str("baz zar"));
    }
}


    int main() {
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        dict_del_item(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    