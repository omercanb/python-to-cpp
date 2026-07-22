#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
#include "scalars.h"
#include "mathops.h"
using namespace py;
int main() {
    int a;
    print(pow(10, 10));
    print(idiv(-10, 3));
    print(idiv(10, 3));
    print(fdiv(5, 2));
    print(pow(0.5, 4));
    print((50.0 * 100));
    a = pow(10, 10);
    return a;
}
