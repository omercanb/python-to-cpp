#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "strops.h"
#include "dict.h"
#include "set.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    _int a;
    _float b;
    a = 3LL;
    b = fdiv(a, 2LL);
    return 0LL;
}
