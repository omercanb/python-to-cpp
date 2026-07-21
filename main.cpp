#include "list.h"
#include "ptr.h"
#include "print.h"
#include "tuple.h"
using namespace py;
int main() {
    int a;
    int b;
    int x;
    std::string s;
    int p;
    int q;
    int m;
    int n;
    tuple<int, int> t;
    tuple<int, int> t2;
    destructure(a, b) = tuple(1, 2);
    print("Test 1 - Simple destructure:", a, b);
    destructure(a, b) = tuple(10, 20);
    print("Test 2 - Reassign:", a, b);
    destructure(x, s) = tuple(42, "hello");
    print("Test 3 - Mixed types:", x, s);
    destructure(p, q) = tuple(100, 200);
    destructure(m, n) = tuple(p, q);
    print("Test 4 - Chained destructure:", m, n);
    t = tuple(1, 2);
    t2 = t;
    return 0;
}
