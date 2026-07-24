// Claude generated C++ List that aims to copy python's list semantics

#pragma once

#include "exceptions.h"
#include "iter.h"
#include "ptr.h"
#include "slice.h"
#include "str.h"
#include "types.h"
#include <algorithm>
#include <cstddef>
#include <functional>
#include <initializer_list>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace py {

template <typename T>
class list {
  public:
    using value_type = T;
    using size_type = _int;

    // ---- construction -------------------------------------------------------
    list() = default;
    list(std::initializer_list<T> init) : data_(init) {}

    // Construct from any iterable - requires explicit type: list<int>(map(...))
    // (deduction guide in iter.h handles type inference)

    template <typename IterableType>
    list(IterableType &&iterable) {
        auto it = py::iter(iterable);
        while (!it.done()) {
            data_.push_back(it.current());
            it.next();
        }
    }

    size_type __len__() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    bool empty() const noexcept { return data_.empty(); }

    T &operator[](size_type i) { return data_[normIndex(i)]; }
    const T &operator[](size_type i) const { return data_[normIndex(i)]; }

    // What generated code calls for a[i] and a[i] = x. Strict, unlike
    // dict's insert-on-write.
    T &__getitem__(size_type i) { return data_[normIndex(i)]; }
    const T &__getitem__(size_type i) const { return data_[normIndex(i)]; }

    // a[i:j:k] -- a new list, like Python. Out of range bounds clamp rather
    // than raising, which is why this does not go through normIndex.
    ptr<list<T>> __getitem__(const slice &s) const {
        tuple<_int, _int, _int> bounds = s.indices(__len__());
        _int start = bounds.get<0>(), stop = bounds.get<1>(),
             step = bounds.get<2>();

        auto out = new list<T>();
        if (step > 0) {
            for (_int i = start; i < stop; i += step)
                out->append(data_[static_cast<std::size_t>(i)]);
        } else {
            for (_int i = start; i > stop; i += step)
                out->append(data_[static_cast<std::size_t>(i)]);
        }
        return ptr<list<T>>(out);
    }
    void __setitem__(size_type i, const T &value) {
        data_[normIndex(i)] = value;
    }

    void __delitem__(size_type i) { // del a[i]  (strict)
        data_.erase(data_.begin() + normIndex(i));
    }

    void append(const T &x) { data_.push_back(x); }
    void append(T &&x) { data_.push_back(std::move(x)); }

    // Clamps instead of raising: insert(len, x) == append.
    void insert(_int i, const T &x) {
        _int n = __len__();
        if (i < 0) {
            i += n;
            if (i < 0)
                i = 0;
        }
        if (i > n)
            i = n;
        data_.insert(data_.begin() + i, x);
    }

    void remove(const T &value) {
        for (auto it = data_.begin(); it != data_.end(); ++it) {
            if (*it == value) {
                data_.erase(it);
                return;
            }
        }
        throw ValueError("list.remove(x): x not in list");
    }

    T pop(_int i = -1) {
        if (data_.empty())
            throw IndexError("pop from empty list");
        _int n = __len__();
        if (i < 0)
            i += n;
        if (i < 0 || i >= n)
            throw IndexError("pop index out of range");
        T value = std::move(data_[static_cast<std::size_t>(i)]);
        data_.erase(data_.begin() + i);
        return value;
    }

    void extend(const ptr<list<T>> &other) {
        auto len = other->__len__();
        for (size_type i = 0; i < len; ++i) {
            this->append((*other)[i]);
        }
    }

    void clear() noexcept { data_.clear(); }

    _int index(const T &value, size_type start = 0,
               std::optional<size_type> stop = std::nullopt) const {
        _int n = __len__();
        _int s = start;
        _int e = stop.value_or(n);
        if (s < 0) {
            s += n;
            if (s < 0)
                s = 0;
        }
        if (e < 0) {
            e += n;
        } // note: not clamped to 0, matching CPython
        else if (e > n)
            e = n;
        for (_int k = s; k < e; ++k) {
            if (data_[static_cast<std::size_t>(k)] == value)
                return k;
        }
        std::ostringstream m;
        m << "list.index(x): x not in list";
        throw ValueError(m.str());
    }

    _int count(const T &value) const {
        _int c = 0;
        for (const auto &e : data_)
            if (e == value)
                ++c;
        return c;
    }

