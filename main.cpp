#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
using namespace py;
int main() {
    ptr<list<int>> nums;
    ptr<list<int>> a;
    nums = ptr(new list<int>({1, 2, 3, 4, 5}));
    a = ptr(new list(map([=](auto x) { return (x * 2); }, nums)));
    print(a);
    return 0;
}
