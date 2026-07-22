#include <algorithm>
#include <cctype>
#include <cmath>
#include <stdexcept>
#include <string>

int _int(int v) { return v; }
int _int(double v) { return static_cast<int>(v); }
int _int(bool v) { return v ? 1 : 0; }

int _int(const std::string &s, int base = 10) {
    std::string t = s;
    t.erase(0, t.find_first_not_of(" \t\n"));
    t.erase(t.find_last_not_of(" \t\n") + 1);
    size_t pos;
    int result =
        std::stoll(t, &pos, base); // throws std::invalid_argument on failure
    if (pos != t.size())
        throw std::invalid_argument("invalid literal for int(): " + s);
    return result;
}

double _float(int v) { return v; }
double _float(double v) { return v; }
double _float(bool v) { return v ? 1.0 : 0.0; }

double _float(const std::string &s) {
    std::string t = s;
    t.erase(0, t.find_first_not_of(" \t\n"));
    t.erase(t.find_last_not_of(" \t\n") + 1);

    std::string low = t;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    if (low == "inf" || low == "infinity")
        return INFINITY;
    if (low == "-inf" || low == "-infinity")
        return -INFINITY;
    if (low == "nan" || low == "-nan")
        return NAN;

    size_t pos;
    double result = std::stod(t, &pos); // handles scientific notation
    if (pos != t.size())
        throw std::invalid_argument("could not convert string to float: " + s);
    return result;
}
