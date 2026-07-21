#include <iostream>
#include "../cpp/tuple.h"
#include "../cpp/print.h"
using namespace py;

int main() {
    // Test 1: Create and access tuple
    tuple<int, int> t1(42, 99);
    print("Tuple (42, 99):", t1);

    // Test 2: Access elements
    print("First element:", t1.get<0>());
    print("Second element:", t1.get<1>());

    // Test 3: Length
    print("Length of tuple:", t1.__len__());

    // Test 4: Tuple with different types
    tuple<int, std::string> t2(5, "hello");
    print("Mixed tuple:", t2);

    // Test 5: Default constructor
    tuple<int, int> t3;
    print("Default tuple:", t3);

    // Test 6: Destructuring with destructure(a, b) = tuple
    int a, b;
    destructure(a, b) = tuple<int, int>(100, 200);
    print("Destructured values - a:", a, "b:", b);

    // Test 7: Destructuring with different types
    int x;
    std::string s;
    destructure(x, s) = tuple<int, std::string>(42, "world");
    print("Mixed destructure - x:", x, "s:", s);

    return 0;
}