    // sort: stable (like CPython). reverse keeps equal elements' original
    // order.
    void sort(bool reverse = false) {
        if (!reverse)
            std::stable_sort(data_.begin(), data_.end(),
                             [](const T &a, const T &b) { return a < b; });
        else
            std::stable_sort(data_.begin(), data_.end(),
                             [](const T &a, const T &b) { return b < a; });
    }

    void reverse() noexcept { std::reverse(data_.begin(), data_.end()); }

    // Copies via *this; list<T>(data_) would hit the iterable constructor.
    ptr<list<T>> copy() const { return ptr(new list<T>(*this)); }

    // ---- membership / iteration --------------------------------------------
    bool __contains__(const T &value) const { // `value in a`
        for (const auto &e : data_)
            if (e == value)
                return true;
        return false;
    }
    auto begin() { return data_.begin(); }
    auto end() { return data_.end(); }
    auto begin() const { return data_.begin(); }
    auto end() const { return data_.end(); }

    // ---- operators ----------------------------------------------------------
    // + returns a new list; += extends in place and returns *this (Python
    // semantics).
    list<T> operator+(const list<T> &other) const {
        list<T> out(data_);
        out.data_.insert(out.data_.end(), other.data_.begin(),
                         other.data_.end());
        return out;
    }
    list<T> &operator+=(const list<T> &other) {
        extend(other);
        return *this;
    }

    // * repetition. Non-positive count yields an empty list (Python behavior).
    list<T> operator*(size_type n) const {
        list<T> out;
        if (n > 0) {
            out.data_.reserve(static_cast<std::size_t>(n * __len__()));
            for (_int k = 0; k < n; ++k)
                out.data_.insert(out.data_.end(), data_.begin(), data_.end());
        }
        return out;
    }
    list<T> &operator*=(size_type n) {
        *this = (*this) * n;
        return *this;
    }

    // Lexicographic comparison (std::vector already does this element-wise).
    bool operator==(const list<T> &o) const { return data_ == o.data_; }
    bool operator!=(const list<T> &o) const { return data_ != o.data_; }
    bool operator<(const list<T> &o) const { return data_ < o.data_; }
    bool operator<=(const list<T> &o) const { return data_ <= o.data_; }
    bool operator>(const list<T> &o) const { return data_ > o.data_; }
    bool operator>=(const list<T> &o) const { return data_ >= o.data_; }

    const std::vector<T> &raw() const noexcept { return data_; } // escape hatch

    class list_iterator {
      public:
        list<T> &l;
        size_t i;
        list_iterator(list<T> &l) : l(l), i(0) {}
        T current() { return l[i]; }
        T next() { return l[i++]; }
        bool done() { return i >= l.__len__(); }
    };
    list_iterator iter() { return list_iterator(*this); }

    str __str__() const {
        str result = "[";
        for (size_type i = 0; i < __len__(); ++i) {
            if (i > 0)
                result += ", ";
            result += repr((*this)[i]);
        }
        return result + "]";
    }

  private:
    std::vector<T> data_;

    // strict integer-index normalization shared by [], delItem
    std::size_t normIndex(_int i) const {
        _int n = __len__();
        if (i < 0)
            i += n;
        if (i < 0 || i >= n)
            throw IndexError("list index out of range");
        return static_cast<std::size_t>(i);
    }
};

template <typename T>
auto iter(list<T> &l) { return l.iter(); }
template <typename It>
auto next(It &it) { return it.next(); }

// n * a  (mirror of a * n)
template <typename T>
list<T> operator*(typename list<T>::size_type n, const list<T> &a) {
    return a * n;
}

template <typename T>
inline _int len(const list<T> &l) {
    return l.__len__();
}

// sorted(iterable, *, reverse=False) - returns a new list.
// _sorted_kwargs is emitted when the call passes reverse=, like print.
template <typename T>
ptr<list<T>> sorted(const ptr<list<T>> &l) {
    auto out = l->copy();
    out->sort();
    return out;
}
template <typename T>
ptr<list<T>> _sorted_kwargs(bool reverse, const ptr<list<T>> &l) {
    auto out = l->copy();
    out->sort(reverse);
    return out;
}

// Deduction guide
template <typename IterableType>
list(IterableType &&)
    -> list<decltype(iter(std::declval<IterableType &>()).current())>;

} // namespace py
