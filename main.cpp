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
int main() {
    ptr<list<bool>> a;
    a = ptr(new list<bool>());
    a->append(true);
    a->append(false);
    print(a->__getitem__(0LL));
    a->__setitem__(0LL, false);
    print(a->__getitem__(0LL));
    return 0LL;
}
