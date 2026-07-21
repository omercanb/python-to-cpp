#include "list.h"
#include "ptr.h"
#include "print.h"
#include "tuple.h"
#include "iter.h"
using namespace py;
int main() {
    ptr<list<int>> nums;
    ptr<list<int>> nums2;
    int n;
    nums = ptr(new list({1, 2, 3, 4, 5}));
    nums2 = ptr(new list({2}));
    for (auto __iter = iter(map([=](auto x) { return (2 * x); }, nums)); !__iter.done();) {
        n = next(__iter);
        nums2->append(n);
    }
    print(nums);
    print(nums2);
    return 0;
}
