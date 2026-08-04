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
int main() {
    _int i;
    ptr<set<_int>> __set_comprehension_0;
    _int a;
    ptr<set<_int>> s;
    ptr<dict<_int, _int>> __dict_comprehension_0;
    ptr<dict<_int, _int>> d;
    ptr<dict<_int, _int>> __dict_comprehension_1;
    _int b;
    for (_int i = 0; i < 10LL; ++i) {
        print(i);
    }
    for (_int i = 0; i < 10LL; ++i) {
        print(i);
    }
    __set_comprehension_0 = ptr(new set<_int>());
    for (_int a = 0; a < 10LL; ++a) {
    }
    s = __set_comprehension_0;
    __dict_comprehension_0 = ptr(new dict<_int, _int>());
    for (_int a = 0; a < 10LL; ++a) {
        __dict_comprehension_0->__setitem__(a, a);
    }
    d = __dict_comprehension_0;
    __dict_comprehension_1 = ptr(new dict<_int, _int>());
    for (_int b = 0; b < 10LL; ++b) {
        __dict_comprehension_1->__setitem__(b, b);
    }
    __dict_comprehension_1;
    return 0LL;
}
