#pragma once

#include "types.h"
#include <cstddef>
#include <functional>
#include <string>
#include <type_traits>
#include <utility>

namespace py {

// ---- hash() - Python hashing ----
// Required by dict keys and set elements. The contract (per the Python
// glossary) is that objects comparing equal must hash equal.
//
// Note: CPython also guarantees hash(1) == hash(1.0) == hash(True),
// because those compare equal. That can't arise here - dict<_int, V> and
// dict<_float, V> are distinct C++ types, so keys of different types are
// never compared against each other in the first place.

inline size_t hash(_int x) { return std::hash<_int>{}(x); }
inline size_t hash(_float x) { return std::hash<_float>{}(x); }
inline size_t hash(bool x) { return std::hash<bool>{}(x); }
inline size_t hash(const std::string &s) { return std::hash<std::string>{}(s); }

// Order-sensitive combine, so hash((1, 2)) != hash((2, 1)).
inline size_t hash_combine(size_t seed, size_t h) {
    return seed ^ (h + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2));
}

namespace detail {

template <typename T, typename = void>
struct has_hash_method : std::false_type {};
template <typename T>
struct has_hash_method<
    T, std::void_t<decltype(std::declval<const T &>().__hash__())>>
    : std::true_type {};

} // namespace detail

// Fallback for user-defined classes: prefer __hash__(), like CPython.
template <typename T> inline size_t hash(const T &x) {
    static_assert(detail::has_hash_method<T>::value,
                  "unhashable type: needs a __hash__() method to be used as a "
                  "dict key or set element");
    return static_cast<size_t>(x.__hash__());
}

// Functor form, for std::unordered_map / std::unordered_set.
// Declared after every hash() overload above so ordinary lookup finds
// them all (ADL alone would miss py::hash for std::string keys).
template <typename T> struct hasher {
    size_t operator()(const T &x) const { return hash(x); }
};

} // namespace py
