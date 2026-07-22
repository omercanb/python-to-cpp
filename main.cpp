#include "types.h"
#include "truthy.h"
#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "dict.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    _int a;
    print(pow(10LL, 10LL));
    print(idiv(-10LL, 3LL));
    print(idiv(10LL, 3LL));
    print(fdiv(5LL, 2LL));
    print(pow(0.5, 4LL));
    print((50.0 * 100LL));
    a = pow(10LL, 10LL);
    return a;
}
