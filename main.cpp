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
    ptr<list<_int>> l;
    ptr<dict<_int, _int>> d;
    ptr<set<_int>> s;
    str text;
    tuple<_int, _int, _int> t;
    ptr<list<tuple<_int, _int>>> pairs;
    ptr<set<tuple<_int, _int>>> pair_set;
    ptr<dict<tuple<_int, _int>, str>> pair_dict;
    tuple<tuple<_int, _int>, tuple<_int, _int>> nested;
    ptr<list<tuple<str, _int>>> mixed;
    ptr<list<str>> strs;
    _int count;
    _int x;
    l = ptr(new list<_int>({1LL, 2LL, 3LL}));
    print((l->__contains__(2LL)), (l->__contains__(9LL)));
    print((!l->__contains__(2LL)), (!l->__contains__(9LL)));
    d = ptr(new dict<_int, _int>({{1LL, 10LL}, {2LL, 20LL}}));
    print((d->__contains__(1LL)), (d->__contains__(9LL)));
    print((d->values()->__contains__(10LL)));
    print((!d->__contains__(1LL)), (!d->__contains__(9LL)));
    s = ptr(new set<_int>({1LL, 2LL, 3LL}));
    print((s->__contains__(2LL)), (s->__contains__(9LL)));
    print((!s->__contains__(2LL)), (!s->__contains__(9LL)));
    text = str("hello world");
    print((text.__contains__(str("hello"))), (text.__contains__(str("zz"))));
    print((text.__contains__(str("o w"))));
    print((!text.__contains__(str("hello"))), (!text.__contains__(str("zz"))));
    t = tuple(1LL, 2LL, 3LL);
    print((t.__contains__(2LL)), (t.__contains__(9LL)));
    pairs = ptr(new list<tuple<_int, _int>>({tuple(1LL, 2LL), tuple(3LL, 4LL)}));
    print((pairs->__contains__(tuple(1LL, 2LL))), (pairs->__contains__(tuple(9LL, 9LL))));
    print((!pairs->__contains__(tuple(1LL, 2LL))), (!pairs->__contains__(tuple(9LL, 9LL))));
    print((pairs->__contains__(tuple(2LL, 1LL))));
    pair_set = ptr(new set<tuple<_int, _int>>({tuple(1LL, 2LL), tuple(3LL, 4LL)}));
    print((pair_set->__contains__(tuple(1LL, 2LL))), (pair_set->__contains__(tuple(9LL, 9LL))));
    print((pair_set->__contains__(tuple(2LL, 1LL))));
    pair_dict = ptr(new dict<tuple<_int, _int>, str>({{tuple(1LL, 2LL), str("a")}, {tuple(3LL, 4LL), str("b")}}));
    print((pair_dict->__contains__(tuple(1LL, 2LL))), (pair_dict->__contains__(tuple(9LL, 9LL))));
    nested = tuple(tuple(1LL, 2LL), tuple(3LL, 4LL));
    print((nested.__contains__(tuple(1LL, 2LL))), (nested.__contains__(tuple(9LL, 9LL))));
    mixed = ptr(new list<tuple<str, _int>>({tuple(str("a"), 1LL), tuple(str("b"), 2LL)}));
    print((mixed->__contains__(tuple(str("a"), 1LL))), (mixed->__contains__(tuple(str("a"), 2LL))));
    strs = ptr(new list<str>({str("a"), str("b")}));
    print((strs->__contains__(str("a"))), (strs->__contains__(str("z"))));
    if (to_bool((l->__contains__(2LL)))) {
        print(str("found"));
    } else {
        print(str("missing"));
    }
    count = 0LL;
    for (auto __iter = iter(ptr(new list<_int>({1LL, 2LL, 3LL, 4LL}))); !__iter.done();) {
        x = next(__iter);
        if (to_bool((s->__contains__(x)))) {
            count = (count + 1LL);
        }
    }
    print(count);
    return 0LL;
}
