#pragma once

// Python dict semantics on top of std::unordered_map.
//
// Ordering: CPython dicts are insertion-ordered (guaranteed since 3.7),
// which would need a second, dense insertion-order array alongside the
// hash table. We deliberately don't reproduce that - iteration order here
// is unspecified, so transpiled programs must sort before comparing.

#include "exceptions.h"
#include "hash.h"
#include "list.h"
#include "ptr.h"
#include "str.h"
#include "tuple.h"
#include "types.h"
#include <initializer_list>
#include <optional>
#include <string>
#include <unordered_map>
#include <utility>

namespace py {

template <typename K, typename V> class dict {
  public:
    using key_type = K;
    using mapped_type = V;
    using size_type = _int;

    // ---- construction -------------------------------------------------------
    dict() = default;
    dict(std::initializer_list<std::pair<const K, V>> init) : data_(init) {}

    // ---- size / truthiness --------------------------------------------------
    size_type __len__() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    size_type len() const noexcept { return __len__(); }
    bool empty() const noexcept { return data_.empty(); }
    explicit operator bool() const noexcept { return !data_.empty(); }

    // ---- item access --------------------------------------------------------
    // Write path: d[k] = v. Inserts a default-constructed value when the
    // key is absent, exactly like std::unordered_map::operator[].
    V &operator[](const K &key) { return data_[key]; }

    // Read path: d[k]. Python raises KeyError for a missing key, which
    // operator[] can't do (it can't tell a read from a write), so reads
    // are routed here by the code generator instead.
    V &__getitem__(const K &key) {
        auto it = data_.find(key);
        if (it == data_.end())
            throw KeyError("key not found");
        return it->second;
    }
    const V &__getitem__(const K &key) const {
        auto it = data_.find(key);
        if (it == data_.end())
            throw KeyError("key not found");
        return it->second;
    }

    void __setitem__(const K &key, const V &value) { data_[key] = value; }

    // del d[k]
    void __delitem__(const K &key) {
        if (data_.erase(key) == 0)
            throw KeyError("key not found");
    }

    bool __contains__(const K &key) const { // `k in d`
        return data_.find(key) != data_.end();
    }

    // ---- dict methods -------------------------------------------------------
    // get(key, default=None): never raises. Without a default, a missing
    // key yields a value-initialized V (our stand-in for None).
    V get(const K &key) const {
        auto it = data_.find(key);
        return it == data_.end() ? V() : it->second;
    }
    V get(const K &key, const V &fallback) const {
        auto it = data_.find(key);
        return it == data_.end() ? fallback : it->second;
    }

    // pop(key[, default]): raises KeyError when absent and no default.
    V pop(const K &key) {
        auto it = data_.find(key);
        if (it == data_.end())
            throw KeyError("key not found");
        V value = std::move(it->second);
        data_.erase(it);
        return value;
    }
    V pop(const K &key, const V &fallback) {
        auto it = data_.find(key);
        if (it == data_.end())
            return fallback;
        V value = std::move(it->second);
        data_.erase(it);
        return value;
    }

    // popitem(): CPython pops in LIFO order; with no insertion order to
    // draw on we remove an arbitrary item instead.
    tuple<K, V> popitem() {
        if (data_.empty())
            throw KeyError("popitem(): dictionary is empty");
        auto it = data_.begin();
        tuple<K, V> entry(it->first, it->second);
        data_.erase(it);
        return entry;
    }

    // setdefault(key, default=None): insert-and-return when absent.
    V &setdefault(const K &key) { return data_[key]; }
    V &setdefault(const K &key, const V &fallback) {
        auto it = data_.find(key);
        if (it == data_.end())
            it = data_.emplace(key, fallback).first;
        return it->second;
    }

    void update(const ptr<dict<K, V>> &other) {
        for (const auto &entry : other->data_)
            data_[entry.first] = entry.second;
    }

    void clear() noexcept { data_.clear(); }

    ptr<dict<K, V>> copy() const { return ptr(new dict<K, V>(*this)); }

    // keys()/values()/items(): CPython returns live views onto the dict.
    // These are snapshots - a later mutation is not reflected back.
    ptr<list<K>> keys() const {
        auto out = ptr(new list<K>());
        for (const auto &entry : data_)
            out->append(entry.first);
        return out;
    }
    ptr<list<V>> values() const {
        auto out = ptr(new list<V>());
        for (const auto &entry : data_)
            out->append(entry.second);
        return out;
    }
    ptr<list<tuple<K, V>>> items() const {
        auto out = ptr(new list<tuple<K, V>>());
        for (const auto &entry : data_)
            out->append(tuple<K, V>(entry.first, entry.second));
        return out;
    }

    // ---- comparison ---------------------------------------------------------
    // Order-independent, like Python: equal iff same keys mapping to equal
    // values. std::unordered_map::operator== already works this way.
    bool operator==(const dict<K, V> &o) const { return data_ == o.data_; }
    bool operator!=(const dict<K, V> &o) const { return data_ != o.data_; }

    // ---- iteration ----------------------------------------------------------
    // `for k in d` iterates keys, matching Python.
    class dict_iterator {
      public:
        using map_type = std::unordered_map<K, V, hasher<K>>;
        const map_type &m;
        typename map_type::const_iterator it;

        dict_iterator(const map_type &m) : m(m), it(m.begin()) {}
        K current() { return it->first; }
        K next() {
            K key = it->first;
            ++it;
            return key;
        }
        bool done() { return it == m.end(); }
    };
    dict_iterator iter() const { return dict_iterator(data_); }

    const std::unordered_map<K, V, hasher<K>> &raw() const noexcept {
        return data_;
    }

  private:
    std::unordered_map<K, V, hasher<K>> data_;
};

template <typename K, typename V> auto iter(const dict<K, V> &d) {
    return d.iter();
}

template <typename K, typename V>
inline _int len(const dict<K, V> &d) {
    return d.__len__();
}

// sorted(d) sorts a dict's keys, since iterating a dict yields its keys.
// Iteration order here is unspecified, so this is how transpiled programs
// get a deterministic view of a dict.
template <typename K, typename V> ptr<list<K>> sorted(const ptr<dict<K, V>> &d) {
    auto out = d->keys();
    out->sort();
    return out;
}
template <typename K, typename V>
ptr<list<K>> _sorted_kwargs(bool reverse, const ptr<dict<K, V>> &d) {
    auto out = d->keys();
    out->sort(reverse);
    return out;
}

// str() - {k: v, ...} with elements rendered via repr(), like Python
template <typename K, typename V> std::string str(const dict<K, V> &d) {
    std::string result = "{";
    bool first = true;
    for (const auto &entry : d.raw()) {
        if (!first)
            result += ", ";
        result += repr(entry.first) + ": " + repr(entry.second);
        first = false;
    }
    return result + "}";
}

} // namespace py
