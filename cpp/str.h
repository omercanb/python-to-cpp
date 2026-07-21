#pragma once

#include <string>

namespace py {

// Forward declarations for types that will define str()
template <typename T> class list;
template <typename T> class ptr;

// str() overloads for primitives
inline std::string str(int x) { return std::to_string(x); }

inline std::string str(double x) { return std::to_string(x); }

inline std::string str(bool x) { return x ? "True" : "False"; }

inline std::string str(const std::string &s) { return s; }

inline std::string str(const char *s) { return std::string(s); }

} // namespace py
