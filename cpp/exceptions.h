#pragma once

// Python-style exceptions, shared by the container types.
// Deriving from std::runtime_error so transpiled try/except maps to try/catch.

#include <stdexcept>

namespace py {

struct PyException : std::runtime_error {
    using std::runtime_error::runtime_error;
};
struct IndexError : PyException {
    using PyException::PyException;
};
struct KeyError : PyException {
    using PyException::PyException;
};
struct ValueError : PyException {
    using PyException::PyException;
};
struct TypeError : PyException {
    using PyException::PyException;
};

} // namespace py
