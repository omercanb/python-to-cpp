#include <iostream>
#include <cassert>
#include "../../cpp/print.h"
#include "../../cpp/tuple.h"
using namespace py;

// Test utilities
void assert_true(bool condition, const std::string& test_name) {
    if (!condition) {
        std::cerr << "FAIL: " << test_name << "\n";
        exit(1);
    }
    std::cout << "PASS: " << test_name << "\n";
}

// Test implementations
void test_tuple_construction() {
    tuple<int, int> t(42, 99);
    assert_true(t.get<0>() == 42, "tuple construction first");
    assert_true(t.get<1>() == 99, "tuple construction second");
    assert_true(true, "test_tuple_construction");
}

void test_tuple_length() {
    tuple<int, int> t(1, 2);
    assert_true(t.__len__() == 2, "tuple length");
    assert_true(true, "test_tuple_length");
}

void test_tuple_mixed_types() {
    tuple<int, std::string> t(5, "hello");
    assert_true(t.get<0>() == 5, "mixed tuple int");
    assert_true(t.get<1>() == "hello", "mixed tuple string");
    assert_true(true, "test_tuple_mixed_types");
}

void test_tuple_default_construction() {
    tuple<int, int> t;
    assert_true(t.get<0>() == 0, "default tuple first");
    assert_true(t.get<1>() == 0, "default tuple second");
    assert_true(true, "test_tuple_default_construction");
}

void test_tuple_destructuring() {
    int a, b;
    destructure(a, b) = tuple<int, int>(100, 200);
    assert_true(a == 100, "destructure first");
    assert_true(b == 200, "destructure second");
    assert_true(true, "test_tuple_destructuring");
}

void test_tuple_destructuring_reassign() {
    int x = 0, y = 0;
    destructure(x, y) = tuple<int, int>(10, 20);
    assert_true(x == 10, "destructure reassign first");
    assert_true(y == 20, "destructure reassign second");

    // Reassign again
    destructure(x, y) = tuple<int, int>(30, 40);
    assert_true(x == 30, "destructure reassign again first");
    assert_true(y == 40, "destructure reassign again second");
    assert_true(true, "test_tuple_destructuring_reassign");
}

void test_tuple_destructuring_mixed_types() {
    int num;
    std::string str;
    destructure(num, str) = tuple<int, std::string>(42, "world");
    assert_true(num == 42, "destructure mixed int");
    assert_true(str == "world", "destructure mixed string");
    assert_true(true, "test_tuple_destructuring_mixed_types");
}

void test_tuple_assignment() {
    tuple<int, int> t1(1, 2);
    tuple<int, int> t2(10, 20);
    t1 = t2;
    assert_true(t1.get<0>() == 10, "assignment first");
    assert_true(t1.get<1>() == 20, "assignment second");
    assert_true(true, "test_tuple_assignment");
}

int main() {
    test_tuple_construction();
    test_tuple_length();
    test_tuple_mixed_types();
    test_tuple_default_construction();
    test_tuple_destructuring();
    test_tuple_destructuring_reassign();
    test_tuple_destructuring_mixed_types();
    test_tuple_assignment();
    std::cout << "\nAll tests passed!\n";
    return 0;
}
