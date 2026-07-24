#include "dict.h"
#include "exceptions.h"
#include "finally.h"
#include "iter.h"
#include "list.h"
#include "mathops.h"
#include "print.h"
#include "ptr.h"
#include "scalars.h"
#include "set.h"
#include "slice.h"
#include "strops.h"
#include "truthy.h"
#include "tuple.h"
#include "types.h"
using namespace py;

namespace prog_boolops {
_int side(_int v) {
    print(str("SIDE"));
    return v;
}

int run() {
    _int a;
    _int b;
    _int zero;
    str empty;
    str text;
    ptr<list<_int>> no_items;
    _float f;
    _float g;
    _int n;
    a = 1LL;
    b = 2LL;
    zero = 0LL;
    print(_and(a, b));
    print(_or(a, b));
    print(_and(zero, b));
    print(_or(zero, b));
    print(_and(zero, zero));
    print(_or(zero, zero));
    empty = str("");
    text = str("hi");
    print(_or(empty, text));
    print(_and(text, empty));
    print(_or(text, empty));
    print(_and(empty, text));
    no_items = ptr(new list<_int>());
    print(_or(no_items, ptr(new list<_int>({1LL, 2LL}))));
    print(_and(ptr(new list<_int>({3LL})), no_items));
    print(_or(ptr(new list<_int>({3LL})), ptr(new list<_int>({4LL}))));
    print(_and(no_items, ptr(new list<_int>({4LL}))));
    f = 0.0;
    g = 2.5;
    print(_or(f, g));
    print(_and(g, f));
    print(_and(zero, side(9LL)));
    print(_or(a, side(9LL)));
    print(_and(a, side(9LL)));
    print(_or(zero, side(9LL)));
    print(_and(a, _and(b, 3LL)));
    print(_or(zero, _or(zero, 3LL)));
    print(_or(_and(a, b), 3LL));
    print(_or(zero, _and(b, 3LL)));
    print((_and(a, b) + 1LL));
    if ((to_bool(a) && to_bool(text))) {
        print(str("cond and"));
    }
    if ((to_bool(empty) || to_bool(a))) {
        print(str("cond or"));
    }
    if ((!(to_bool(empty) || to_bool(zero)))) {
        print(str("cond not"));
    }
    if ((to_bool(a) && (to_bool(text) && to_bool(b)))) {
        print(str("cond chained"));
    }
    if ((to_bool(no_items) || to_bool(text))) {
        print(str("cond mixed"));
    }
    if ((to_bool(zero) && to_bool(side(9LL)))) {
        print(str("unreachable"));
    }
    n = 0LL;
    // While loop
    while ((to_bool(((n < 2LL))) && to_bool(text))) {
        n = (n + 1LL);
    }
    print(n);
    print((!to_bool(a)));
    print((!to_bool(zero)));
    print((!to_bool(empty)));
    print((!to_bool(_and(a, b))));
    return 0LL;
}
}

namespace prog_casts {
int run() {
    _float a;
    _int b;
    _float c;
    str float_str;
    _float f1;
    str int_str;
    _int i1;
    _int i2;
    a = 2.0;
    b = to_int(a);
    c = to_float(b);
    float_str = str("  0.10 ");
    f1 = to_float(float_str);
    int_str = str("100");
    i1 = to_int(int_str);
    i2 = to_int(int_str, 2LL);
    print(a, b, c, f1, i1, i2);
    return 0LL;
}
}

