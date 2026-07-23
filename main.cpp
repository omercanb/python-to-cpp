#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "strops.h"
#include "dict.h"
#include "set.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    _int a;
    _int b;
    _int x;
    str s;
    _int p;
    _int q;
    _int m;
    _int n;
    tuple<_int, _int> t;
    tuple<_int, _int> t2;
    _int z;
    destructure(a, b) = tuple(1LL, 2LL);
    print(str("Test 1 - Simple destructure:"), a, b);
    destructure(a, b) = tuple(10LL, 20LL);
    print(str("Test 2 - Reassign:"), a, b);
    destructure(x, s) = tuple(42LL, str("hello"));
    print(str("Test 3 - Mixed types:"), x, s);
    destructure(p, q) = tuple(100LL, 200LL);
    destructure(m, n) = tuple(p, q);
    print(str("Test 4 - Chained destructure:"), m, n);
    t = tuple(1LL, 2LL);
    t2 = t;
    z = t.get<0>();
    z = t.get<1>();
    return 0LL;
}
