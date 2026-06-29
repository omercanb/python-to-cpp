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
i /= 5;
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
}

 