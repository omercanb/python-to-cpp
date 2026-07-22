#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "dict.h"
#include "set.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    ptr<set<_int>> s;
    ptr<set<_int>> a;
    ptr<set<_int>> b;
    ptr<set<_int>> small;
    ptr<set<_int>> big;
    ptr<set<_int>> nine;
    ptr<set<_int>> c;
    ptr<set<_int>> d;
    ptr<set<_int>> keep;
    ptr<set<_int>> drop;
    _int total;
    _int x;
    s = ptr(new set<_int>({3LL, 1LL, 2LL, 1LL}));
    print(len(s));
    print(sorted(s));
    print(_sorted_kwargs(true, s));
    s->add(4LL);
    print(sorted(s));
    s->add(4LL);
    print(len(s));
    s->remove(4LL);
    print(sorted(s));
    s->discard(99LL);
    print(sorted(s));
    a = ptr(new set<_int>({1LL, 2LL, 3LL}));
    b = ptr(new set<_int>({3LL, 4LL}));
    print(sorted((a | b)));
    print(sorted((a & b)));
    print(sorted((a - b)));
    print(sorted((a ^ b)));
    print(sorted(a->union_(b)));
    print(sorted(a->intersection(b)));
    print(sorted(a->difference(b)));
    print(sorted(a->symmetric_difference(b)));
    print(sorted(a), sorted(b));
    small = ptr(new set<_int>({1LL, 2LL}));
    big = ptr(new set<_int>({1LL, 2LL, 3LL}));
    print(small->issubset(big));
    print(big->issuperset(small));
    nine = ptr(new set<_int>({9LL}));
    print(small->isdisjoint(nine));
    print(small->isdisjoint(big));
    print(((small <= big)), ((small < big)));
    print(((big >= small)), ((big > small)));
    print(((ptr(new set<_int>({1LL, 2LL})) == ptr(new set<_int>({2LL, 1LL})))));
    print(((small != big)));
    c = a->copy();
    c->add(99LL);
    print(sorted(a), sorted(c));
    d = ptr(new set<_int>({1LL, 2LL, 3LL}));
    d->update(ptr(new set<_int>({4LL})));
    print(sorted(d));
    keep = ptr(new set<_int>({2LL, 3LL, 4LL}));
    d->intersection_update(keep);
    print(sorted(d));
    drop = ptr(new set<_int>({4LL}));
    d->difference_update(drop);
    print(sorted(d));
    d->symmetric_difference_update(ptr(new set<_int>({3LL, 5LL})));
    print(sorted(d));
    d->clear();
    print(len(d));
    total = 0LL;
    for (auto __iter = iter(ptr(new set<_int>({1LL, 2LL, 3LL}))); !__iter.done();) {
        x = next(__iter);
        total = (total + x);
    }
    print(total);
    return 0LL;
}
