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
    _int a;
    _int b;
    _int c;
    ptr<list<_int>> l;
    _int d;
    ptr<list<_int>> l1;
    ptr<list<_int>> l2;
    a = 1LL;
    b = 2LL;
    c = 3LL;
    l = ptr(new list<_int>());
    l->append(1LL);
    print(l);
    print(((a < b) && (b < c)));
    print(((a > b)));
    print(((a > b) && (b > c)));
    d = 3LL;
    print(((c <= d)));
    print(((a == d)));
    print(((c == d)));
    l1 = ptr(new list<_int>({1LL, 2LL, 3LL}));
    l2 = ptr(new list<_int>({1LL, 2LL, 3LL}));
    print((__is(l1, l1)));
    print((__is(l1, l2)));
    return 0LL;
}
