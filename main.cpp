#include <iostream>
#include "print.h"
#include "list.h"
#include "ptr.h"
#include "range.h"
using namespace py;


int main();

int main() {
    int x;
    ptr<list<int>> l;
    int i;
    int step;
    int n;

    x = 2;
    l = ptr(new list<int>({2, 3, 4}));
    for (size_t i = 0; i < len(l); ++i) {
        print(l);
    }
    for (int i = 0; i < x; ++i) {
        print("first", i);
    }
    for (int i = x; i < (x + 5); ++i) {
        print("second", i);
    }
    for (int i = x; i < (x + 10); i += 2) {
        print("third", i);
    }
    for (int i = x; i > (x - 7); i += -2) {
        print("fourth", i);
    }
    step = x;
    for (int i = x;; i += step) {
        if ((step > 0 && i >= (10 * x)) || (step < 0 && i <= (10 * x))) break;
        print("fifth", i);
    }
    step = (-2);
    for (int i = (5 * x);; i += step) {
        if ((step > 0 && i >= (10 * x)) || (step < 0 && i <= (10 * x))) break;
        print("sixth", i);
    }
    for (auto n__iter = iter(l); !n__iter.done();) {
        n = next(n__iter);
        print("seventh", n);
    }
    return 0;
}

