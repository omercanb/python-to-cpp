#pragma once

#include "types.h"
#include <array>
#include <charconv>
#include <string>

namespace py {

// Forward declarations for types that will define str()
template <typename T> class list;
template <typename T> class ptr;
template <typename... Ts> class tuple;

// str() overloads for primitives
inline std::string str(_int x) { return std::to_string(x); }

inline std::string str(_float x) {
    std::array<char, 32> buf;
    auto result = std::to_chars(buf.data(), buf.data() + buf.size(), x);
    std::string s(buf.data(), result.ptr);
    if (s.find('.') == std::string::npos && s.find('e') == std::string::npos &&
        s.find("inf") == std::string::npos &&
        s.find("nan") == std::string::npos) {
        s += ".0";
    }
    return s;
}

inline std::string str(bool x) { return x ? "True" : "False"; }

inline std::string str(const std::string &s) { return s; }

inline std::string str(const char *s) { return std::string(s); }

// repr() - like str(), but quotes strings. Containers render their
// elements with repr(), so Python shows {'a': 1} not {a: 1}.
inline std::string repr(const std::string &s) { return "'" + s + "'"; }
inline std::string repr(const char *s) { return "'" + std::string(s) + "'"; }
template <typename T> std::string repr(const T &x) { return str(x); }

} // namespace py
