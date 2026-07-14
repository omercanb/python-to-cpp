#pragma once
#include "list.h"
#include "ptr.h"

#include <iostream>
#include <ostream>

namespace py {
template <typename First, typename... Rest>
void print(First &&first, Rest &&...rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) {
        ((std::cout << " " << rest), ...);
    }
    std::cout << "\n";
}
void print() { std::cout << "\n"; }

template <typename T>
std::ostream &operator<<(std::ostream &os, const ptr<T> &p) {
    os << *p;
    return os;
}

template <typename T>
std::ostream &operator<<(std::ostream &os, const list<T> &l) {
    os << "[";
    for (size_t i = 0; i < l.size() - 1; ++i) {
        os << l[i] << ", ";
    }
    os << l[l.size() - 1] << "]";
    return os;
}
} // namespace py
