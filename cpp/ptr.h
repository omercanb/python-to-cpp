#pragma once

// A refcounted pointer that copies python objects

#include "str.h"
#include "truthy.h"
#include <iostream>
#include <utility>
namespace py {
template <typename T> class ptr {
    // Hold a pointer to an object
    // Hold a reference to a 'refcount' int
  public:
    using value_type = T;
    using size_type = long long;

    int *refcount;
    value_type *object;

    ptr() {
        object = nullptr;
        refcount = new int;
        *refcount = 1;
        std::cerr << "empty constructor\n";
    }

    ptr(value_type *obj) {
        object = obj;
        refcount = new int;
        *refcount = 1;
        std::cerr << "pointer constructor: " << *refcount << "\n";
    }

    ptr(const ptr &o) {
        std::cerr << "copy constructor\n";
        o.reference();
        object = o.object;
        refcount = o.refcount;
    }

    // Refence and dereference must happen in this order to survive self assign:
    // a = a
    ptr &operator=(const ptr &o) {
        o.reference();
        dereference();
        object = o.object;
        refcount = o.refcount;
        std::cerr << "copy assign" << *refcount << "\n";
        return *this;
    }

    value_type &operator*() const { return *object; }
    value_type *operator->() const { return object; }

    ~ptr() { dereference(); }

    void reference() const { (*refcount)++; }
    void dereference() const {
        (*refcount)--;
        if ((*refcount) <= 0) {
            std::cerr << "deletion\n";
            if (object != nullptr) {
                delete object;
            }
            delete refcount;
        }
    }
    // Templated on the index type so non-integer keys (dict) work too.
    template <typename I> decltype(auto) operator[](const I &i) {
        return (*object)[i];
    }
    template <typename I> decltype(auto) operator[](const I &i) const {
        return (*object)[i];
    }
};

template <typename T> _int len(const ptr<T> &p) { return len(*(p.object)); }

// Keeps the ptr alive alongside the container's own iterator: the inner
// iterators hold a bare reference, which would dangle while iterating a
// temporary (`for x in [1, 2, 3]`).
template <typename T> class owning_iter {
  public:
    ptr<T> owner; // declared first: must outlive inner
    decltype(std::declval<T &>().iter()) inner;

    owning_iter(ptr<T> p) : owner(p), inner(p->iter()) {}

    decltype(auto) current() { return inner.current(); }
    decltype(auto) next() { return inner.next(); }
    bool done() { return inner.done(); }
};

template <typename T> auto iter(ptr<T> p) { return owning_iter<T>(p); }

// str() - dereference and convert to string
template <typename T> std::string str(const ptr<T> &p) {
    return str(*p.object);
}

// to_bool() - dereference and forward truthiness
template <typename T> inline bool to_bool(const ptr<T> &p) {
    return to_bool(*p.object);
}

template <typename T1, typename T2>
bool __is(const ptr<T1> &p1, const ptr<T2> &p2) {
    return (void *)p1.object == (void *)p2.object;
}

} // namespace py
