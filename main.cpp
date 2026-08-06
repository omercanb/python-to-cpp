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
#include "file.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
#include "builtins.h"
using namespace py;
int main();
void __init_module__();

void __init_module__() {
}

int main() {
    _int x;
    ptr<list<_int>> a;
    __init_module__();
    x = 10LL;
    a = ptr(new list<_int>());
    _int __stop_0 = x;
    for (x = 0; x < __stop_0; ++x) {
        a->append(x);
    }
    a->sort([](auto x) { return ((x < 5LL)); });
    return 0LL;
}
