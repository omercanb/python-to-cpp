#pragma once

// Python set semantics on top of std::unordered_set.
// Python guarantees no ordering here either, so programs must sort before
// comparing. frozenset is not implemented.

#include "exceptions.h"
#include "hash.h"
#include "list.h"
#include "ptr.h"
#include "str.h"
#include "types.h"
#include <initializer_list>
#include <string>
#include <unordered_set>

namespace py {

template <typename T> class set {
  public:
    using value_type = T;
    using size_type = _int;

    // ---- construction -------------------------------------------------------
    set() = default;
    set(std::initializer_list<T> init) : data_(init) {}

    template <typename IterableType> set(IterableType &&iterable) {
        auto it = py::iter(iterable);
        while (!it.done()) {
            data_.insert(it.current());
            it.next();
        }
    }

    // ---- size / truthiness --------------------------------------------------
    size_type __len__() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    size_type len() const noexcept { return __len__(); }
    bool empty() const noexcept { return data_.empty(); }
    explicit operator bool() const noexcept { return !data_.empty(); }

    bool __contains__(const T &value) const { // `x in s`
        return data_.find(value) != data_.end();
    }

    // ---- mutating methods ---------------------------------------------------
    void add(const T &value) { data_.insert(value); }

    // remove() raises when absent, discard() does not - the only difference.
    void remove(const T &value) {
        if (data_.erase(value) == 0)
            throw KeyError("element not found");
    }
    void discard(const T &value) { data_.erase(value); }

    // Removes an arbitrary element, like Python.
    T pop() {
        if (data_.empty())
            throw KeyError("pop from an empty set");
        auto it = data_.begin();
        T value = *it;
        data_.erase(it);
        return value;
    }

    void clear() noexcept { data_.clear(); }

    void update(const ptr<set<T>> &other) {
        for (const auto &v : other->data_)
            data_.insert(v);
    }
    void intersection_update(const ptr<set<T>> &other) {
        std::unordered_set<T, hasher<T>> kept;
        for (const auto &v : data_)
            if (other->__contains__(v))
                kept.insert(v);
        data_ = std::move(kept);
    }
    void difference_update(const ptr<set<T>> &other) {
        for (const auto &v : other->data_)
            data_.erase(v);
    }
    void symmetric_difference_update(const ptr<set<T>> &other) {
        for (const auto &v : other->data_) {
            if (data_.find(v) != data_.end())
                data_.erase(v);
            else
                data_.insert(v);
        }
    }

    // ---- non-mutating methods -----------------------------------------------
    // `union` is a C++ keyword; codegen rewrites s.union(...) to union_.
    ptr<set<T>> union_(const ptr<set<T>> &other) const {
        auto out = ptr(new set<T>(*this));
        out->update(other);
        return out;
    }
    ptr<set<T>> intersection(const ptr<set<T>> &other) const {
        auto out = ptr(new set<T>());
        for (const auto &v : data_)
            if (other->__contains__(v))
                out->add(v);
        return out;
    }
    ptr<set<T>> difference(const ptr<set<T>> &other) const {
        auto out = ptr(new set<T>());
        for (const auto &v : data_)
            if (!other->__contains__(v))
                out->add(v);
        return out;
    }
    ptr<set<T>> symmetric_difference(const ptr<set<T>> &other) const {
        auto out = ptr(new set<T>(*this));
        out->symmetric_difference_update(other);
        return out;
    }

    ptr<set<T>> copy() const { return ptr(new set<T>(*this)); }

    // ---- predicates ---------------------------------------------------------
    bool issubset(const ptr<set<T>> &other) const {
        for (const auto &v : data_)
            if (!other->__contains__(v))
                return false;
        return true;
    }
    bool issuperset(const ptr<set<T>> &other) const {
        for (const auto &v : other->raw())
            if (!__contains__(v))
                return false;
        return true;
    }
    bool isdisjoint(const ptr<set<T>> &other) const {
        for (const auto &v : data_)
            if (other->__contains__(v))
                return false;
        return true;
    }

    // ---- comparison ---------------------------------------------------------
    // Subset ordering, so it is partial: two sets can be unequal with
    // neither one below the other.
    bool operator==(const set<T> &o) const { return data_ == o.data_; }
    bool operator!=(const set<T> &o) const { return data_ != o.data_; }
    bool operator<=(const set<T> &o) const {
        for (const auto &v : data_)
            if (o.data_.find(v) == o.data_.end())
                return false;
        return true;
    }
    bool operator<(const set<T> &o) const {
        return __len__() < o.__len__() && *this <= o;
    }
    bool operator>=(const set<T> &o) const { return o <= *this; }
    bool operator>(const set<T> &o) const { return o < *this; }

    // ---- iteration ----------------------------------------------------------
    class set_iterator {
      public:
        using data_type = std::unordered_set<T, hasher<T>>;
        const data_type &s;
        typename data_type::const_iterator it;

        set_iterator(const data_type &s) : s(s), it(s.begin()) {}
        T current() { return *it; }
        T next() { return *it++; }
        bool done() { return it == s.end(); }
    };
    set_iterator iter() const { return set_iterator(data_); }

    const std::unordered_set<T, hasher<T>> &raw() const noexcept { return data_; }

  private:
    std::unordered_set<T, hasher<T>> data_;
};

template <typename T> auto iter(const set<T> &s) { return s.iter(); }

template <typename T> inline _int len(const set<T> &s) { return s.__len__(); }

// Sets are pointer-wrapped, so the operators live on ptr<set<T>>.
template <typename T>
ptr<set<T>> operator|(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return a->union_(b);
}
template <typename T>
ptr<set<T>> operator&(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return a->intersection(b);
}
template <typename T>
ptr<set<T>> operator-(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return a->difference(b);
}
template <typename T>
ptr<set<T>> operator^(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return a->symmetric_difference(b);
}
template <typename T>
bool operator==(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a == *b;
}
template <typename T>
bool operator!=(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a != *b;
}
template <typename T>
bool operator<=(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a <= *b;
}
template <typename T>
bool operator<(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a < *b;
}
template <typename T>
bool operator>=(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a >= *b;
}
template <typename T>
bool operator>(const ptr<set<T>> &a, const ptr<set<T>> &b) {
    return *a > *b;
}

// sorted() is how a program gets a stable view of an unordered set.
template <typename T> ptr<list<T>> sorted(const ptr<set<T>> &s) {
    auto out = ptr(new list<T>());
    for (const auto &v : s->raw())
        out->append(v);
    out->sort();
    return out;
}
template <typename T>
ptr<list<T>> _sorted_kwargs(bool reverse, const ptr<set<T>> &s) {
    auto out = sorted(s);
    out->sort(reverse);
    return out;
}

// str() - {1, 2, 3}; empty prints as set(), since {} is an empty dict.
template <typename T> std::string str(const set<T> &s) {
    if (s.__len__() == 0)
        return "set()";
    std::string result = "{";
    bool first = true;
    for (const auto &v : s.raw()) {
        if (!first)
            result += ", ";
        result += repr(v);
        first = false;
    }
    return result + "}";
}

} // namespace py
