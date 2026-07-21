// Claude generated C++ List that aims to copy python's list semantics

#pragma once

#include "ptr.h"
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

// ---- Python-style exceptions ------------------------------------------------
// Deriving from std::runtime_error so transpiled try/except maps to try/catch.

struct PyException : std::runtime_error {
    using std::runtime_error::runtime_error;
};
struct IndexError : PyException {
    using PyException::PyException;
};
struct ValueError : PyException {
    using PyException::PyException;
};
struct TypeError : PyException {
    using PyException::PyException;
};

template <typename T> class list {
  public:
    using value_type = T;
    using size_type = size_t;

    // ---- construction -------------------------------------------------------
    list() = default;
    list(std::initializer_list<T> init) : data_(init) {}

    // ---- size / truthiness --------------------------------------------------
    size_type size() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    size_type len() const noexcept { return size(); }
    bool empty() const noexcept { return data_.empty(); }
    explicit operator bool() const noexcept {
        return !data_.empty();
    } // `if a:`

    // ---- integer indexing: a[i]  (STRICT, like CPython) ---------------------
    T &operator[](size_type i) { return data_[normIndex(i)]; }
    const T &operator[](size_type i) const { return data_[normIndex(i)]; }
    // ---- deletion -----------------------------------------------------------
    void delItem(size_type i) { // del a[i]  (strict)
        data_.erase(data_.begin() + normIndex(i));
    }

    // ---- list methods -----
    void append(const T &x) { data_.push_back(x); }
    void append(T &&x) { data_.push_back(std::move(x)); }

    // insert is LENIENT: clamps, never raises. insert(len, x) == append.
    void insert(size_type i, const T &x) {
        long long n = size();
        if (i < 0) {
            i += n;
            if (i < 0)
                i = 0;
        }
        if (i > n)
            i = n;
        data_.insert(data_.begin() + i, x);
    }

    // remove: first element == value, else ValueError
    void remove(const T &value) {
        for (auto it = data_.begin(); it != data_.end(); ++it) {
            if (*it == value) {
                data_.erase(it);
                return;
            }
        }
        throw ValueError("list.remove(x): x not in list");
    }

    // pop(i=-1): bounds-checked. Empty -> IndexError("pop from empty list").
    T pop(size_type i = -1) {
        if (data_.empty())
            throw IndexError("pop from empty list");
        long long n = size();
        if (i < 0)
            i += n;
        if (i < 0 || i >= n)
            throw IndexError("pop index out of range");
        T value = std::move(data_[static_cast<std::size_t>(i)]);
        data_.erase(data_.begin() + i);
        return value;
    }

    void extend(ptr<list<T>> &other) {
        auto len = other->size();
        for (size_type i = 0; i < len; ++i) {
            this->append((*other)[i]);
        }
    }

    void clear() noexcept { data_.clear(); }

    // index(value, start=0, stop=size): ValueError if not found.
    // start/stop are clamped exactly as CPython does.
    size_type index(const T &value, size_type start = 0,
                    std::optional<size_type> stop = std::nullopt) const {
        long long n = size();
        long long s = start;
        long long e = stop.value_or(n);
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
        for (long long k = s; k < e; ++k) {
            if (data_[static_cast<std::size_t>(k)] == value)
                return k;
        }
        std::ostringstream m;
        m << "list.index(x): x not in list";
        throw ValueError(m.str());
    }

    size_type count(const T &value) const {
        size_type c = 0;
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

    list<T> copy() const { return list<T>(data_); } // shallow, like list.copy()

    // ---- membership / iteration --------------------------------------------
    bool contains(const T &value) const { // `value in a`
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
            out.data_.reserve(static_cast<std::size_t>(n * size()));
            for (long long k = 0; k < n; ++k)
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
        int next() { return l[i++]; }
        bool done() { return i >= l.len(); }
    };
    list_iterator iter() { return list_iterator(*this); }

  private:
    std::vector<T> data_;

    // strict integer-index normalization shared by [], delItem
    std::size_t normIndex(long long i) const {
        long long n = size();
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

template <typename T> inline size_t len(list<T> &l) { return l.size(); }

// str() - convert list to string representation
template <typename T>
std::string str(const list<T> &l) {
    std::string result = "[";
    for (size_t i = 0; i < l.size(); ++i) {
        if (i > 0)
            result += ", ";
        result += str(l[i]);
    }
    result += "]";
    return result;
}

} // namespace py
