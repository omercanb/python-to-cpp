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
ptr<list<_int>> __list_comprehension_0() {
    ptr<list<_int>> __tmp_0;
    _int n;
    __tmp_0 = ptr(new list<_int>());
    _int __stop_1 = 10LL;
    for (n = 0; n < __stop_1; ++n) {
        __tmp_0->append(n);
    }
    return __tmp_0;
}

ptr<list<_int>> __list_comprehension_1(_int x) {
    ptr<list<_int>> __tmp_1;
    __tmp_1 = ptr(new list<_int>());
    _int __stop_2 = x;
    for (x = 0; x < __stop_2; ++x) {
        __tmp_1->append(x);
    }
    return __tmp_1;
}

ptr<dict<_int, _int>> __dict_comprehension_0(_int x) {
    ptr<dict<_int, _int>> __tmp_2;
    __tmp_2 = ptr(new dict<_int, _int>());
    _int __stop_3 = x;
    for (x = 0; x < __stop_3; ++x) {
        if (to_bool(((mod(x, 2LL) == 0LL)))) {
            __tmp_2->__setitem__(x, x);
        }
    }
    return __tmp_2;
}

ptr<list<_int>> __list_comprehension_2(_int x) {
    ptr<list<_int>> __tmp_3;
    _int y;
    __tmp_3 = ptr(new list<_int>());
    _int __stop_4 = x;
    for (x = 0; x < __stop_4; ++x) {
        if (to_bool(mod(x, 2LL))) {
            _int __stop_5 = x;
            for (y = 0; y < __stop_5; ++y) {
                if (to_bool(mod(y, 2LL))) {
                    __tmp_3->append(x);
                }
            }
        }
    }
    return __tmp_3;
}

ptr<list<tuple<_int, _int>>> __list_comprehension_3(ptr<list<_int>> z, _int x) {
    ptr<list<tuple<_int, _int>>> __tmp_4;
    __tmp_4 = ptr(new list<tuple<_int, _int>>());
    for (auto __iter_6 = iter(zip(z, range(x))); !__iter_6.done();) {
        x = next(__iter_6);
        __tmp_4->append(x);
    }
    return __tmp_4;
}

ptr<list<str>> __list_comprehension_4() {
    ptr<list<str>> __tmp_5;
    str x;
    __tmp_5 = ptr(new list<str>());
    for (auto __iter_7 = iter(str("a,b,c,d")); !__iter_7.done();) {
        x = next(__iter_7);
        __tmp_5->append(x);
    }
    return __tmp_5;
}

ptr<list<tuple<_int, str>>> __list_comprehension_5(_int x) {
    ptr<list<tuple<_int, str>>> __tmp_6;
    __tmp_6 = ptr(new list<tuple<_int, str>>());
    for (auto __iter_8 = iter(zip(range(x), str("a, b, c, d"))); !__iter_8.done();) {
        x = next(__iter_8);
        __tmp_6->append(x);
    }
    return __tmp_6;
}

int main() {
    _int x;
    _int y;
    ptr<list<_int>> z;
    __list_comprehension_0();
    x = 20LL;
    __list_comprehension_1(x);
    __dict_comprehension_0(x);
    __list_comprehension_2(x);
    y = 10LL;
    z = ptr(new list<_int>({1LL, 2LL, 3LL}));
    __list_comprehension_3(z, x);
    __list_comprehension_4();
    __list_comprehension_5(x);
    return 0LL;
}
