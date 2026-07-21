#pragma once

#include "str.h"
#include "tuple.h"
#include <memory>

namespace py {

// ---- enumerate ----
// Wraps an iterator and produces tuple<int, element_type>
template <typename IterType> class enumerate_iter {
  public:
    IterType iter_;
    int index;

    enumerate_iter(IterType iter) : iter_(iter), index(0) {}

    bool done() { return iter_.done(); }

    void next() {
        iter_.next();
        index++;
    }

    // Get current (index, element) as a tuple
    auto current() {
        return tuple<int, decltype(iter_.current())>(index, iter_.current());
    }
};

template <typename Container> auto enumerate(Container &c) {
    return enumerate_iter<decltype(c.iter())>(c.iter());
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

template <typename C1, typename C2> auto zip(C1 &c1, C2 &c2) {
    return zip_iter<decltype(c1.iter()), decltype(c2.iter())>(c1.iter(),
                                                              c2.iter());
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
auto map(Container &c, Func func) {
    return map_iter<decltype(c.iter()), Func>(c.iter(), func);
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
auto filter(Container &c, Pred pred) {
    return filter_iter<decltype(c.iter()), Pred>(c.iter(), pred);
}

} // namespace py
