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

    ptr(value_type *obj) {
        std::cout << "pointer constructor\n";
        object = obj;
        refcount = new int;
        *refcount = 1;
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
        std::cout << "copy assign\n";
        o.reference();
        dereference();
        object = o.object;
        refcount = o.refcount;
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
            delete object;
            delete refcount;
        }
    }
};

} // namespace py
