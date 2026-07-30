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
str("Simple, brute-force N-Queens solver.");
void generate_permutations(ptr<list<_int>> values, _int start, ptr<list<ptr<list<_int>>>> result) {
    _int n;
    _int i;
    _int tmp;
    str("Fill `result` with every permutation of `values`, built eagerly.");
    n = len(values);
    if (to_bool(((start == n)))) {
        result->append(ptr(new list<_int>(values)));
        return;
    }
    for (_int i = start; i < n; ++i) {
        tmp = values->__getitem__(start);
        values->__setitem__(start, values->__getitem__(i));
        values->__setitem__(i, tmp);
        generate_permutations(values, (start + 1LL), result);
        tmp = values->__getitem__(start);
        values->__setitem__(start, values->__getitem__(i));
        values->__setitem__(i, tmp);
    }
}

ptr<list<ptr<list<_int>>>> permutations(_int n) {
    ptr<list<ptr<list<_int>>>> result;
    str("All permutations of range(n), as a list built up front instead of lazily.");
    result = ptr(new list<ptr<list<_int>>>());
    generate_permutations(ptr(new list<_int>(range(n))), 0LL, result);
    return result;
}

ptr<set<_int>> comprehension_1(ptr<range> cols, ptr<list<_int>> vec) {
    ptr<set<_int>> __result_2 = ptr(new set<_int>());
    _int i;
    for (auto __iter_3 = iter(cols); !__iter_3.done();) {
        i = next(__iter_3);
        __result_2->add((vec->__getitem__(i) + i));
    }
    return __result_2;
}

ptr<set<_int>> comprehension_4(ptr<range> cols, ptr<list<_int>> vec) {
    ptr<set<_int>> __result_5 = ptr(new set<_int>());
    _int i;
    for (auto __iter_6 = iter(cols); !__iter_6.done();) {
        i = next(__iter_6);
        __result_5->add((vec->__getitem__(i) - i));
    }
    return __result_5;
}

ptr<list<ptr<list<_int>>>> do_n_queens(_int queen_count) {
    ptr<range> cols;
    ptr<list<ptr<list<_int>>>> solutions;
    ptr<list<_int>> vec;
    str("N-Queens solver.\n\n    Args:\n        queen_count: the number of queens to solve for. This is also the\n            board size.\n\n    Returns:\n        Solutions to the problem. Each returned value looks like\n        [3, 8, 2, 1, 4, ..., 6] where each number is the column position for the\n        queen, and the index into the list indicates the row.\n    ");
    cols = range(queen_count);
    solutions = ptr(new list<ptr<list<_int>>>());
    for (auto __iter_7 = iter(permutations(queen_count)); !__iter_7.done();) {
        vec = next(__iter_7);
        if (to_bool(((queen_count == len(comprehension_1(cols, vec))) && (len(comprehension_1(cols, vec)) == len(comprehension_4(cols, vec)))))) {
            solutions->append(vec);
        }
    }
    return solutions;
}

void bench_n_queens(_int queen_count) {
    do_n_queens(queen_count);
}

void nqueens() {
    _int queen_count;
    _int i;
    queen_count = 8LL;
    for (_int i = 0; i < 3LL; ++i) {
        bench_n_queens(queen_count);
    }
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        nqueens(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    