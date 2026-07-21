#pragma once

#include <climits>
#include <iostream>
#include <string>

class range_iterator;
class range;
std::ostream &operator<<(std::ostream &os, const range &r);

class range {
  public:
    int start;
    int stop;
    int step;
    range() { start = stop = step = 0; }
    range(int start, int stop = INT_MAX, int step = 1) {
        if (stop == INT_MAX) {
            stop = start;
            start = 0;
        }
        this->start = start;
        this->stop = stop;
        this->step = step;
    }
    range_iterator iter();
};

class range_iterator {
  public:
    range r;
    int cur;
    range_iterator(range r) : r(r), cur(r.start) {}
    int next() {
        auto temp = cur;
        cur += r.step;
        return temp;
    }

    bool done() {
        if (r.step > 0) {
            return cur >= r.stop;
        } else {
            return cur <= r.stop;
        }
    }
};

inline range_iterator range::iter() { return range_iterator(*this); }
auto iter(range r) { return r.iter(); }
auto next(range_iterator &r) { return r.next(); }

std::ostream &operator<<(std::ostream &os, const range &r) {
    os << "range(" << r.start << ", " << r.stop;
    if (r.step != 1) {
        os << ", " << r.step;
    }
    os << ")";
    return os;
};

// str() - convert range to string representation
inline std::string str(const range &r) {
    std::string result = "range(" + std::to_string(r.start) + ", " + std::to_string(r.stop);
    if (r.step != 1) {
        result += ", " + std::to_string(r.step);
    }
    result += ")";
    return result;
}
