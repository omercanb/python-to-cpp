#pragma once

#include "hash.h"
#include "str.h"
#include <tuple>
#include <type_traits>
#include <string>
#include <sstream>

namespace py {

namespace detail {
// Python compares values of unrelated types as unequal rather than
// erroring, so `in` over a mixed tuple skips incomparable elements.
template <typename A, typename B, typename = void>
struct comparable : std::false_type {};
template <typename A, typename B>
struct comparable<A, B,
                  std::void_t<decltype(std::declval<const A &>() ==
                                       std::declval<const B &>())>>
    : std::true_type {};

template <typename A, typename B> bool eq(const A &a, const B &b) {
    if constexpr (comparable<A, B>::value)
        return a == b;
    else
        return false;
}
} // namespace detail

// Generic tuple wrapper around std::tuple
template <typename... Ts> class tuple {
  public:
    std::tuple<Ts...> data;
    // Default constructor - creates with default-initialized values
    tuple() : data() {}

    // Regular constructor - takes arguments
    tuple(Ts... args) : data(args...) {}

    str __str__() const {
        str result = "(";
        bool first = true;
        std::apply(
            [&](const Ts &...items) {
                (([&] {
                     if (!first)
                         result += ", ";
                     result += repr(items);
                     first = false;
                 }()),
                 ...);
            },
            data);
        // Python writes a one element tuple as (x,), to tell it from (x)
        if constexpr (sizeof...(Ts) == 1)
            result += ",";
        return result + ")";
    }

    // Get element by compile-time index
    template <size_t I> auto get() {
        return std::get<I>(data);
    }

    template <size_t I> const auto get() const {
        return std::get<I>(data);
    }

    // Python-like __len__()
    int __len__() const { return sizeof...(Ts); }

    template <typename U> bool __contains__(const U &value) const {
        bool found = false;
        std::apply(
            [&](const auto &...elems) {
                ((found = found || detail::eq(value, elems)), ...);
            },
            data);
        return found;
    }

    // Assignment operator - forwards to underlying std::tuple
    template <typename... Us>
    tuple& operator=(const tuple<Us...>& other) {
        data = other.data;
        return *this;
    }

    // Iterator support for for loops
    class tuple_iterator {
      public:
        tuple<Ts...> &t;
        size_t i;

        tuple_iterator(tuple<Ts...> &t) : t(t), i(0) {}

        bool done() { return i >= t.__len__(); }

        void next() { i++; }
    };

    tuple_iterator iter() { return tuple_iterator(*this); }
};

// Specialization for 2-element tuple (for enumerate, zip, etc.)
template <typename T1, typename T2> class tuple<T1, T2> {
  public:
    std::tuple<T1, T2> data;
    tuple() : data() {}
    tuple(T1 a, T2 b) : data(a, b) {}

    template <size_t I> auto get() {
        return std::get<I>(data);
    }

    template <size_t I> const auto get() const {
        return std::get<I>(data);
    }

    int __len__() const { return 2; }

    template <typename U> bool __contains__(const U &value) const {
        bool found = false;
        std::apply(
            [&](const auto &...elems) {
                ((found = found || detail::eq(value, elems)), ...);
            },
            data);
        return found;
    }

    // Direct access for convenience
    T1 &first() { return std::get<0>(data); }
    T2 &second() { return std::get<1>(data); }

    const T1 &first() const { return std::get<0>(data); }
    const T2 &second() const { return std::get<1>(data); }

    // Assignment operator - forwards to underlying std::tuple
    template <typename U1, typename U2>
    tuple& operator=(const tuple<U1, U2>& other) {
        data = other.data;
        return *this;
    }

    class tuple_iterator {
      public:
        tuple<T1, T2> &t;
        size_t i;

        tuple_iterator(tuple<T1, T2> &t) : t(t), i(0) {}

        bool done() { return i >= 2; }

        void next() { i++; }
    };

    str __str__() const {
        return str("(") + repr(first()) + ", " + repr(second()) + ")";
    }

    tuple_iterator iter() { return tuple_iterator(*this); }
};

// ---- equality / hashing -----------------------------------------------------
// Needed both for `t1 == t2` and for tuples used as dict keys / set elements.
// std::tuple already compares element-wise.
template <typename... Ts, typename... Us>
bool operator==(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return a.data == b.data;
}
template <typename... Ts, typename... Us>
bool operator!=(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return !(a == b);
}

// Lexicographic, like Python: compares element by element, left to right.
template <typename... Ts, typename... Us>
bool operator<(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return a.data < b.data;
}
template <typename... Ts, typename... Us>
bool operator<=(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return a.data <= b.data;
}
template <typename... Ts, typename... Us>
bool operator>(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return a.data > b.data;
}
template <typename... Ts, typename... Us>
bool operator>=(const tuple<Ts...> &a, const tuple<Us...> &b) {
    return a.data >= b.data;
}

template <typename... Ts> inline size_t hash(const tuple<Ts...> &t) {
    size_t seed = sizeof...(Ts);
    std::apply([&](const Ts &...elems) { ((seed = hash_combine(seed, hash(elems))), ...); },
               t.data);
    return seed;
}

// Destructuring - creates a tuple of references
// Usage: destructure(a, b) = some_tuple;
template <typename... Ts> tuple<Ts&...> destructure(Ts&... args) {
    return tuple<Ts&...>(args...);
}

} // namespace py
