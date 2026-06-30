#include <iostream>
#include "print.h"
#include "list.h"
#include "ptr.h"
using namespace py;
int add(int x, int y) {
print(x, y);
return (x + y);
}

 

void loop(int x) {
if (x > 0) {
print(x);
loop((x - 1));
}

}

 

void show(ptr<list<int>> x) {
int i= 10;
while (i > 10) {
print(x);
i -= 1;
}

}

 

int global_x= 10;

void combinator() {
print(global_x);
global_x -= 1;
if (global_x > 0) {
combinator();
combinator();
combinator();
combinator();
}

}

 

void range(int start, int end) {
if (start >= end) {
return;
}

print(start);
range((start + 1), end);
}

 

int main() {
int x= 10;
int y= 20;
int z= (x + y);
print(z);
double a= 0.4;
double b= ((2 * a) + x);
print(b);
double c= (a / b);
double d= 1.0;
print(a, b, c);
int i;
i= 20;
i += 2;
i %= 10;
if (i > 10) {
print(i);
} else {
print(d);
}

if (a || (b && c)) {
print(a);
}

if (((a || b) || c) && d) {
print();
}

if ((a <= b) && (b < c) && (c <= d)) {
print();
}

print((b ? a : c));
i= 10;
while (i > 5) {
print(i);
i -= 1;
}

int j= 0;
while (j < 20) {
j += 1;
if ((j % 2) == 0) {
continue;
}

print(j);
if ((j % 11) == 0) {
break;
}

}

int h= 3;
j;
ptr<list<int>> q= ptr(new list({1, 2, 3}));
ptr<list<ptr<list<int>>>> l= ptr(new list({ptr(new list({3, 4})), ptr(new list({4, 4}))}));
print(q);
print(l);
}

 