#include "iter.h"
#include "tuple.h"
#include "ptr.h"
#include "list.h"
#include "print.h"
#include "scalars.h"
using namespace py;
int main() {
    double a;
    int b;
    double c;
    std::string float_str;
    double f1;
    std::string int_str;
    int i1;
    int i2;
    a = 2.0;
    b = _int(a);
    c = _float(b);
    float_str = "  0.10 ";
    f1 = _float(float_str);
    int_str = "100";
    i1 = _int(int_str);
    i2 = _int(int_str, 2);
    print(a, b, c, f1, i1, i2);
    return 0;
}
