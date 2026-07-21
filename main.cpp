#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
using namespace py;
int main() {
    ptr<list<int>> nums;
    ptr<list<int>> a;
    std::string s;
    ptr<list<int>> filtered;
    int x;
    int y;
    int i;
    int n;
    nums = ptr(new list<int>({1, 2, 3, 4, 5}));
    a = ptr(new list(map([](auto x) { return (x * 2); }, nums)));
    print(a);
    for (auto __iter = iter(map([](auto x) { return str(x); }, nums)); !__iter.done();) {
        s = next(__iter);
        print(s);
    }
    filtered = ptr(new list(filter([](auto x) { return (x % 2) == 0; }, nums)));
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
    return 0;
}
