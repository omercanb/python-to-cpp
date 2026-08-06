#pragma once

// The C++ types representing Python's `int` and `float` - change here to
// retarget the whole runtime. Global namespace, not py::, so unnamespaced
// headers and generated code can use them unqualified.
using _int = long long;
using _float = double;
