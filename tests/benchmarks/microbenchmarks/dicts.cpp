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
ptr<list<tuple<str, str>>> __list_comprehension_42(ptr<list<tuple<str, str>>> s);
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
    _int __stop_943 = 1000LL;
    for (j = 0; j < __stop_943; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_944 = mod(j, 10LL);
        for (i = 0; i < __stop_944; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_945 = 1000LL;
    for (i = 0; i < __stop_945; ++i) {
        for (auto __iter_320 = iter(a); !__iter_320.done();) {
            d = next(__iter_320);
            for (auto __iter_321 = iter(d); !__iter_321.done();) {
                k = next(__iter_321);
                if (to_bool(((k == str("0 str"))))) {
                    n += 1LL;
                }
            }
            for (auto __iter_322 = iter(d->keys()); !__iter_322.done();) {
                k = next(__iter_322);
                if (to_bool(((k == str("0 str"))))) {
                    n += 1LL;
                }
            }
            for (auto __iter_323 = iter(d->values()); !__iter_323.done();) {
                v = next(__iter_323);
                if (to_bool(((v == 0LL)))) {
                    n += 1LL;
                }
            }
            for (auto __iter_324 = iter(d->items()); !__iter_324.done();) {
                destructure(k, v) = next(__iter_324);
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
    _int __stop_946 = 1000LL;
    for (j = 0; j < __stop_946; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_947 = mod(j, 10LL);
        for (i = 0; i < __stop_947; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_948 = 1000LL;
    for (i = 0; i < __stop_948; ++i) {
        for (auto __iter_325 = iter(a); !__iter_325.done();) {
            d = next(__iter_325);
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
    _int __stop_949 = (100LL * 1000LL);
    for (i = 0; i < __stop_949; ++i) {
        d = ptr(new dict<_int, ptr<list<_int>>>());
        _int __stop_950 = mod(i, 10LL);
        for (j = 0; j < __stop_950; ++j) {
            _int __stop_951 = mod(i, 11LL);
            for (k = 0; k < __stop_951; ++k) {
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
    _int __stop_952 = (1000LL * 1000LL);
    for (i = 0; i < __stop_952; ++i) {
        d = ptr(new dict<_int, str>());
        _int __stop_953 = mod(i, 4LL);
        for (j = 0; j < __stop_953; ++j) {
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
    _int __stop_954 = 100LL;
    for (j = 0; j < __stop_954; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_955 = mod(j, 10LL);
        for (i = 0; i < __stop_955; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_956 = (10LL * 1000LL);
    for (i = 0; i < __stop_956; ++i) {
        for (auto __iter_326 = iter(a); !__iter_326.done();) {
            d = next(__iter_326);
            d2 = d->copy();
            d3 = d2->copy();
            d4 = d3->copy();
            if (!(to_bool(((len(d4) == len(d)))))) throw AssertionError("");
        }
    }
}

ptr<list<tuple<str, str>>> __list_comprehension_42(ptr<list<tuple<str, str>>> s) {
    ptr<list<tuple<str, str>>> __tmp_42;
    str key;
    str value;
    __tmp_42 = ptr(new list<tuple<str, str>>());
    for (auto __iter_327 = iter(s); !__iter_327.done();) {
        destructure(key, value) = next(__iter_327);
        __tmp_42->append(tuple(key, value));
    }
    return __tmp_42;
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
    _int __stop_957 = 1000LL;
    for (j = 0; j < __stop_957; ++j) {
        items = ptr(new list<tuple<str, str>>({tuple(mod(str("Foobar-%d"), j), to_str(j)), tuple(mod(str("%d str"), j), str("x"))}));
        if (to_bool(((mod(j, 2LL) == 0LL)))) {
            items->append(tuple(str("blah"), str("bar")));
        }
        a->append(items);
    }
    n = 0LL;
    _int __stop_958 = 1000LL;
    for (i = 0; i < __stop_958; ++i) {
        for (auto __iter_328 = iter(a); !__iter_328.done();) {
            s = next(__iter_328);
            d = ptr(new dict<str, str>(__list_comprehension_42(s)));
            if (!(to_bool(((len(d) == len(s)))))) throw AssertionError("");
        }
    }
}

void dict_del_item() {
    ptr<dict<str, str>> d;
    _int j;
    d = ptr(new dict<str, str>({{str("long_lived"), str("value")}}));
    _int __stop_959 = (1000LL * 1000LL);
    for (j = 0; j < __stop_959; ++j) {
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
    