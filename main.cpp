#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "dict.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    ptr<list<_int>> l;
    _int x;
    _int y;
    _int z;
    ptr<list<_int>> l3;
    ptr<list<_int>> l2;
    _int n;
    l = ptr(new list<_int>({1LL, 2LL, 3LL}));
    l->append(4LL);
    print(l);
    l->insert(0LL, 100LL);
    print(l);
    l->insert(2LL, 200LL);
    print(l);
    l->insert(-1LL, 300LL);
    print(l);
    l->insert(100LL, 400LL);
    print(l);
    l->insert(-100LL, 500LL);
    print(l);
    l->remove(200LL);
    print(l);
    x = l->pop();
    print(x, l);
    y = l->pop(0LL);
    print(y, l);
    z = l->pop(-2LL);
    print(z, l);
    l->extend(ptr(new list<_int>({7LL, 8LL})));
    print(l);
    l3 = l->copy();
    print(l3);
    l->clear();
    print(l);
    l2 = ptr(new list<_int>({5LL, 3LL, 1LL, 3LL, 9LL}));
    print(l2->index(3LL));
    print(l2->index(3LL, 3LL));
    print(l2->index(3LL, 0LL, 2LL));
    print(l2->index(9LL, -2LL));
    print(l2->count(3LL));
    print(l2->count(42LL));
    l2->sort();
    print(l2);
    l2->sort(true);
    print(l2);
    l2->sort(false);
    print(l2);
    l2->reverse();
    print(l2);
    n = len(l2);
    print(n);
    print(l2->__getitem__(0LL), l2->__getitem__(-1LL));
    return 0LL;
}
