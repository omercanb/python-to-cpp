#include <iostream>
#include "print.h"
#include "list.h"
#include "ptr.h"
#include "range.h"
using namespace py;


int main();

int main() {
    int i;
    int j;

    for (auto i__iter = iter(range(10)); !i__iter.done();) {
        i = next(i__iter);
        print();
        for (auto j__iter = iter(range(10)); !j__iter.done();) {
            j = next(j__iter);
            if (i == j) {
                print("(((((", i, j, ")))))");
            } else {
                print("    (", i, j, ")");
            }
        }
        print();
    }
    return 0;
}

