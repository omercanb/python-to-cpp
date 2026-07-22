// Claude generated C++ List that aims to copy python's list semantics

#pragma once

#include "exceptions.h"
#include "iter.h"
#include "ptr.h"
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

// Exceptions (IndexError, ValueError, ...) now live in exceptions.h

template <typename T> class list {
  public:
    using value_type = T;
    using size_type = _int;

    // ---- construction -------------------------------------------------------
    list() = default;
    list(std::initializer_list<T> init) : data_(init) {}

    // Construct from any iterable - requires explicit type: list<int>(map(...))
    // (deduction guide in iter.h handles type inference)

    template <typename IterableType> list(IterableType &&iterable) {
        auto it = py::iter(iterable);
        while (!it.done()) {
            data_.push_back(it.current());
            it.next();
        }
    }

    size_type __len__() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    size_type len() const noexcept { return __len__(); }
    bool empty() const noexcept { return data_.empty(); }
    explicit operator bool() const noexcept {
        return !data_.empty();
    } // `if a:`

    T &operator[](size_type i) { return data_[normIndex(i)]; }
    const T &operator[](size_type i) const { return data_[normIndex(i)]; }
    void __delitem__(size_type i) { // del a[i]  (strict)
        data_.erase(data_.begin() + normIndex(i));
    }

    void append(const T &x) { data_.push_back(x); }
    void append(T &&x) { data_.push_back(std::move(x)); }

    // insert is LENIENT: clamps, never raises. insert(len, x) == append.
    // i is signed (unlike size_type) so a negative "from the end" index
    // survives the `i < 0` check below instead of wrapping around.
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

    // Returns ptr<list<T>> (not list<T>) since every Python list value is
    // pointer-wrapped in the transpiler. Copy-constructs explicitly via
    // *this rather than list<T>(data_), since list<T>(data_) resolves to
    // the generic "construct from any iterable" constructor (data_ is a
    // std::vector<T>, which has no py::iter() overload) instead of an
    // actual copy.
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

    // ---- repr: best-effort `print(a)` ("[1, 2, 3]", strings quoted) ---------
    std::string repr() const {
        std::ostringstream os;
        os << '[';
        for (std::size_t k = 0; k < data_.size(); ++k) {
            if (k)
                os << ", ";
            reprElem(os, data_[k]);
        }
        os << ']';
        return os.str();
    }

    const std::vector<T> &raw() const noexcept { return data_; } // escape hatch

    class list_iterator {
      public:
        list<T> &l;
        size_t i;
        list_iterator(list<T> &l) : l(l), i(0) {}
        T current() { return l[i]; }
        T next() { return l[i++]; }
        bool done() { return i >= l.len(); }
    };
    list_iterator iter() { return list_iterator(*this); }

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

template <typename T> auto iter(list<T> &l) { return l.iter(); }
template <typename It> auto next(It &it) { return it.next(); }

// n * a  (mirror of a * n)
template <typename T>
list<T> operator*(typename list<T>::size_type n, const list<T> &a) {
    return a * n;
}

template <typename T> inline _int len(const list<T> &l) {
    return l.__len__();
}

// sorted(iterable, *, reverse=False) - returns a new list, leaving the
// argument untouched. The _kwargs form is what the code generator emits
// when the call actually passes reverse=, mirroring print/_print_kwargs.
template <typename T> ptr<list<T>> sorted(const ptr<list<T>> &l) {
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

// str() - convert list to string representation
template <typename T> std::string str(const list<T> &l) {
    std::string result = "[";
    for (size_t i = 0; i < l.__len__(); ++i) {
        if (i > 0)
            result += ", ";
        result += repr(l[i]); // elements use repr(), like Python
    }
    result += "]";
    return result;
}

// Deduction guide
template <typename IterableType>
list(IterableType &&)
    -> list<decltype(iter(std::declval<IterableType &>()).current())>;

} // namespace py
