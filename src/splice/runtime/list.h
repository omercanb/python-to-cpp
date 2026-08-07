// Claude generated C++ List that aims to copy python's list semantics

#pragma once

#include "exceptions.h"
#include "iter.h"
#include "ptr.h"
#include "range.h"
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

namespace detail {

// std::vector<bool> is bit-packed: data_[i] returns a proxy, not a real
// bool&, so every T&-returning method below (operator[], __getitem__,
// back()) would bind that proxy to a dangling reference. bool_vector is a
// plain, unpacked array of bool instead - one real byte per element,
// contiguous, no bit manipulation, no indirection - so it has the same
// memory layout and performance characteristics as std::vector<char>, and
// list<T>'s own methods need no bool-specific handling at all.
class bool_vector {
  public:
    using iterator = bool *;
    using const_iterator = const bool *;

    bool_vector() = default;
    bool_vector(std::initializer_list<bool> init) {
        reserve(init.size());
        for (bool b : init)
            push_back(b);
    }
    bool_vector(const bool_vector &o) { assign_from(o.data_, o.size_); }
    bool_vector(bool_vector &&o) noexcept
        : data_(o.data_), size_(o.size_), capacity_(o.capacity_) {
        o.data_ = nullptr;
        o.size_ = o.capacity_ = 0;
    }
    bool_vector &operator=(const bool_vector &o) {
        if (this != &o) {
            delete[] data_;
            data_ = nullptr;
            size_ = capacity_ = 0;
            assign_from(o.data_, o.size_);
        }
        return *this;
    }
    bool_vector &operator=(bool_vector &&o) noexcept {
        if (this != &o) {
            delete[] data_;
            data_ = o.data_;
            size_ = o.size_;
            capacity_ = o.capacity_;
            o.data_ = nullptr;
            o.size_ = o.capacity_ = 0;
        }
        return *this;
    }
    ~bool_vector() { delete[] data_; }

    size_t size() const noexcept { return size_; }
    bool empty() const noexcept { return size_ == 0; }
    void clear() noexcept { size_ = 0; }

    bool &operator[](size_t i) { return data_[i]; }
    const bool &operator[](size_t i) const { return data_[i]; }
    bool &back() { return data_[size_ - 1]; }
    const bool &back() const { return data_[size_ - 1]; }

    iterator begin() { return data_; }
    iterator end() { return data_ + size_; }
    const_iterator begin() const { return data_; }
    const_iterator end() const { return data_ + size_; }

    void reserve(size_t n) {
        if (n > capacity_)
            grow_to(n);
    }
    void push_back(bool b) {
        if (size_ == capacity_)
            grow_to(capacity_ == 0 ? 4 : capacity_ * 2);
        data_[size_++] = b;
    }
    iterator insert(iterator pos, bool value) {
        size_t at = static_cast<size_t>(pos - data_);
        if (size_ == capacity_)
            grow_to(capacity_ == 0 ? 4 : capacity_ * 2);
        for (size_t i = size_; i > at; --i)
            data_[i] = data_[i - 1];
        data_[at] = value;
        ++size_;
        return data_ + at;
    }
    template <typename It> iterator insert(iterator pos, It first, It last) {
        size_t at = static_cast<size_t>(pos - data_);
        size_t count = static_cast<size_t>(last - first);
        if (size_ + count > capacity_)
            grow_to(size_ + count);
        for (size_t i = size_; i > at; --i)
            data_[i + count - 1] = data_[i - 1];
        size_t i = at;
        for (It it = first; it != last; ++it, ++i)
            data_[i] = *it;
        size_ += count;
        return data_ + at;
    }
    iterator erase(iterator pos) {
        size_t at = static_cast<size_t>(pos - data_);
        for (size_t i = at; i + 1 < size_; ++i)
            data_[i] = data_[i + 1];
        --size_;
        return data_ + at;
    }

  private:
    bool *data_ = nullptr;
    size_t size_ = 0;
    size_t capacity_ = 0;

    void assign_from(const bool *src, size_t n) {
        data_ = n ? new bool[n] : nullptr;
        size_ = n;
        capacity_ = n;
        for (size_t i = 0; i < n; ++i)
            data_[i] = src[i];
    }
    void grow_to(size_t n) {
        bool *bigger = new bool[n];
        for (size_t i = 0; i < size_; ++i)
            bigger[i] = data_[i];
        delete[] data_;
        data_ = bigger;
        capacity_ = n;
    }
};

inline bool operator==(const bool_vector &a, const bool_vector &b) {
    if (a.size() != b.size())
        return false;
    for (size_t i = 0; i < a.size(); ++i)
        if (a[i] != b[i])
            return false;
    return true;
}
inline bool operator!=(const bool_vector &a, const bool_vector &b) { return !(a == b); }
inline bool operator<(const bool_vector &a, const bool_vector &b) {
    return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end());
}
inline bool operator<=(const bool_vector &a, const bool_vector &b) { return !(b < a); }
inline bool operator>(const bool_vector &a, const bool_vector &b) { return b < a; }
inline bool operator>=(const bool_vector &a, const bool_vector &b) { return !(a < b); }

template <typename T> struct list_storage { using type = std::vector<T>; };
template <> struct list_storage<bool> { using type = bool_vector; };

} // namespace detail

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

    // a[-1] and a[-1] = x. A reference, like operator[], so both read and
    // write go through the same call.
    T &back() {
        if (data_.empty())
            throw IndexError("list index out of range");
        return data_.back();
    }
    const T &back() const {
        if (data_.empty())
            throw IndexError("list index out of range");
        return data_.back();
    }

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
        list<T> out;
        out.data_ = data_;
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

    const typename detail::list_storage<T>::type &raw() const noexcept {
        return data_;
    } // escape hatch

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
    typename detail::list_storage<T>::type data_;

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

// Python list values are pointer-backed, so codegen's `a * n` / `n * a`
// need this repeated here rather than on list<T> itself - forwards to the
// value-type operator* above and re-wraps the result.
template <typename T>
ptr<list<T>> operator*(const ptr<list<T>> &a, typename list<T>::size_type n) {
    return ptr<list<T>>(new list<T>(*a * n));
}
template <typename T>
ptr<list<T>> operator*(typename list<T>::size_type n, const ptr<list<T>> &a) {
    return a * n;
}

// a *= n -- mutates the pointed-to list in place, mirroring list<T>::operator*=.
template <typename T>
ptr<list<T>> &operator*=(ptr<list<T>> &a, typename list<T>::size_type n) {
    *a *= n;
    return a;
}

template <typename T>
ptr<list<T>> operator+(const ptr<list<T>> &a, const ptr<list<T>> &b) {
    return ptr<list<T>>(new list<T>(*a + *b));
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
