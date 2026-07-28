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
str("Binary trees benchmark.\n\nAdapted from the Computer Language Benchmarks Game:\nhttps://benchmarksgame-team.pages.debian.net/benchmarksgame/performance/binarytrees.html\n");
class Tree {
  public:
    std::optional<Tree> left;
    std::optional<Tree> right;

    Tree(_int depth) { __init__(depth); }

    void __init__(_int depth) {
        if (to_bool(((depth == 0LL)))) {
            this->left = None;
            this->right = None;
        } else {
            this->left = ptr(new Tree((depth - 1LL)));
            this->right = ptr(new Tree((depth - 1LL)));
        }
    }

    _int check() {
        if (to_bool(((this->left is not None)))) {
            return ((1LL + this->left->check()) + this->right->check());
        } else {
            return 1LL;
        }
    }

};

void binary_trees() {
    _int min_depth;
    _int max_depth;
    _int stretch_depth;
    ptr<Tree> long_lived_tree;
    _int d;
    auto iterations;
    _int check;
    _int i;
    min_depth = 4LL;
    max_depth = 10LL;
    stretch_depth = (max_depth + 1LL);
    print(str("stretch tree of depth {} check: {}").format(stretch_depth, ptr(new Tree(stretch_depth))->check()));
    long_lived_tree = ptr(new Tree(max_depth));
    for (_int d = min_depth; d < stretch_depth; d += 2) {
        iterations = pow(2LL, ((max_depth + min_depth) - d));
        check = 0LL;
        for (_int i = 1LL; i < (iterations + 1LL); ++i) {
        }
        print(str("{} trees of depth {} check: {}").format(iterations, d, check));
    }
    print(str("long lived tree of depth {} check: {}").format(max_depth, long_lived_tree->check()));
}


    int main() {
        auto t0 = std::chrono::steady_clock::now();
        binary_trees(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\n';
        return 0;
    }
    