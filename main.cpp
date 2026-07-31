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
void multiple_assignment() {
    _int x;
    _int y;
    ptr<list<_int>> a;
    _int n;
    _int i;
    _int xx;
    _int yy;
    x = 0LL;
    y = 1LL;
    a = ptr(new list<_int>({2LL, 3LL}));
    n = 0LL;
    for (_int i = 0; i < 1000000LL; ++i) {
        destructure(x, y) = tuple(y, x);
        destructure(a->__getitem__(0LL), a->__getitem__(1LL)) = tuple(a->__getitem__(1LL), a->__getitem__(0LL));
        destructure(xx, yy) = tuple(a->__getitem__(0LL), a->__getitem__(1LL));
    }
}

int main() {
    multiple_assignment();
    return 0LL;
}