namespace prog_comparison {
int run() {
    _int a;
    _int b;
    _int c;
    _int d;
    ptr<list<_int>> l1;
    ptr<list<_int>> l2;
    a = 1LL;
    b = 2LL;
    c = 3LL;
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
}

namespace prog_dict {
int run() {
    ptr<dict<_int, _int>> d;
    ptr<dict<_int, _int>> e;
    ptr<dict<_int, _int>> c;
    ptr<dict<str, _int>> s;
    d = ptr(new dict<_int, _int>({{1LL, 10LL}, {2LL, 20LL}, {3LL, 30LL}}));
    print(len(d));
    print(d->__getitem__(1LL), d->__getitem__(2LL), d->__getitem__(3LL));
    print(sorted(d));
    print(_sorted_kwargs(true, d));
    d->__setitem__(4LL, 40LL);
    print(len(d), d->__getitem__(4LL));
    d->__setitem__(1LL, 11LL);
    print(len(d), d->__getitem__(1LL));
    print(d->get(1LL));
    print(d->get(99LL, (-1LL)));
    print(d->pop(4LL));
    print(d->pop(99LL, (-1LL)));
    print(len(d));
    print(d->setdefault(2LL, 999LL));
    print(d->setdefault(9LL, 90LL));
    print(sorted(d));
    print(sorted(d->keys()));
    print(sorted(d->values()));
    e = ptr(new dict<_int, _int>({{5LL, 50LL}}));
    d->update(e);
    print(sorted(d));
    c = d->copy();
    print(len(c));
    c->clear();
    print(len(c), len(d));
    s = ptr(new dict<str, _int>({{str("b"), 2LL}, {str("a"), 1LL}}));
    print(sorted(s));
    print(s->__getitem__(str("a")), s->__getitem__(str("b")));
    return 0LL;
}
}

namespace prog_exceptions {
_int guarded_parse(str text) {
    str("finally must run when the try returns, and when it raises through.");
    {
        Finally __finally([&] {
            print(str("cleanup"), text);
        });
        return to_int(text);
    }
}

_int parse_or(str text, _int fallback) {
    _int value;
    str("else runs only when nothing was raised.");
    {
        bool __thrown = false;
        try {
            value = to_int(text);
        } catch (ValueError &) {
            __thrown = true;
            print(str("bad literal"), text);
            return fallback;
        }
        if (!__thrown) {
            print(str("good literal"), text);
            return value;
        }
    }
}

_int nested() {
    {
        Finally __finally([&] {
            print(str("outer finally"));
        });
        try {
            {
                Finally __finally([&] {
                    print(str("inner finally"));
                });
                return to_int(str("nope"));
            }
        } catch (ValueError &) {
            print(str("outer caught"));
            return (-1LL);
        }
    }
}

_int handler_raises() {
    str("A raising handler skips else and still runs finally on the way out.");
    try {
        {
            Finally __finally([&] {
                print(str("guard ran"));
            });
            bool __thrown = false;
            try {
                print(to_int(str("bad")));
            } catch (ValueError &) {
                __thrown = true;
                print(str("handler raising"));
                return to_int(str("worse"));
            }
            if (!__thrown) {
                print(str("not reached"));
            }
        }
    } catch (ValueError &) {
        print(str("caught the handler's exception"));
    }
    return 0LL;
}

_int check_positive(_int n) {
    if (to_bool(((n < 0LL)))) {
        throw ValueError(str("negative"));
    }
    return n;
}

_int reraise(_int n) {
    str("A bare raise passes the live exception on, finally still runs.");
    {
        Finally __finally([&] {
            print(str("reraise finally"));
        });
        try {
            return check_positive(n);
        } catch (ValueError &) {
            print(str("logging and passing it on"));
            throw;
        }
    }
}

_int raise_bare_class(str key) {
    throw KeyError("");
}

_int siblings(str first, str second) {
    str("Two try statements in one scope must not collide over their flags.");
    {
        bool __thrown = false;
        try {
            print(to_int(first));
        } catch (ValueError &) {
            __thrown = true;
            print(str("first was bad"));
        }
        if (!__thrown) {
            print(str("first was fine"));
        }
    }
    {
        bool __thrown = false;
        try {
            print(to_int(second));
        } catch (ValueError &) {
            __thrown = true;
            print(str("second was bad"));
        }
        if (!__thrown) {
            print(str("second was fine"));
        }
    }
    return 0LL;
}

_int relay() {
    str("`raise e` keeps the real type, rather than the one the handler declared.");
    try {
        throw ValueError(str("original"));
    } catch (PyException &e) {
        print(str("relaying"));
        e.raise();
    }
}

int run() {
    ptr<list<_int>> numbers;
    ptr<dict<str, _int>> counts;
    _int i;
    print(guarded_parse(str("41")));
    try {
        print(guarded_parse(str("zzz")));
    } catch (ValueError &) {
        print(str("caught from callee"));
    }
    print(parse_or(str("7"), 0LL));
    print(parse_or(str("seven"), 0LL));
    print(nested());
    print(handler_raises());
    print(check_positive(3LL));
    try {
        print(check_positive((-1LL)));
    } catch (ValueError &) {
        print(str("caught the raise"));
    }
    try {
        print(reraise((-2LL)));
    } catch (ValueError &) {
        print(str("caught the re-raise"));
    }
    try {
        print(raise_bare_class(str("k")));
    } catch (KeyError &) {
        print(str("caught the bare class"));
    }
    print(siblings(str("8"), str("eight")));
    try {
        print(relay());
    } catch (ValueError &) {
        print(str("still a ValueError after the relay"));
    }
    try {
        throw TypeError(str("wrong type"));
    } catch (PyException &) {
        print(str("base handler took the subclass"));
    }
    numbers = ptr(new list<_int>({1LL, 2LL, 3LL}));
    try {
        print(numbers->__getitem__(10LL));
    } catch (IndexError &) {
        print(str("index error wins over the base class"));
    } catch (PyException &) {
        print(str("not reached"));
    }
    counts = ptr(new dict<str, _int>({{str("a"), 1LL}}));
    try {
        print(counts->__getitem__(str("b")));
    } catch (PyException &) {
        print(str("bare except caught it"));
    }
    try {
        print(to_float(str("x")));
    } catch (ValueError &e) {
        print(str("float refused it"));
    }
    for (_int i = 0; i < 3LL; ++i) {
        {
            Finally __finally([&] {
                print(str("loop finally"), i);
            });
            if (to_bool(((i == 1LL)))) {
                break;
            }
            print(str("loop"), i);
        }
    }
    return 0LL;
}
}

namespace prog_iter {
int run() {
    ptr<list<_int>> nums;
    ptr<list<_int>> a;
    str s;
    ptr<list<_int>> filtered;
    _int x;
    _int y;
    _int i;
    _int n;
    nums = ptr(new list<_int>({1LL, 2LL, 3LL, 4LL, 5LL}));
    a = ptr(new list<_int>(map([](auto x) { return (x * 2LL); }, nums)));
    print(a);
    for (auto __iter = iter(map([](auto x) { return to_str(x); }, nums)); !__iter.done();) {
        s = next(__iter);
        print(s);
    }
    filtered = ptr(new list<_int>(filter([](auto x) { return ((mod(x, 2LL) == 0LL)); }, nums)));
    print(filtered);
    for (auto __iter = iter(zip(nums, a)); !__iter.done();) {
        destructure(x, y) = next(__iter);
        print(x, y);
    }
    nums = a;
    for (auto __iter = iter(enumerate(nums)); !__iter.done();) {
        destructure(i, n) = next(__iter);
        print(i, n);
    }
    return 0LL;
}
}

namespace prog_list {
ptr<list<_int>> give_list(ptr<list<_int>> l) {
    print(l);
    l->append(2LL);
    print(l);
    return l;
}

int run() {
    ptr<list<_int>> l;
    _int a;
    ptr<list<_int>> l2;
    _int x;
    _int y;
    _int z;
    ptr<list<_int>> l3;
    _int n;
    print(ptr(new list<_int>(ptr(new list<_int>({1LL, 2LL, 3LL})))));
    l = ptr(new list<_int>({1LL, 2LL, 3LL}));
    print(l);
    l = ptr(new list<_int>({1LL, 2LL, 3LL}));
    print(l);
    l->append(4LL);
    print(l);
    l = give_list(l);
    print(l);
    print(l->__getitem__(1LL));
    a = l->__getitem__(0LL);
    print(l);
    l->__setitem__(0LL, a);
    print(l);
    l->__setitem__(0LL, 2LL);
    print(l);
    l2 = l->__getitem__(slice(0LL, 1LL, std::nullopt));
    print(l2);
    l->insert(0LL, 100LL);
    print(l);
    l->insert(2LL, 200LL);
    print(l);
    l->insert((-1LL), 300LL);
    print(l);
    l->insert(100LL, 400LL);
    print(l);
    l->insert((-100LL), 500LL);
    print(l);
    l->remove(200LL);
    print(l);
    x = l->pop();
    print(x, l);
    y = l->pop(0LL);
    print(y, l);
    z = l->pop((-2LL));
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
    print(l2->index(9LL, (-2LL)));
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
    print(l2->__getitem__(0LL), l2->__getitem__((-1LL)));
    return 0LL;
}
}

namespace prog_loops {
int run() {
    _int x;
    ptr<list<_int>> l;
    _int i;
    _int step;
    _int n;
    x = 2LL;
    l = ptr(new list<_int>({2LL, 3LL, 4LL}));
    for (size_t i = 0; i < len(l); ++i) {
        print(l);
    }
    for (_int i = 0; i < x; ++i) {
        print(str("first"), i);
    }
    for (_int i = x; i < (x + 5LL); ++i) {
        print(str("second"), i);
    }
    for (_int i = x; i < (x + 10LL); i += 2) {
        print(str("third"), i);
    }
    for (_int i = x;; i += (-2LL)) {
        if (((-2LL) > 0 && i >= (x - 7LL)) || ((-2LL) < 0 && i <= (x - 7LL))) break;
        print(str("fourth"), i);
    }
    step = x;
    for (_int i = x;; i += step) {
        if ((step > 0 && i >= (10LL * x)) || (step < 0 && i <= (10LL * x))) break;
        print(str("fifth"), i);
    }
    step = (-2LL);
    for (_int i = (5LL * x);; i += step) {
        if ((step > 0 && i >= (10LL * x)) || (step < 0 && i <= (10LL * x))) break;
        print(str("sixth"), i);
    }
    for (auto __iter = iter(l); !__iter.done();) {
        n = next(__iter);
        print(str("seventh"), n);
    }
    for (auto __iter = iter(l); !__iter.done();) {
        n = next(__iter);
        print(str("eight"), n);
    }
    return 0LL;
}
}

namespace prog_math {
int run() {
    _int a;
    print(pow(10LL, 10LL));
    print(idiv((-10LL), 3LL));
    print(idiv(10LL, 3LL));
    print(fdiv(5LL, 2LL));
    print(pow(0.5, 4LL));
    print((50.0 * 100LL));
    a = pow(10LL, 10LL);
    print((-(-5LL)));
    print((~5LL));
    print((-(+5LL)));
    return a;
}
}

namespace prog_membership {
int run() {
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
}

namespace prog_print {
int run() {
    _int a;
    _int b;
    _int c;
    a = 1LL;
    b = 2LL;
    c = 3LL;
    print();
    print(a);
    print(a, b, c);
    _print_kwargs(str(" "), str("end"));
    _print_kwargs(str("sep"), str("\n"));
    _print_kwargs(str("-"), str("\n"), a, b, c);
    _print_kwargs(str(" "), str("()"), a);
    _print_kwargs(str(" "), str("()"), b);
    print(c);
    _print_kwargs(str("sep"), str("end"), a, b, c);
    return 0LL;
}
}

namespace prog_set {
int run() {
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
    ptr<set<tuple<_int, _int>>> s1;
    ptr<set<tuple<_int, _int>>> s2;
    ptr<set<str>> s3;
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
    s1 = ptr(new set<tuple<_int, _int>>({tuple(1LL, 2LL), tuple(1LL, 3LL)}));
    print(sorted(s1));
    s2 = ptr(new set<tuple<_int, _int>>({tuple(1LL, 2LL), tuple(1LL, 2LL)}));
    print(sorted(s2));
    s3 = ptr(new set<str>({str("Hello"), str("World")}));
    print(sorted(s3));
    return 0LL;
}
}

namespace prog_slice {
int run() {
    ptr<list<_int>> l;
    ptr<list<_int>> empty;
    ptr<list<_int>> original;
    ptr<list<_int>> copied;
    str s;
    l = ptr(new list<_int>({0LL, 1LL, 2LL, 3LL, 4LL, 5LL}));
    print(l->__getitem__(slice(0LL, 1LL, std::nullopt)));
    print(l->__getitem__(slice(1LL, 4LL, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, 3LL, std::nullopt)));
    print(l->__getitem__(slice(3LL, std::nullopt, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, std::nullopt, 2LL)));
    print(l->__getitem__(slice(1LL, 5LL, 2LL)));
    print(l->__getitem__(slice(std::nullopt, std::nullopt, 3LL)));
    print(l->__getitem__(slice((-3LL), std::nullopt, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, (-2LL), std::nullopt)));
    print(l->__getitem__(slice((-4LL), (-1LL), std::nullopt)));
    print(l->__getitem__(slice((-1LL), std::nullopt, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, std::nullopt, (-1LL))));
    print(l->__getitem__(slice(4LL, 1LL, (-1LL))));
    print(l->__getitem__(slice(std::nullopt, std::nullopt, (-2LL))));
    print(l->__getitem__(slice((-1LL), (-4LL), (-1LL))));
    print(l->__getitem__(slice(10LL, 20LL, std::nullopt)));
    print(l->__getitem__(slice((-100LL), 100LL, std::nullopt)));
    print(l->__getitem__(slice(std::nullopt, 100LL, std::nullopt)));
    print(l->__getitem__(slice((-100LL), std::nullopt, std::nullopt)));
    print(l->__getitem__(slice(2LL, 2LL, std::nullopt)));
    print(l->__getitem__(slice(4LL, 1LL, std::nullopt)));
    print(l->__getitem__(slice(1LL, 4LL, (-1LL))));
    empty = ptr(new list<_int>());
    print(empty->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt)));
    print(empty->__getitem__(slice(0LL, 5LL, std::nullopt)));
    print(empty->__getitem__(slice(std::nullopt, std::nullopt, (-1LL))));
    original = ptr(new list<_int>({1LL, 2LL, 3LL}));
    copied = original->__getitem__(slice(std::nullopt, std::nullopt, std::nullopt));
    copied->append(4LL);
    print(original, copied);
    s = str("abcdef");
    print(s.__getitem__(slice(0LL, 1LL, std::nullopt)));
    print(s.__getitem__(slice(1LL, 4LL, std::nullopt)));
    print(s.__getitem__(slice(std::nullopt, 3LL, std::nullopt)));
    print(s.__getitem__(slice(3LL, std::nullopt, std::nullopt)));
    print(s.__getitem__(slice(std::nullopt, std::nullopt, std::nullopt)));
    print(s.__getitem__(slice(std::nullopt, std::nullopt, 2LL)));
    print(s.__getitem__(slice(1LL, 5LL, 2LL)));
    print(s.__getitem__(slice((-3LL), std::nullopt, std::nullopt)));
    print(s.__getitem__(slice(std::nullopt, (-2LL), std::nullopt)));
    print(s.__getitem__(slice((-4LL), (-1LL), std::nullopt)));
    print(s.__getitem__(slice(std::nullopt, std::nullopt, (-1LL))));
    print(s.__getitem__(slice(4LL, 1LL, (-1LL))));
    print(s.__getitem__(slice(std::nullopt, std::nullopt, (-2LL))));
    print(s.__getitem__(slice(100LL, 200LL, std::nullopt)));
    print(s.__getitem__(slice((-100LL), 100LL, std::nullopt)));
    print(s.__getitem__(slice(2LL, 2LL, std::nullopt)));
    print(s.__getitem__(slice(4LL, 1LL, std::nullopt)));
    print(str("").__getitem__(slice(std::nullopt, std::nullopt, std::nullopt)));
    print(str("").__getitem__(slice(0LL, 5LL, std::nullopt)));
    return 0LL;
}
}

