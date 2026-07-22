#include "../../cpp/set.h"
#include "../../cpp/truthy.h"
#include <iostream>
#include <string>
using namespace py;

void assert_true(bool condition, const std::string &test_name) {
    if (!condition) {
        std::cerr << "FAIL: " << test_name << "\n";
        exit(1);
    }
    std::cout << "PASS: " << test_name << "\n";
}

static ptr<set<_int>> make(std::initializer_list<_int> values) {
    return ptr(new set<_int>(values));
}

void test_add_dedupes() {
    set<_int> s;
    s.add(1);
    s.add(2);
    s.add(1); // duplicate
    assert_true(s.__len__() == 2, "add() ignores duplicates");
    assert_true(s.__contains__(1) && s.__contains__(2), "add() stores elements");
    assert_true(!s.__contains__(99), "contains() is false for an absent element");
}

void test_remove_vs_discard() {
    set<_int> s;
    s.add(1);
    s.remove(1);
    assert_true(s.__len__() == 0, "remove() deletes the element");
    try {
        s.remove(99);
        assert_true(false, "remove() on a missing element should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "remove() on a missing element raises KeyError");
    }
    s.discard(99); // must not raise
    assert_true(true, "discard() on a missing element does not raise");
}

void test_pop() {
    set<_int> s;
    s.add(7);
    assert_true(s.pop() == 7, "pop() returns the only element");
    assert_true(s.__len__() == 0, "pop() removes the element");
    try {
        s.pop();
        assert_true(false, "pop() on an empty set should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "pop() on an empty set raises KeyError");
    }
}

void test_non_mutating_operations() {
    auto a = make({1, 2, 3});
    auto b = make({3, 4});

    assert_true(*a->union_(b) == *make({1, 2, 3, 4}), "union()");
    assert_true(*a->intersection(b) == *make({3}), "intersection()");
    assert_true(*a->difference(b) == *make({1, 2}), "difference()");
    assert_true(*a->symmetric_difference(b) == *make({1, 2, 4}),
                "symmetric_difference()");
    // None of the above may modify their operands.
    assert_true(*a == *make({1, 2, 3}) && *b == *make({3, 4}),
                "set operations leave both operands untouched");
}

void test_operators_match_methods() {
    auto a = make({1, 2, 3});
    auto b = make({3, 4});
    assert_true(*(a | b) == *a->union_(b), "| matches union()");
    assert_true(*(a & b) == *a->intersection(b), "& matches intersection()");
    assert_true(*(a - b) == *a->difference(b), "- matches difference()");
    assert_true(*(a ^ b) == *a->symmetric_difference(b),
                "^ matches symmetric_difference()");
}

void test_mutating_updates() {
    auto a = make({1, 2, 3});
    a->update(make({4}));
    assert_true(*a == *make({1, 2, 3, 4}), "update()");

    a = make({1, 2, 3});
    a->intersection_update(make({2, 3, 9}));
    assert_true(*a == *make({2, 3}), "intersection_update()");

    a = make({1, 2, 3});
    a->difference_update(make({1, 9}));
    assert_true(*a == *make({2, 3}), "difference_update()");

    a = make({1, 2, 3});
    a->symmetric_difference_update(make({3, 4}));
    assert_true(*a == *make({1, 2, 4}), "symmetric_difference_update()");
}

void test_predicates() {
    auto small = make({1, 2});
    auto big = make({1, 2, 3});
    auto other = make({9});

    assert_true(small->issubset(big), "issubset() true for a strict subset");
    assert_true(small->issubset(small), "issubset() true for an equal set");
    assert_true(!big->issubset(small), "issubset() false for a superset");
    assert_true(big->issuperset(small), "issuperset()");
    assert_true(small->isdisjoint(other), "isdisjoint() true when nothing overlaps");
    assert_true(!small->isdisjoint(big), "isdisjoint() false when they overlap");
}

void test_comparison_operators() {
    auto small = make({1, 2});
    auto big = make({1, 2, 3});

    assert_true(small <= big && small < big, "<= and < for a proper subset");
    assert_true(small <= make({1, 2}), "<= is true for an equal set");
    assert_true(!(small < make({1, 2})), "< is false for an equal set");
    assert_true(big >= small && big > small, ">= and > for a proper superset");
    assert_true(make({1, 2}) == make({2, 1}), "== ignores insertion order");
    assert_true(small != big, "!= for differing sets");

    // Subset ordering is partial: neither of these contains the other.
    auto left = make({1});
    auto right = make({2});
    assert_true(!(left < right) && !(right < left) && left != right,
                "disjoint sets are unordered but unequal");
}

void test_truthiness_and_len() {
    set<_int> empty;
    auto full = make({1});
    assert_true(!to_bool(empty), "an empty set is falsy");
    assert_true(to_bool(*full), "a non-empty set is truthy");
    assert_true(len(*full) == 1, "len()");
}

void test_iteration() {
    auto s = make({1, 2, 3});
    _int total = 0;
    _int count = 0;
    for (auto it = py::iter(*s); !it.done();) {
        total += py::next(it);
        count++;
    }
    assert_true(count == 3, "iteration visits every element once");
    assert_true(total == 6, "iteration yields the elements (1+2+3)");
}

void test_sorted_gives_stable_order() {
    auto s = make({3, 1, 2});
    auto asc = sorted(s);
    assert_true(asc->__getitem__(0) == 1 && asc->__getitem__(2) == 3,
                "sorted() returns elements in ascending order");
    auto desc = _sorted_kwargs(true, s);
    assert_true(desc->__getitem__(0) == 3 && desc->__getitem__(2) == 1,
                "sorted(reverse=True) returns descending order");
}

void test_str_and_string_elements() {
    set<_int> empty;
    assert_true(to_str(empty) == "set()", "an empty set prints as set(), not {}");
    set<str> s;
    s.add("a");
    assert_true(to_str(s) == "{'a'}", "str() quotes string elements via repr()");
}

void test_copy_is_independent() {
    auto a = make({1, 2});
    auto c = a->copy();
    c->add(3);
    assert_true(*a == *make({1, 2}), "mutating a copy leaves the original alone");
    assert_true(c->__len__() == 3, "the copy kept its own edit");
}

int main() {
    test_add_dedupes();
    test_remove_vs_discard();
    test_pop();
    test_non_mutating_operations();
    test_operators_match_methods();
    test_mutating_updates();
    test_predicates();
    test_comparison_operators();
    test_truthiness_and_len();
    test_iteration();
    test_sorted_gives_stable_order();
    test_str_and_string_elements();
    test_copy_is_independent();
    std::cout << "\nAll tests passed!\n";
    return 0;
}
