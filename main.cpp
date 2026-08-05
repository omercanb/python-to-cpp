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
bool is_close(_float x, _float y);
ptr<list<ptr<list<_float>>>> make_matrix(_int w, _int h);
tuple<ptr<list<ptr<list<_float>>>>, ptr<list<ptr<list<_float>>>>> setup_matrix_mult();
ptr<list<ptr<list<_float>>>> multiply(ptr<list<ptr<list<_float>>>> a, ptr<list<ptr<list<_float>>>> b);
int main();

bool is_close(_float x, _float y) {
    return ((0.999999 <= fdiv(x, y)) && (fdiv(x, y) <= 1.000001));
}

ptr<list<ptr<list<_float>>>> make_matrix(_int w, _int h) {
    _int state;
    ptr<list<ptr<list<_float>>>> result;
    _int i;
    ptr<list<_float>> row;
    _int j;
    state = SEED;
    result = ptr(new list<ptr<list<_float>>>());
    _int __stop_1 = h;
    for (i = 0; i < __stop_1; ++i) {
        row = ptr(new list<_float>());
        _int __stop_2 = w;
        for (j = 0; j < __stop_2; ++j) {
            state = mod(((state * 1103515245LL) + 12345LL), pow(2LL, 31LL));
            row->append(fdiv(state, pow(2LL, 31LL)));
        }
        result->append(row);
    }
    return result;
}

tuple<ptr<list<ptr<list<_float>>>>, ptr<list<ptr<list<_float>>>>> setup_matrix_mult() {
    return tuple(make_matrix(SIZE, SIZE), make_matrix(SIZE, SIZE));
}

ptr<list<ptr<list<_float>>>> multiply(ptr<list<ptr<list<_float>>>> a, ptr<list<ptr<list<_float>>>> b) {
    ptr<list<ptr<list<_float>>>> result;
    _int i;
    _int j;
    _float x;
    _int k;
    result = ptr(new list<ptr<list<_float>>>());
    _int __len_3 = len(a);
    for (i = 0; i < __len_3; ++i) {
        result->append((ptr(new list<_float>({0.0})) * len(b->__getitem__(0LL))));
        _int __len_4 = len(b->__getitem__(0LL));
        for (j = 0; j < __len_4; ++j) {
            x = 0.0;
            _int __len_5 = len(b);
            for (k = 0; k < __len_5; ++k) {
                x += (a->__getitem__(i)->__getitem__(k) * b->__getitem__(k)->__getitem__(j));
            }
            result->back()->__setitem__(j, x);
        }
    }
    return result;
}

int main() {
    ptr<list<ptr<list<_float>>>> m;
    ptr<list<ptr<list<_float>>>> m2;
    _int i;
    SIZE = 30LL;
    SEED = 535LL;
    destructure(m, m2) = setup_matrix_mult();
    _int __stop_6 = 50LL;
    for (i = 0; i < __stop_6; ++i) {
        m = multiply(m, m2);
    }
    if (!(to_bool(is_close(m->__getitem__(0LL)->__getitem__(0LL), 3.630221302e+58)))) throw AssertionError(to_str(m->__getitem__(0LL)->__getitem__(0LL)));
    return 0LL;
}
