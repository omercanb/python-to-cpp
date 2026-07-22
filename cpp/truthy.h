#pragma once

#include "types.h"
#include <optional>
#include <string>
#include <type_traits>
#include <utility>

namespace py {

// ---- to_bool() - Python truthiness ----
// Concrete overrides for scalars, then Optional[T] (T | None), then a
// generic fallback used by containers/classes: prefer a native
// `operator bool()` (e.g. list<T> already has one), else call __bool__(),
// else use __len__() != 0, else default to True - mirroring CPython's own
// bool() resolution order (__bool__, then __len__, then True).

inline bool to_bool(_int x) { return x != 0; }
inline bool to_bool(_float x) { return x != 0.0; }
inline bool to_bool(bool x) { return x; }
inline bool to_bool(const std::string &s) { return !s.empty(); }

// None is falsy; otherwise defer to the held value's own truthiness
template <typename T> inline bool to_bool(const std::optional<T> &x) {
    return x.has_value() && to_bool(*x);
}

namespace detail {

template <typename T, typename = void>
struct has_bool_conversion : std::false_type {};
template <typename T>
struct has_bool_conversion<
    T, std::void_t<decltype(static_cast<bool>(std::declval<const T &>()))>>
    : std::true_type {};

template <typename T, typename = void>
struct has_bool_method : std::false_type {};
template <typename T>
struct has_bool_method<
    T, std::void_t<decltype(std::declval<const T &>().__bool__())>>
    : std::true_type {};

template <typename T, typename = void>
struct has_len_method : std::false_type {};
template <typename T>
struct has_len_method<
    T, std::void_t<decltype(std::declval<const T &>().__len__())>>
    : std::true_type {};

} // namespace detail

template <typename T> inline bool to_bool(const T &x) {
    if constexpr (detail::has_bool_conversion<T>::value) {
        return static_cast<bool>(x);
    } else if constexpr (detail::has_bool_method<T>::value) {
        return x.__bool__();
    } else if constexpr (detail::has_len_method<T>::value) {
        return x.__len__() != 0;
    } else {
        return true;
    }
}

} // namespace py
