#pragma once
#include "str.h"
#include "list.h"
#include "ptr.h"
#include "range.h"

#include <iostream>
#include <string>

namespace py {

// ---- print implementation ----

// Internal implementation - takes sep, end, and variadic args explicitly
// Called by transpiler when kwargs are present
template <class... Args>
void _print_kwargs(const std::string &sep, const std::string &end, Args... args) {
    std::string result;
    bool first = true;

    // Fold expression: for each arg, add separator if not first, then the arg
    (([&] {
        if (!first)
            result += sep;
        result += str(args);
        first = false;
    }()),
     ...);

    std::cout << result << end;
}

// Overload for no arguments with kwargs
void _print_kwargs(const std::string &sep, const std::string &end) {
    std::cout << end;
}

// Public API - no kwargs, uses default sep and end
template <class... Args>
void print(Args... args) {
    _print_kwargs(" ", "\n", args...);
}

// Public API - no arguments
void print() {
    _print_kwargs(" ", "\n");
}

} // namespace py
