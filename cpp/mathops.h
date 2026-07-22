#pragma once

#include <cmath>

namespace py {

inline double pow(double base, int exp) { return std::pow(base, exp); }
inline double pow(double base, double exp) { return std::pow(base, exp); }
inline int pow(int base, int exp) {
    return static_cast<int>(pow(static_cast<double>(base), exp));
}

// Python and C++ modulo differ slightly for negative numerators
inline int mod(int a, int b) {
    int r = a % b;
    return (r != 0 && (r ^ b) < 0) ? r + b : r;
}

inline double fdiv(double a, double b) { return a / b; }
inline double fdiv(int a, double b) { return static_cast<double>(a) / b; }
inline double fdiv(double a, int b) { return a / static_cast<double>(b); }
inline double fdiv(int a, int b) { return static_cast<double>(a) / b; }
// Pythons '//' division that rounds to negative infinity
inline int idiv(int a, int b) { return a >= 0 ? a / b : -1 - (-1 - a) / b; }

} // namespace py
