#include "../../cpp/dict.h"
#include "../../cpp/print.h"
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

void test_setitem_and_getitem() {
    dict<_int, _int> d;
    d[1] = 10;
    d[2] = 20;
    assert_true(d.__len__() == 2, "len after two inserts");
    assert_true(d.__getitem__(1) == 10, "getitem returns stored value");
    d[1] = 11; // overwrite, not append
    assert_true(d.__len__() == 2, "overwriting a key doesn't grow the dict");
    assert_true(d.__getitem__(1) == 11, "overwriting a key replaces the value");
}

void test_getitem_missing_raises() {
    dict<_int, _int> d;
    d[1] = 10;
    try {
        d.__getitem__(99);
        assert_true(false, "getitem on a missing key should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "getitem on a missing key raises KeyError");
    }
}

void test_contains() {
    dict<str, _int> d;
    d["a"] = 1;
    assert_true(d.__contains__("a"), "contains() true for a present key");
    assert_true(!d.__contains__("zz"), "contains() false for an absent key");
}

void test_get_defaults() {
    dict<_int, _int> d;
    d[1] = 10;
    assert_true(d.get(1) == 10, "get(k) returns the value when present");
    assert_true(d.get(99) == 0, "get(k) returns a default V when absent");
    assert_true(d.get(1, 77) == 10, "get(k, default) prefers the stored value");
    assert_true(d.get(99, 77) == 77, "get(k, default) falls back when absent");
    assert_true(d.__len__() == 1, "get() never inserts");
}

void test_pop_defaults() {
    dict<_int, _int> d;
    d[1] = 10;
    d[2] = 20;
    assert_true(d.pop(1) == 10, "pop(k) returns the value");
    assert_true(d.__len__() == 1, "pop(k) removes the entry");
    assert_true(d.pop(99, 77) == 77, "pop(k, default) falls back when absent");
    try {
        d.pop(99);
        assert_true(false, "pop(k) on a missing key should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "pop(k) on a missing key raises KeyError");
    }
}

void test_popitem() {
    dict<_int, _int> d;
    d[1] = 10;
    auto entry = d.popitem();
    assert_true(entry.get<0>() == 1 && entry.get<1>() == 10,
                "popitem() returns the (key, value) pair");
    assert_true(d.__len__() == 0, "popitem() removes the entry");
    try {
        d.popitem();
        assert_true(false, "popitem() on an empty dict should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "popitem() on an empty dict raises KeyError");
    }
}

void test_setdefault() {
    dict<_int, _int> d;
    d[1] = 10;
    assert_true(d.setdefault(1, 77) == 10,
                "setdefault() returns the existing value when present");
    assert_true(d.__len__() == 1, "setdefault() doesn't overwrite a present key");
    assert_true(d.setdefault(2, 77) == 77,
                "setdefault() returns the default when absent");
    assert_true(d.__getitem__(2) == 77, "setdefault() inserts the default");
    assert_true(d.setdefault(3) == 0,
                "setdefault(k) with no default inserts a default V");
    assert_true(d.__len__() == 3, "setdefault() grew the dict twice");
}

void test_delitem() {
    dict<_int, _int> d;
    d[1] = 10;
    d.__delitem__(1);
    assert_true(d.__len__() == 0, "delitem() removes the entry");
    try {
        d.__delitem__(99);
        assert_true(false, "delitem() on a missing key should raise KeyError");
    } catch (const KeyError &) {
        assert_true(true, "delitem() on a missing key raises KeyError");
    }
}

void test_update_and_clear() {
    dict<_int, _int> d;
    d[1] = 10;
    d[2] = 20;
    auto other = ptr(new dict<_int, _int>());
    (*other)[2] = 999; // overlapping key: other wins
    (*other)[3] = 30;
    d.update(other);
    assert_true(d.__len__() == 3, "update() merges in new keys");
    assert_true(d.__getitem__(2) == 999, "update() lets the argument win on overlap");
    assert_true(d.__getitem__(3) == 30, "update() brings across new keys");
    d.clear();
    assert_true(d.__len__() == 0, "clear() empties the dict");
}

void test_keys_values_items() {
    dict<_int, _int> d;
    d[1] = 10;
    d[2] = 20;
    auto keys = d.keys();
    auto values = d.values();
    auto items = d.items();
    assert_true(keys->__len__() == 2, "keys() has one entry per key");
    assert_true(values->__len__() == 2, "values() has one entry per key");
    assert_true(items->__len__() == 2, "items() has one entry per key");
    // Iteration order is unspecified, so check by membership.
    assert_true(keys->__contains__(1) && keys->__contains__(2), "keys() holds every key");
    assert_true(values->__contains__(10) && values->__contains__(20),
                "values() holds every value");
}

void test_copy_is_shallow_but_independent() {
    dict<_int, _int> d;
    d[1] = 10;
    auto c = d.copy();
    c->__setitem__(1, 999);
    c->__setitem__(2, 20);
    assert_true(d.__getitem__(1) == 10, "mutating the copy doesn't affect the original");
    assert_true(d.__len__() == 1, "inserting into the copy doesn't affect the original");
    assert_true(c->__getitem__(1) == 999, "the copy kept its own edit");
}

void test_equality_ignores_insertion_order() {
    dict<_int, _int> a;
    a[1] = 10;
    a[2] = 20;
    dict<_int, _int> b;
    b[2] = 20; // inserted in the opposite order
    b[1] = 10;
    assert_true(a == b, "dicts compare equal regardless of insertion order");
    b[3] = 30;
    assert_true(a != b, "dicts with different keys compare unequal");
}

void test_truthiness() {
    dict<_int, _int> empty;
    dict<_int, _int> full;
    full[1] = 10;
    assert_true(!to_bool(empty), "an empty dict is falsy");
    assert_true(to_bool(full), "a non-empty dict is truthy");
}

void test_iteration_yields_keys() {
    dict<_int, _int> d;
    d[1] = 10;
    d[2] = 20;
    d[3] = 30;
    _int seen = 0;
    _int count = 0;
    for (auto it = py::iter(d); !it.done();) {
        seen += py::next(it); // iterating a dict yields keys, like Python
        count++;
    }
    assert_true(count == 3, "iterating a dict visits every entry once");
    assert_true(seen == 6, "iterating a dict yields keys (1+2+3)");
}

void test_string_keys_and_str() {
    dict<str, _int> d;
    d["a"] = 1;
    assert_true(d.__getitem__("a") == 1, "string keys work");
    assert_true(to_str(d) == "{'a': 1}",
                "str() quotes string keys via repr(), like Python");
}

void test_tuple_keys() {
    dict<tuple<_int, _int>, str> d;
    d[tuple<_int, _int>(1, 2)] = "a";
    assert_true(d.__contains__(tuple<_int, _int>(1, 2)),
                "tuples work as dict keys (hashable)");
    assert_true(!d.__contains__(tuple<_int, _int>(2, 1)),
                "tuple key hashing is order-sensitive");
    assert_true(d.__getitem__(tuple<_int, _int>(1, 2)) == "a",
                "tuple keys round-trip to their value");
}

int main() {
    test_setitem_and_getitem();
    test_getitem_missing_raises();
    test_contains();
    test_get_defaults();
    test_pop_defaults();
    test_popitem();
    test_setdefault();
    test_delitem();
    test_update_and_clear();
    test_keys_values_items();
    test_copy_is_shallow_but_independent();
    test_equality_ignores_insertion_order();
    test_truthiness();
    test_iteration_yields_keys();
    test_string_keys_and_str();
    test_tuple_keys();
    std::cout << "\nAll tests passed!\n";
    return 0;
}
