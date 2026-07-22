#pragma once

#include "str.h"
#include "tuple.h"
#include "types.h"
#include <memory>

namespace py {

// ---- enumerate ----
// Wraps an iterator and produces tuple<_int, element_type>
template <typename IterType> class enumerate_iter {
  public:
    IterType iter_;
    _int index;

    enumerate_iter(IterType iter) : iter_(iter), index(0) {}

    bool done() { return iter_.done(); }

    void next() {
        iter_.next();
        index++;
    }

    // Get current (index, element) as a tuple
    auto current() {
        return tuple<_int, decltype(iter_.current())>(index, iter_.current());
    }
};

template <typename Container> auto enumerate(Container &&c) {
    return enumerate_iter<decltype(iter(c))>(iter(c));
}

// ---- zip ----
// Wraps two iterators and produces tuple<T1, T2>
template <typename Iter1, typename Iter2> class zip_iter {
  public:
    Iter1 iter1_;
    Iter2 iter2_;

    zip_iter(Iter1 iter1, Iter2 iter2) : iter1_(iter1), iter2_(iter2) {}

    bool done() { return iter1_.done() || iter2_.done(); }

    void next() {
        iter1_.next();
        iter2_.next();
    }

    auto current() {
        return tuple<decltype(iter1_.current()), decltype(iter2_.current())>(
            iter1_.current(), iter2_.current());
    }
};

template <typename C1, typename C2> auto zip(C1 &&c1, C2 &&c2) {
    return zip_iter<decltype(iter(c1)), decltype(iter(c2))>(iter(c1), iter(c2));
}

// ---- map ----
// Wraps an iterator and applies a function to each element
template <typename IterType, typename Func> class map_iter {
  public:
    IterType iter_;
    Func func_;

    map_iter(IterType iter, Func func) : iter_(iter), func_(func) {}

    bool done() { return iter_.done(); }

    void next() { iter_.next(); }

    auto current() { return func_(iter_.current()); }
};

template <typename Container, typename Func>
auto map(Func func, Container &&c) {
    return map_iter<decltype(iter(c)), Func>(iter(c), func);
}

// ---- filter ----
// Wraps an iterator and skips elements that don't match predicate
template <typename IterType, typename Pred> class filter_iter {
  public:
    IterType iter_;
    Pred pred_;

    filter_iter(IterType iter, Pred pred) : iter_(iter), pred_(pred) {
        advance_to_match();
    }

    bool done() { return iter_.done(); }

    void next() {
        iter_.next();
        advance_to_match();
    }

    auto current() { return iter_.current(); }

  private:
    void advance_to_match() {
        while (!iter_.done() && !pred_(iter_.current())) {
            iter_.next();
        }
    }
};

template <typename Container, typename Pred>
auto filter(Pred pred, Container &&c) {
    return filter_iter<decltype(iter(c)), Pred>(iter(c), pred);
}

// ---- iter() functions for iterator types ----
// These allow calling iter() on an iterator to get itself back
// Lvalue versions
template <typename IterType>
enumerate_iter<IterType> &iter(enumerate_iter<IterType> &e) {
    return e;
}

template <typename Iter1, typename Iter2>
zip_iter<Iter1, Iter2> &iter(zip_iter<Iter1, Iter2> &z) {
    return z;
}

template <typename IterType, typename Func>
map_iter<IterType, Func> &iter(map_iter<IterType, Func> &m) {
    return m;
}

template <typename IterType, typename Pred>
filter_iter<IterType, Pred> &iter(filter_iter<IterType, Pred> &f) {
    return f;
}

// Rvalue versions - return by value since we can't return reference to
// temporary
template <typename IterType>
enumerate_iter<IterType> iter(enumerate_iter<IterType> &&e) {
    return e;
}

template <typename Iter1, typename Iter2>
zip_iter<Iter1, Iter2> iter(zip_iter<Iter1, Iter2> &&z) {
    return z;
}

template <typename IterType, typename Func>
map_iter<IterType, Func> iter(map_iter<IterType, Func> &&m) {
    return m;
}

template <typename IterType, typename Pred>
filter_iter<IterType, Pred> iter(filter_iter<IterType, Pred> &&f) {
    return f;
}

// ---- next() functions for iterator types ----
// Return current value and advance the iterator
template <typename IterType> auto next(enumerate_iter<IterType> &e) {
    auto val = e.current();
    e.next();
    return val;
}

template <typename Iter1, typename Iter2> auto next(zip_iter<Iter1, Iter2> &z) {
    auto val = z.current();
    z.next();
    return val;
}

template <typename IterType, typename Func>
auto next(map_iter<IterType, Func> &m) {
    auto val = m.current();
    m.next();
    return val;
}

template <typename IterType, typename Pred>
auto next(filter_iter<IterType, Pred> &f) {
    auto val = f.current();
    f.next();
    return val;
}

// ---- Deduction guide for list construction from iterables ----
// Defined here (not in list.h) because it needs iter() functions to be declared
// #include "list.h"
//
// template <typename IterableType>
// list(IterableType &&) ->
// list<decltype(iter(std::declval<IterableType>()).current())>;
//
} // namespace py
