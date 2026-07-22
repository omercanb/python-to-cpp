#pragma once

#include "hash.h"
#include "str.h"
#include <tuple>
#include <string>
#include <sstream>

namespace py {

// Generic tuple wrapper around std::tuple
template <typename... Ts> class tuple {
  public:
    std::tuple<Ts...> data;
    // Default constructor - creates with default-initialized values
    tuple() : data() {}

    // Regular constructor - takes arguments
    tuple(Ts... args) : data(args...) {}

    // Get element by compile-time index
    template <size_t I> auto get() {
        return std::get<I>(data);
    }

    template <size_t I> const auto get() const {
        return std::get<I>(data);
    }

    // Python-like __len__()
    int __len__() const { return sizeof...(Ts); }

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

    tuple_iterator iter() { return tuple_iterator(*this); }
};

// to_str() for tuple - (a, b)
template <typename T1, typename T2>
str to_str(const tuple<T1, T2> &t) {
    return str("(") + repr(t.first()) + ", " + repr(t.second()) + ")";
}

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
