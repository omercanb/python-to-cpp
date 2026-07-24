#pragma once

// Python-style exceptions, shared by the container types.
// Deriving from std::runtime_error so transpiled try/except maps to try/catch.

#include <stdexcept>
#include <utility>

namespace py {

class str;

struct PyException : std::runtime_error {
    using std::runtime_error::runtime_error;
    // Python prints an exception as its message. Defined over in str.h, the
    // first point where str is a complete type.
    str __str__() const;
    // Takes a py::str, which cannot be named here: str.h throws these types.
    // Requiring raw() keeps this off const char* and std::string.
    template <class S, class = decltype(std::declval<const S &>().raw())>
    explicit PyException(const S &message) : std::runtime_error(message.raw()) {}
    // Backs `raise e`, where throwing e would slice it to its declared type.
    // Every subclass must override this or it slices anyway.
    virtual void raise() const { throw *this; }
};
struct IndexError : PyException {
    using PyException::PyException;
    void raise() const override { throw *this; }
};
struct KeyError : PyException {
    using PyException::PyException;
    void raise() const override { throw *this; }
};
struct ValueError : PyException {
    using PyException::PyException;
    void raise() const override { throw *this; }
};
struct TypeError : PyException {
    using PyException::PyException;
    void raise() const override { throw *this; }
};

} // namespace py
