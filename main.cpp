#include "list.h"
#include "ptr.h"
using namespace py;
ptr<list<int>> l() {
    return ptr(new list({1, 2, 3}));
}

double example(int a, double y) {
    return (a + y);
}

int main() {
    int a;
    a = 1;
    a = 2;
    return 0;
}
