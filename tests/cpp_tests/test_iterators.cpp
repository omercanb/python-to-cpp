#include "../../cpp/list.h"
#include "../../cpp/print.h"
#include <cassert>
#include <iostream>
using namespace py;

// Test utilities
void assert_true(bool condition, const std::string &test_name) {
    if (!condition) {
        std::cerr << "FAIL: " << test_name << "\n";
        exit(1);
    }
    std::cout << "PASS: " << test_name << "\n";
}

// Test implementations
void test_enumerate() {
    list<int> nums;
    nums.append(10);
    nums.append(20);
    nums.append(30);

    auto e = enumerate(nums);
    assert_true(!e.done(), "enumerate not done");

    auto t = e.current();
    assert_true(t.get<0>() == 0, "enumerate index 0");
    assert_true(t.get<1>() == 10, "enumerate value 10");
    assert_true(true, "test_enumerate");
}

void test_enumerate_loop() {
    list<int> nums;
    nums.append(10);
    nums.append(20);
    nums.append(30);

    auto e = enumerate(nums);
    int expected_indices[] = {0, 1, 2};
    int expected_values[] = {10, 20, 30};
    int count = 0;

    while (!e.done()) {
        auto t = e.current();
        assert_true(t.get<0>() == expected_indices[count],
                    "enumerate loop index");
        assert_true(t.get<1>() == expected_values[count],
                    "enumerate loop value");
        e.next();
        count++;
    }
    assert_true(count == 3, "enumerate loop iterated 3 times");
    assert_true(true, "test_enumerate_loop");
}

void test_zip() {
    list<int> nums;
    nums.append(1);
    nums.append(2);

    list<std::string> strs;
    strs.append("a");
    strs.append("b");

    auto z = zip(nums, strs);
    assert_true(!z.done(), "zip not done");

    auto t = z.current();
    assert_true(t.get<0>() == 1, "zip first element 1");
    assert_true(t.get<1>() == "a", "zip second element a");
    assert_true(true, "test_zip");
}

void test_map() {
    list<int> nums;
    nums.append(1);
    nums.append(2);
    nums.append(3);

    auto double_val = [](int x) { return x * 2; };
    auto m = map(double_val, nums);

    assert_true(!m.done(), "map not done");
    int val = m.current();
    assert_true(val == 2, "map first doubled value 2");
    assert_true(true, "test_map");
}

void test_filter() {
    list<int> nums;
    nums.append(1);
    nums.append(2);
    nums.append(3);
    nums.append(4);

    auto is_even = [](int x) { return x % 2 == 0; };
    auto f = filter(is_even, nums);

    assert_true(!f.done(), "filter not done at start");
    int val = f.current();
    assert_true(val == 2, "filter first even value 2");
    assert_true(true, "test_filter");
}

void test_filter_loop() {
    list<int> nums;
    nums.append(1);
    nums.append(2);
    nums.append(3);
    nums.append(4);
    nums.append(5);
    nums.append(6);

    auto is_even = [](int x) { return x % 2 == 0; };
    auto f = filter(is_even, nums);

    int expected[] = {2, 4, 6};
    int count = 0;

    while (!f.done()) {
        int val = f.current();
        assert_true(val == expected[count], "filter loop value");
        f.next();
        count++;
    }
    assert_true(count == 3, "filter loop iterated 3 times");
    assert_true(f.done(), "filter done after iteration");
    assert_true(true, "test_filter_loop");
}

void test_enumerate_for_loop_pattern() {
    list<int> nums;
    nums.append(10);
    nums.append(20);
    nums.append(30);

    int expected_indices[] = {0, 1, 2};
    int expected_values[] = {10, 20, 30};
    int count = 0;

    // This is the pattern the transpiler generates:
    // for (auto __iter = iter(enumerate(nums)); !__iter.done();) {
    //     destructure(i, n) = next(__iter);
    //     ...
    // }
    for (auto __iter = py::iter(py::enumerate(nums)); !__iter.done();) {
        int i, n;
        py::destructure(i, n) = py::next(__iter);
        assert_true(i == expected_indices[count], "enumerate for loop index");
        assert_true(n == expected_values[count], "enumerate for loop value");
        count++;
    }
    assert_true(count == 3, "enumerate for loop iterated 3 times");
    assert_true(true, "test_enumerate_for_loop_pattern");
}

int main() {
    test_enumerate();
    test_enumerate_loop();
    test_zip();
    test_map();
    test_filter();
    test_filter_loop();
    test_enumerate_for_loop_pattern();
    std::cout << "\nAll tests passed!\n";
    return 0;
}
