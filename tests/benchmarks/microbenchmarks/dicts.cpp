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
void dict_iteration() {
    ptr<list<ptr<dict<str, _int>>>> a;
    _int j;
    ptr<dict<str, _int>> d;
    _int i;
    _int n;
    str k;
    _int v;
    a = ptr(new list<ptr<dict<str, _int>>>());
    _int __stop_1 = 1000LL;
    for (j = 0; j < __stop_1; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_2 = mod(j, 10LL);
        for (i = 0; i < __stop_2; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_3 = 1000LL;
    for (i = 0; i < __stop_3; ++i) {
        for (auto __iter_4 = iter(a); !__iter_4.done();) {
            d = next(__iter_4);
            for (auto __iter_5 = iter(d); !__iter_5.done();) {
                k = next(__iter_5);
                if (to_bool(((k == str("0 str"))))) {
                }
            }
            for (auto __iter_6 = iter(d->keys()); !__iter_6.done();) {
                k = next(__iter_6);
                if (to_bool(((k == str("0 str"))))) {
                }
            }
            for (auto __iter_7 = iter(d->values()); !__iter_7.done();) {
                v = next(__iter_7);
                if (to_bool(((v == 0LL)))) {
                }
            }
            for (auto __iter_8 = iter(d->items()); !__iter_8.done();) {
                destructure(k, v) = next(__iter_8);
                if ((to_bool(((v == 1LL))) || to_bool(((k == str("1 str")))))) {
                }
            }
        }
    }
}

void dict_to_list() {
    ptr<list<ptr<dict<str, _int>>>> a;
    _int j;
    ptr<dict<str, _int>> d;
    _int i;
    _int n;
    a = ptr(new list<ptr<dict<str, _int>>>());
    _int __stop_9 = 1000LL;
    for (j = 0; j < __stop_9; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_10 = mod(j, 10LL);
        for (i = 0; i < __stop_10; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_11 = 1000LL;
    for (i = 0; i < __stop_11; ++i) {
        for (auto __iter_12 = iter(a); !__iter_12.done();) {
            d = next(__iter_12);
            (n + (+len(ptr(new list<str>(d)))));
        }
    }
}

void dict_set_default() {
    _int n;
    _int i;
    ptr<dict<_int, ptr<list<_int>>>> d;
    _int j;
    _int k;
    n = 0LL;
    _int __stop_13 = (100LL * 1000LL);
    for (i = 0; i < __stop_13; ++i) {
        d = ptr(new dict<_int, ptr<list<_int>>>());
        _int __stop_14 = mod(i, 10LL);
        for (j = 0; j < __stop_14; ++j) {
            _int __stop_15 = mod(i, 11LL);
            for (k = 0; k < __stop_15; ++k) {
                d->setdefault(j, ptr(new list<_int>()))->append(k);
            }
        }
    }
}

void dict_clear() {
    _int n;
    _int i;
    ptr<dict<_int, str>> d;
    _int j;
    n = 0LL;
    _int __stop_16 = (1000LL * 1000LL);
    for (i = 0; i < __stop_16; ++i) {
        d = ptr(new dict<_int, str>());
        _int __stop_17 = mod(i, 4LL);
        for (j = 0; j < __stop_17; ++j) {
            d->__setitem__(j, str("x"));
        }
        d->clear();
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
    _int __stop_18 = 100LL;
    for (j = 0; j < __stop_18; ++j) {
        d = ptr(new dict<str, _int>());
        _int __stop_19 = mod(j, 10LL);
        for (i = 0; i < __stop_19; ++i) {
            d->__setitem__(mod(str("Foobar-%d"), j), j);
            d->__setitem__(mod(str("%d str"), j), i);
        }
        a->append(d);
    }
    n = 0LL;
    _int __stop_20 = (10LL * 1000LL);
    for (i = 0; i < __stop_20; ++i) {
        for (auto __iter_21 = iter(a); !__iter_21.done();) {
            d = next(__iter_21);
            d2 = d->copy();
            d3 = d2->copy();
            d4 = d3->copy();
        }
    }
}

ptr<list<tuple<str, str>>> __list_comprehension_48(ptr<list<tuple<str, str>>> s) {
    ptr<list<tuple<str, str>>> __tmp_48;
    str key;
    str value;
    __tmp_48 = ptr(new list<tuple<str, str>>());
    for (auto __iter_22 = iter(s); !__iter_22.done();) {
        destructure(key, value) = next(__iter_22);
        __tmp_48->append(tuple(key, value));
    }
    return __tmp_48;
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
    _int __stop_23 = 1000LL;
    for (j = 0; j < __stop_23; ++j) {
        items = ptr(new list<tuple<str, str>>({tuple(mod(str("Foobar-%d"), j), to_str(j)), tuple(mod(str("%d str"), j), str("x"))}));
        if (to_bool(((mod(j, 2LL) == 0LL)))) {
            items->append(tuple(str("blah"), str("bar")));
        }
        a->append(items);
    }
    n = 0LL;
    _int __stop_24 = 1000LL;
    for (i = 0; i < __stop_24; ++i) {
        for (auto __iter_25 = iter(a); !__iter_25.done();) {
            s = next(__iter_25);
            d = ptr(new dict<str, str>(__list_comprehension_48(s)));
        }
    }
}

void dict_del_item() {
    ptr<dict<str, str>> d;
    _int j;
    d = ptr(new dict<str, str>({{str("long_lived"), str("value")}}));
    _int __stop_26 = (1000LL * 1000LL);
    for (j = 0; j < __stop_26; ++j) {
        d->__setitem__(str("xyz"), str("asdf"));
        d->__setitem__(str("asdf"), str("lulz"));
        d->__setitem__(str("foobar"), str("baz zar"));
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        dict_del_item(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    