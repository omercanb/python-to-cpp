#include "../../cpp/list.h"
#include "../../cpp/print.h"
#include "../../cpp/truthy.h"
#include <cassert>
#include <iostream>
#include <vector>
using namespace py;

// Test utilities
void assert_true(bool condition, const std::string &test_name) {
    if (!condition) {
        std::cerr << "FAIL: " << test_name << "\n";
        exit(1);
    }
    std::cout << "PASS: " << test_name << "\n";
}

// pop() with no argument should remove and return the LAST element,
// matching Python's list.pop(). list<T>::size_type is an unsigned size_t,
// so the default argument -1 wraps to SIZE_MAX before pop()'s `i < 0`
// from-the-end check ever runs (that check can never be true on an
// unsigned type) - so this currently throws IndexError instead of
// popping the last element.
void test_pop_default_removes_last() {
    list<int> l;
    l.append(1);
    l.append(2);
    l.append(3);
    l.append(4);
    try {
        int popped = l.pop();
        assert_true(popped == 4, "pop() with no args returns last element (4)");
        assert_true(l.len() == 3, "pop() with no args shrinks list by one");
    } catch (const std::exception &e) {
        assert_true(false, std::string("pop() with no args threw: ") + e.what());
    }
}

// Same bug via an explicit negative index.
void test_pop_negative_index() {
    list<int> l;
    l.append(10);
    l.append(20);
    l.append(30);
    try {
        int popped = l.pop(-1);
        assert_true(popped == 30, "pop(-1) returns last element (30)");
        assert_true(l.len() == 2, "pop(-1) shrinks list by one");
    } catch (const std::exception &e) {
        assert_true(false, std::string("pop(-1) threw: ") + e.what());
    }
}

// Positive indices don't hit the unsigned-wraparound bug.
void test_pop_positive_index_still_works() {
    list<int> l;
    l.append(10);
    l.append(20);
    l.append(30);
    int popped = l.pop(1);
    assert_true(popped == 20, "pop(1) returns middle element (20)");
    assert_true(l.len() == 2, "pop(1) shrinks list by one");
    assert_true(l[0] == 10 && l[1] == 30,
                "pop(1) leaves remaining elements in order");
}

// Reproduces the exact pattern from input.py: `while l: ... l.pop()`
void test_pop_loop_drains_list() {
    list<int> l;
    l.append(1);
    l.append(2);
    l.append(3);
    l.append(4);

    std::vector<int> popped_values;
    try {
        while (to_bool(l)) {
            popped_values.push_back(l.pop());
        }
    } catch (const std::exception &e) {
        assert_true(false, std::string("while(l) pop-loop threw: ") + e.what());
        return;
    }
    assert_true(popped_values.size() == 4, "pop-loop pops exactly 4 elements");
    std::vector<int> expected = {4, 3, 2, 1};
    assert_true(popped_values == expected,
                "pop-loop pops elements in reverse order (Python semantics)");
}

// insert() has the same unsigned-index bug for negative positions.
void test_insert_negative_index() {
    list<int> l;
    l.append(1);
    l.append(2);
    l.append(3);
    try {
        l.insert(-1, 99); // Python: [1, 2, 3].insert(-1, 99) -> [1, 2, 99, 3]
        assert_true(l.len() == 4, "insert(-1, x) grows list by one");
        assert_true(l[2] == 99, "insert(-1, x) places element one before the end");
    } catch (const std::exception &e) {
        assert_true(false, std::string("insert(-1, x) threw: ") + e.what());
    }
}

// Positive indices don't hit the unsigned-wraparound bug.
void test_insert_positive_index_still_works() {
    list<int> l;
    l.append(1);
    l.append(2);
    l.append(3);
    l.insert(1, 99);
    assert_true(l.len() == 4, "insert(1, x) grows list by one");
    assert_true(l[1] == 99, "insert(1, x) places element at index 1");
}

// operator[] happens to round-trip negative indices correctly today (it
// forwards to normIndex(long long), unlike pop()/insert() which branch on
// the unsigned size_type directly) - included as a reference point showing
// the bug isn't uniform across the list API.
void test_negative_indexing_read() {
    list<int> l;
    l.append(1);
    l.append(2);
    l.append(3);
    assert_true(l[-1] == 3, "l[-1] reads the last element");
    assert_true(l[-2] == 2, "l[-2] reads the second-to-last element");
}

int main() {
    test_pop_default_removes_last();
    test_pop_negative_index();
    test_pop_positive_index_still_works();
    test_pop_loop_drains_list();
    test_insert_negative_index();
    test_insert_positive_index_still_works();
    test_negative_indexing_read();
    std::cout << "\nAll tests passed!\n";
    return 0;
}