namespace prog_string {
int run() {
    str s;
    str padded;
    str a;
    str b;
    str joined;
    str c;
    s = str("Hello World");
    print(s);
    print(len(s));
    print(s.__getitem__(0LL), s.__getitem__((-1LL)));
    print(s.upper());
    print(s.lower());
    print(s.swapcase());
    print(s.capitalize());
    print(str("hello world").title());
    print(s.casefold());
    print(s.find(str("o")));
    print(s.find(str("o"), 5LL));
    print(s.rfind(str("o")));
    print(s.find(str("zz")));
    print(s.index(str("World")));
    print(s.count(str("l")));
    print(s.count(str("zz")));
    print(s.startswith(str("Hello")));
    print(s.startswith(str("World")));
    print(s.endswith(str("World")));
    print(s.replace(str("l"), str("L")));
    print(s.replace(str("l"), str("L"), 2LL));
    print(s.removeprefix(str("Hello ")));
    print(s.removesuffix(str(" World")));
    padded = str("  spaced  ");
    print(padded.strip());
    print(padded.lstrip());
    print(padded.rstrip());
    print(str("xxhixx").strip(str("x")));
    print(str("hi").ljust(5LL, str(".")));
    print(str("hi").rjust(5LL, str(".")));
    print(str("hi").center(6LL, str(".")));
    print(str("42").zfill(5LL));
    print(str("-42").zfill(5LL));
    print(str("abc").isalpha(), str("a1").isalpha());
    print(str("123").isdigit(), str("12a").isdigit());
    print(str("a1").isalnum(), str("a-1").isalnum());
    print(str("  ").isspace(), str("a ").isspace());
    print(str("ABC").isupper(), str("Abc").isupper());
    print(str("abc").islower(), str("Abc").islower());
    print(s.split());
    print(str("a,b,c").split(str(",")));
    print(str("a,,b").split(str(",")));
    print(str("-").join(str("a,b,c").split(str(","))));
    print(str("one\ntwo").splitlines());
    a = str("foo");
    b = str("bar");
    print((a + b));
    print((a * 3LL));
    print(((a == str("foo"))), ((a == b)));
    print(((a < b)), ((a > b)));
    print(to_str(42LL));
    print(to_str(3.5));
    print(to_str(true));
    print(to_int(str("100")));
    print(to_float(str("0.5")));
    joined = str("");
    for (auto __iter = iter(str("abc")); !__iter.done();) {
        c = next(__iter);
        joined = ((joined + c) + str("."));
    }
    print(joined);
    return 0LL;
}
}

