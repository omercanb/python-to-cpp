#include <iostream>
#include "print.h"
#include "list.h"
#include "ptr.h"
using namespace py;


class A;
class B;
class C;
int add(int a, int b);
int mul(int a);
int main();

class A {
public:
    int x;
    
    A(int x) {
        this->x = x;
    }
    
};
class B {
public:
    ptr<A> a;
    std::string y;
    
    B(ptr<A> a, std::string y) {
        this->a = a;
        this->y = y;
    }
    
    void printA() {
        print(this->a->x);
    }
    
};
class C {
public:
    std::string x;
    std::string y;
    
    C(std::string x, std::string y) {
        this->x = x;
        this->y = y;
    }
    
    std::string combine() {
        return (this->x + this->y);
    }
    
};
int add(int a, int b) {
    return (a + b);
}

int mul(int a) {
    return (2 * a);
}

int main() {
std::ios_base::sync_with_stdio(false);
    int a;
    double c;
    double d;
    int e;
    ptr<list<int>> l;
    std::function<int(int)> z;
    ptr<B> cls;
    ptr<C> stuf;
    int i;

    a = (3 + (4 * 5));
    c = (a / 2);
    d = a;
    e = add(a, d);
    l = ptr(new list<int>({}));
    mul(3);
    z = mul;
    print(z(a));
    l->append(2);
    l->append(4);
    l->extend(l);
    l->extend(l);
    cls = ptr(new B(ptr(new A(10)), "hi"));
    stuf = ptr(new C("hi", "hello"));
    print(stuf->combine());
    print(l, a);
    print(l->count(2));
    i = 0;
    while (i < 10) {
        print(i);
        i += 1;
    }
    cls->printA();
    cls->a = ptr(new A(20));
    cls->printA();
    return 0;
}

