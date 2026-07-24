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
using namespace py;
_int num() {
    return 0LL;
}

int main() {
    _int step;
    bool __thrown_1 = false;
    try {
        to_int(str("no"));
    } catch (PyException &e) {
        __thrown_1 = true;
        print(e);
    }
    if (!__thrown_1) {
        print(str("yes"));
    }
    bool __thrown_2 = false;
    try {
        to_int(str("no"));
    } catch (PyException &e) {
        __thrown_2 = true;
        print(e);
    }
    if (!__thrown_2) {
        print(str("yes"));
    }
    step = 2LL;
    return 0LL;
}
