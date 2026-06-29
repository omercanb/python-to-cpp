#include <iostream>

int add(int x, int y) {
std::cout << x << " " << y << "\n";
return (x + y);
}

 

int main() {
int x = 10;
int y = 20;
int z = (x + y);
std::cout << z << "\n";
double a = 0.4;
double b = ((2 * a) + 5);
std::cout << b << "\n";
double c = (a / b);
std::cout << c << "\n";
double d = (x / y);
std::cout << d << "\n";
int f;
std::cout << a << " " << b << " " << c << " " << d << "\n";
int i;
i = 20;
i += 2;
i /= 5;
i %= 10;
if (i > 10) {
std::cout << i << "\n";
} else {
std::cout << d << "\n";
}

if (a || b || (c && d)) {
std::cout << a << "\n";
}

if (((a || b) || c) && d) {
std::cout << "\n";
}

if ((a <= b) && (b < c) && (c <= d)) {
std::cout << "\n";
}

std::cout << (b ? a : c) << "\n";
}

 