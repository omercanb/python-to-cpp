#include <chrono>
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
void catch_exceptions() {
    _int n;
    _int i;
    n = 0LL;
    _int __stop_1 = (100LL * 1000LL);
    for (i = 0; i < __stop_1; ++i) {
        try {
            f(i);
        } catch (ValueError &) {
        }
    }
}

void f(_int i) {
    if (to_bool(((mod(i, 4LL) == 0LL)))) {
        throw ValueError(str("problem"));
    } else {
        g(i);
    }
}

void g(_int i) {
    if (to_bool(((mod(i, 7LL) == 0LL)))) {
        throw ValueError("");
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        catch_exceptions(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    