namespace prog_truthy {
int run() {
    _int a;
    _int b;
    str s1;
    str s2;
    ptr<list<_int>> empty;
    ptr<list<_int>> full;
    _int n;
    a = 0LL;
    b = 5LL;
    if (to_bool(a)) {
        print(str("a truthy"));
    } else {
        print(str("a falsy"));
    }
    if (to_bool(b)) {
        print(str("b truthy"));
    } else {
        print(str("b falsy"));
    }
    s1 = str("");
    s2 = str("hello");
    if (to_bool(s1)) {
        print(str("s1 truthy"));
    } else {
        print(str("s1 falsy"));
    }
    if (to_bool(s2)) {
        print(str("s2 truthy"));
    } else {
        print(str("s2 falsy"));
    }
    empty = ptr(new list<_int>());
    full = ptr(new list<_int>({1LL, 2LL, 3LL}));
    if (to_bool(empty)) {
        print(str("empty truthy"));
    } else {
        print(str("empty falsy"));
    }
    if (to_bool(full)) {
        print(str("full truthy"));
    } else {
        print(str("full falsy"));
    }
    print((!to_bool(a)));
    print((!to_bool(b)));
    print(to_bool(a));
    print(to_bool(b));
    print(to_bool(0.0));
    print(to_bool(1.5));
    print(to_bool(true));
    print(to_bool(false));
    n = 3LL;
    // While loop
    while (to_bool(n)) {
        print(n);
        n = (n - 1LL);
    }
    return 0LL;
}
}

