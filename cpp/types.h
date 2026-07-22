#pragma once

// Concrete C++ types used to represent Python's `int` and `float`.
// Change these in one place to retarget the whole runtime (e.g. to a
// wider integer type). Left in the global namespace (not `namespace py`)
// so headers that aren't namespaced (scalars.h, range.h) and generated
// code (which may use these before any `using namespace py;`) can all
// see them without qualification.
using _int = long long;
using _float = double;
