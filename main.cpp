#include "types.h"
#include "exceptions.h"
#include "finally.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "slice.h"
#include "list.h"
#include "strops.h"
#include "dict.h"
#include "set.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
#include "builtins.h"
using namespace py;
_int num() {
    return 0LL;
}

int main() {
    ptr<list<_int>> l;
    ptr<list<_int>> a;
    l = ptr(new list<_int>({1LL, 2LL, 3LL, 4LL}));
    a = ptr(new list<_int>(map([](auto x) { return (2LL * x); }, l)));
    return 0LL;
}