namespace prog_tuple {
int run() {
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
}

#include <cstring>

int main(int argc, char** argv) {
    if (argc > 1 && std::strcmp(argv[1], "boolops.py") == 0) return prog_boolops::run();
    if (argc > 1 && std::strcmp(argv[1], "casts.py") == 0) return prog_casts::run();
    if (argc > 1 && std::strcmp(argv[1], "comparison.py") == 0) return prog_comparison::run();
    if (argc > 1 && std::strcmp(argv[1], "dict.py") == 0) return prog_dict::run();
    if (argc > 1 && std::strcmp(argv[1], "exceptions.py") == 0) return prog_exceptions::run();
    if (argc > 1 && std::strcmp(argv[1], "iter.py") == 0) return prog_iter::run();
    if (argc > 1 && std::strcmp(argv[1], "list.py") == 0) return prog_list::run();
    if (argc > 1 && std::strcmp(argv[1], "loops.py") == 0) return prog_loops::run();
    if (argc > 1 && std::strcmp(argv[1], "math.py") == 0) return prog_math::run();
    if (argc > 1 && std::strcmp(argv[1], "membership.py") == 0) return prog_membership::run();
    if (argc > 1 && std::strcmp(argv[1], "print.py") == 0) return prog_print::run();
    if (argc > 1 && std::strcmp(argv[1], "set.py") == 0) return prog_set::run();
    if (argc > 1 && std::strcmp(argv[1], "slice.py") == 0) return prog_slice::run();
    if (argc > 1 && std::strcmp(argv[1], "string.py") == 0) return prog_string::run();
    if (argc > 1 && std::strcmp(argv[1], "truthy.py") == 0) return prog_truthy::run();
    if (argc > 1 && std::strcmp(argv[1], "tuple.py") == 0) return prog_tuple::run();
    return 1;
}

