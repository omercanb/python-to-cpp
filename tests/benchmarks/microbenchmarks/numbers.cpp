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
_int SIZE;
_int SEED;
void matrix_multiply();
bool is_close(_float x, _float y);
tuple<ptr<list<ptr<list<_float>>>>, ptr<list<ptr<list<_float>>>>> setup_matrix_mult();
ptr<list<ptr<list<_float>>>> make_matrix(_int w, _int h);
ptr<list<ptr<list<_float>>>> multiply(ptr<list<ptr<list<_float>>>> a, ptr<list<ptr<list<_float>>>> b);
void int_to_float();
void str_to_float();
void float_abs();
void int_divmod();
void int_list();
_int sum_ints(ptr<list<_int>> a);
_int min_int(ptr<list<_int>> a);
void __init_module__();

void __init_module__() {
    SIZE = 30LL;
    SEED = 535LL;
}

void matrix_multiply() {
    ptr<list<ptr<list<_float>>>> m;
    ptr<list<ptr<list<_float>>>> m2;
    _int i;
    destructure(m, m2) = setup_matrix_mult();
    _int __stop_1 = 50LL;
    for (i = 0; i < __stop_1; ++i) {
        m = multiply(m, m2);
    }
    if (!(to_bool(is_close(m->__getitem__(0LL)->__getitem__(0LL), 3.630221302e+58)))) throw AssertionError(to_str(m->__getitem__(0LL)->__getitem__(0LL)));
}

bool is_close(_float x, _float y) {
    return ((0.999999 <= fdiv(x, y)) && (fdiv(x, y) <= 1.000001));
}

tuple<ptr<list<ptr<list<_float>>>>, ptr<list<ptr<list<_float>>>>> setup_matrix_mult() {
    return tuple(make_matrix(SIZE, SIZE), make_matrix(SIZE, SIZE));
}

ptr<list<ptr<list<_float>>>> make_matrix(_int w, _int h) {
    _int state;
    ptr<list<ptr<list<_float>>>> result;
    _int i;
    ptr<list<_float>> row;
    _int j;
    state = SEED;
    result = ptr(new list<ptr<list<_float>>>());
    _int __stop_2 = h;
    for (i = 0; i < __stop_2; ++i) {
        row = ptr(new list<_float>());
        _int __stop_3 = w;
        for (j = 0; j < __stop_3; ++j) {
            state = mod(((state * 1103515245LL) + 12345LL), pow(2LL, 31LL));
            row->append(fdiv(state, pow(2LL, 31LL)));
        }
        result->append(row);
    }
    return result;
}

ptr<list<ptr<list<_float>>>> multiply(ptr<list<ptr<list<_float>>>> a, ptr<list<ptr<list<_float>>>> b) {
    ptr<list<ptr<list<_float>>>> result;
    _int i;
    _int j;
    _float x;
    _int k;
    result = ptr(new list<ptr<list<_float>>>());
    _int __len_4 = len(a);
    for (i = 0; i < __len_4; ++i) {
        result->append((ptr(new list<_float>({0.0})) * len(b->__getitem__(0LL))));
        _int __len_5 = len(b->__getitem__(0LL));
        for (j = 0; j < __len_5; ++j) {
            x = 0.0;
            _int __len_6 = len(b);
            for (k = 0; k < __len_6; ++k) {
                x += (a->__getitem__(i)->__getitem__(k) * b->__getitem__(k)->__getitem__(j));
            }
            result->back()->__setitem__(j, x);
        }
    }
    return result;
}

void int_to_float() {
    ptr<list<_int>> a;
    _float x;
    _int i;
    _int n;
    a = ptr(new list<_int>({1LL, 4LL, 6LL, 7LL, 8LL, 9LL}));
    x = 0.0;
    _int __stop_7 = (1000LL * 1000LL);
    for (i = 0; i < __stop_7; ++i) {
        for (auto __iter_8 = iter(a); !__iter_8.done();) {
            n = next(__iter_8);
            x += to_float(n);
        }
    }
    if (!(to_bool(((x == 35000000.0))))) throw AssertionError(to_str(x));
}

void str_to_float() {
    ptr<list<str>> a;
    _float x;
    _int i;
    str n;
    a = ptr(new list<str>({str("1"), str("1.234567"), str("44324"), str("23.4"), str("-43.44e-4")}));
    x = 0.0;
    _int __stop_9 = (1000LL * 1000LL);
    for (i = 0; i < __stop_9; ++i) {
        for (auto __iter_10 = iter(a); !__iter_10.done();) {
            n = next(__iter_10);
            x += to_float(n);
        }
    }
    if (!(to_bool(is_close(x, 44349630223.26009)))) throw AssertionError(to_str(x));
}

void float_abs() {
    ptr<list<_float>> a;
    _float x;
    _int i;
    _float n;
    a = ptr(new list<_float>({1LL, (-1.234567), 44324LL, 23.4, (-0.004344)}));
    x = 0.0;
    _int __stop_11 = (1000LL * 1000LL);
    for (i = 0; i < __stop_11; ++i) {
        for (auto __iter_12 = iter(a); !__iter_12.done();) {
            n = next(__iter_12);
            x += abs(n);
        }
    }
    if (!(to_bool(is_close(x, 44349638911.052574)))) throw AssertionError(to_str(x));
}

void int_divmod() {
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int x;
    _int q;
    _int r;
    a = ptr(new list<_int>({1LL, 1235LL, 5434LL, 394879374LL, (-34453LL)}));
    n = 0LL;
    _int __stop_13 = (1000LL * 1000LL);
    for (i = 0; i < __stop_13; ++i) {
        for (auto __iter_14 = iter(a); !__iter_14.done();) {
            x = next(__iter_14);
            destructure(q, r) = divmod(x, 23LL);
            n += (q + r);
        }
    }
    if (!(to_bool(((n == 17167493000000LL))))) throw AssertionError(to_str(n));
}

void int_list() {
    ptr<list<_int>> a;
    ptr<list<_int>> b;
    ptr<list<_int>> c;
    _int n;
    _int i;
    a = ptr(new list<_int>(range(200LL)));
    b = ptr(new list<_int>(reversed(a)));
    c = (ptr(new list<_int>({(-1LL), 3LL, 7LL, 1234LL})) * 40LL);
    n = 0LL;
    _int __stop_15 = 4000LL;
    for (i = 0; i < __stop_15; ++i) {
        n += sum_ints(a);
        n += min_int(a);
        n += min_int(b);
        n += sum_ints(b);
        n += sum_ints(c);
        n += min_int(c);
    }
    if (!(to_bool(((n == 358076000LL))))) throw AssertionError(to_str(n));
}

_int sum_ints(ptr<list<_int>> a) {
    _int s;
    _int x;
    s = 0LL;
    for (auto __iter_16 = iter(a); !__iter_16.done();) {
        x = next(__iter_16);
        s += x;
    }
    return s;
}

_int min_int(ptr<list<_int>> a) {
    _int minimum;
    _int i;
    _int x;
    minimum = a->__getitem__(0LL);
    _int __stop_17 = len(a);
    for (i = 1LL; i < __stop_17; ++i) {
        x = a->__getitem__(i);
        if (to_bool(((x < minimum)))) {
            minimum = x;
        }
    }
    return minimum;
}


    int main() {
        __init_module__();
        auto t0 = std::chrono::steady_clock::now();
        int_list(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    