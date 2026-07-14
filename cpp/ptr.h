#pragma once

// A refcounted pointer that copies python objects

#include <iostream>
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
        std::cout << "empty constructor\n";
    }

    ptr(value_type *obj) {
        object = obj;
        refcount = new int;
        *refcount = 1;
        std::cout << "pointer constructor: " << *refcount << "\n";
    }

    ptr(const ptr &o) {
        std::cout << "copy constructor\n";
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
        std::cout << "copy assign" << *refcount << "\n";
        return *this;
    }

    value_type &operator*() const { return *object; }
    value_type *operator->() const { return object; }

    ~ptr() { dereference(); }

    void reference() const { (*refcount)++; }
    void dereference() const {
        (*refcount)--;
        if ((*refcount) <= 0) {
            std::cout << "deletion\n";
            if (object != nullptr) {
                delete object;
            }
            delete refcount;
        }
    }
    decltype(auto) operator[](size_t i) { return (*object)[i]; }
    decltype(auto) operator[](size_t i) const { return (*object[i]); }
};

template <typename T> size_t len(ptr<T> &p) { return len(*(p.object)); }

template <typename T> auto iter(ptr<T> p) { return p->iter(); }

} // namespace py
