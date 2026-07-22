#include "types.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
ptr<list<_int>> get_list() {
    return ptr(new list<_int>({1LL, 2LL, 3LL, 4LL, 5LL}));
}

int main() {
    ptr<list<_int>> l;
    _int n;
    ptr<list<std::string>> l2;
    ptr<list<_int>> l3;
    l = get_list();
    for (auto __iter = iter(l); !__iter.done();) {
        n = next(__iter);
        print(n);
    }
    l2 = ptr(new list<std::string>({"a", "b", "c"}));
    l2 = ptr(new list<std::string>({"a", "a", "a"}));
    l3 = ptr(new list(ptr(new list<_int>({0LL, 1LL, 0LL, 1LL}))));
    return 0LL;
}
