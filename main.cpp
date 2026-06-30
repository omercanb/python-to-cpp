#include <iostream>

int add(int x, int y) {
std::cout << x << " " << y << "\n";
return (x + y);
}

 

void loop(int x) {
if (x > 0) {
std::cout << x << "\n";
loop((x - 1));
}

}

 

int global_x = 10;

void combinator() {
std::cout << global_x << "\n";
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

std::cout << start << "\n";
range((start + 1), end);
}

 

int main() {
int x = 10;
int y = 20;
int z = (x + y);
std::cout << z << "\n";
double a = 0.4;
double b = ((2 * a) + x);
std::cout << b << "\n";
double c = (a / b);
double d = 1.0;
std::cout << a << " " << b << " " << c << "\n";
int i;
i = 20;
i += 2;
i %= 10;
if (i > 10) {
std::cout << i << "\n";
} else {
std::cout << d << "\n";
}

if (a || (b && c)) {
std::cout << a << "\n";
}

if (((a || b) || c) && d) {
std::cout << "\n";
}

if ((a <= b) && (b < c) && (c <= d)) {
std::cout << "\n";
}

std::cout << (b ? a : c) << "\n";
i = 10;
while (i > 5) {
std::cout << i << "\n";
i -= 1;
}

int j = 0;
while (j < 20) {
j += 1;
if ((j % 2) == 0) {
continue;
}

std::cout << j << "\n";
if ((j % 11) == 0) {
break;
}

}

int h = 3;
j;
combinator();
range(10, 20);
}

 