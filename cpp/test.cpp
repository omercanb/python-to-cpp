#include "list.h"
#include "print.h"
#include "ptr.h"
#include <iostream>

using namespace py;
int main() {
    auto a = py::ptr<py::list<int>>(new py::list<int>({1, 2, 3}));
    py::ptr<py::list<int>> b = py::ptr(new py::list({1, 2, 3}));
    ptr<list<int>> c = ptr(new list({1, 2, 3}));
    a = b;
    auto d = c;
    std::cout << "EOF\n";
    ptr<list<int>> e = new list({0, 1, 2});
    e->append(20);
    e->append(10);
    print(e, e, e, "Hello world");
}
