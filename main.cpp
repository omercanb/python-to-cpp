#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    ptr<list<_int>> l;
    l = ptr(new list<_int>({1LL, 2LL, 3LL, 4LL}));
    // While loop
    while (to_bool(l)) {
        print(1LL);
        print(l);
        print(l->pop());
        print("l: ", l);
    }
    return 0LL;
}
