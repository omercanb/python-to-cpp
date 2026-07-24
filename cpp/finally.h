#pragma once

// Scope guard backing Python's `finally`.

#include <utility>

namespace py {

template <class F>
class Finally {
  public:
    explicit Finally(F body) : body(std::move(body)) {}
    // noexcept(false) lets a raise inside the finally out. Nothing can save one
    // raised while unwinding; C++ terminates rather than replace the live one.
    ~Finally() noexcept(false) { body(); }
    Finally(const Finally &) = delete;
    Finally &operator=(const Finally &) = delete;

  private:
    F body;
};

// C++17 deduces class template arguments from a constructor only with this.
template <class F>
Finally(F) -> Finally<F>;

} // namespace py
