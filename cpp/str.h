#pragma once

// Python str on top of std::string. ASCII only: len() and indexing count
// bytes, not code points, so non-ASCII text will not match Python.
//
// `str` is the type, so the conversion is to_str(), matching to_int/
// to_float/to_bool. Methods returning list<str> (split, ...) are declared
// here and defined in strops.h, since list.h includes this header.

#include "exceptions.h"
#include "types.h"
#include <algorithm>
#include <array>
#include <cctype>
#include <charconv>
#include <ostream>
#include <string>

namespace py {

template <typename T> class list;
template <typename T> class ptr;
template <typename... Ts> class tuple;
class slice;

class str {
  public:
    using size_type = _int;

    str() = default;
    str(const char *s) : data_(s) {}
    str(const std::string &s) : data_(s) {}
    str(std::string &&s) : data_(std::move(s)) {}

    const std::string &raw() const noexcept { return data_; }

    size_type __len__() const noexcept {
        return static_cast<size_type>(data_.size());
    }
    size_type len() const noexcept { return __len__(); }
    bool empty() const noexcept { return data_.empty(); }
    explicit operator bool() const noexcept { return !data_.empty(); }
    size_t __hash__() const { return std::hash<std::string>{}(data_); }

    // Indexing yields a length-1 str: Python has no separate char type.
    str __getitem__(size_type i) const {
        return str(std::string(1, data_[normIndex(i)]));
    }
    // s[i:j:k] -- defined in slice.h, which this header cannot include.
    str __getitem__(const slice &s) const;
    bool __contains__(const str &sub) const {
        return data_.find(sub.data_) != std::string::npos;
    }

    // ---- case ---------------------------------------------------------------
    str upper() const { return mapped(::toupper); }
    str lower() const { return mapped(::tolower); }
    str swapcase() const {
        std::string out = data_;
        for (char &c : out)
            c = isLower(c) ? up(c) : (isUpper(c) ? low(c) : c);
        return str(std::move(out));
    }
    str capitalize() const {
        std::string out = lower().data_;
        if (!out.empty())
            out[0] = up(out[0]);
        return str(std::move(out));
    }
    str title() const {
        std::string out = data_;
        bool start = true;
        for (char &c : out) {
            c = start ? up(c) : low(c);
            start = !isAlpha(c);
        }
        return str(std::move(out));
    }
    str casefold() const { return lower(); }

    // ---- search -------------------------------------------------------------
    // find returns -1 when absent; index raises, which is the only difference.
    _int find(const str &sub) const { return toIndex(data_.find(sub.data_)); }
    _int find(const str &sub, size_type start) const {
        return toIndex(data_.find(sub.data_, clampStart(start)));
    }
    _int rfind(const str &sub) const { return toIndex(data_.rfind(sub.data_)); }
    _int index(const str &sub) const { return found(find(sub)); }
    _int rindex(const str &sub) const { return found(rfind(sub)); }

    bool startswith(const str &prefix) const {
        return data_.rfind(prefix.data_, 0) == 0;
    }
    bool endswith(const str &suffix) const {
        return data_.size() >= suffix.data_.size() &&
               data_.compare(data_.size() - suffix.data_.size(),
                             suffix.data_.size(), suffix.data_) == 0;
    }

    _int count(const str &sub) const {
        if (sub.data_.empty())
            return __len__() + 1;
        _int n = 0;
        for (size_t at = data_.find(sub.data_); at != std::string::npos;
             at = data_.find(sub.data_, at + sub.data_.size()))
            ++n;
        return n;
    }

    // ---- edit ---------------------------------------------------------------
    str replace(const str &old_s, const str &new_s, _int count = -1) const {
        if (old_s.data_.empty())
            return *this;
        std::string out;
        size_t at = 0, prev = 0;
        while (count != 0 && (at = data_.find(old_s.data_, prev)) !=
                                 std::string::npos) {
            out.append(data_, prev, at - prev).append(new_s.data_);
            prev = at + old_s.data_.size();
            if (count > 0)
                --count;
        }
        out.append(data_, prev, std::string::npos);
        return str(std::move(out));
    }

    str removeprefix(const str &prefix) const {
        return startswith(prefix) ? str(data_.substr(prefix.data_.size()))
                                  : *this;
    }
    str removesuffix(const str &suffix) const {
        return !suffix.data_.empty() && endswith(suffix)
                   ? str(data_.substr(0, data_.size() - suffix.data_.size()))
                   : *this;
    }

    // No argument strips whitespace, like Python.
    str strip() const { return lstrip().rstrip(); }
    str lstrip() const {
        size_t b = data_.find_first_not_of(" \t\n\r\f\v");
        return str(b == std::string::npos ? "" : data_.substr(b));
    }
    str rstrip() const {
        size_t e = data_.find_last_not_of(" \t\n\r\f\v");
        return str(e == std::string::npos ? "" : data_.substr(0, e + 1));
    }
    str strip(const str &chars) const { return lstrip(chars).rstrip(chars); }
    str lstrip(const str &chars) const {
        size_t b = data_.find_first_not_of(chars.data_);
        return str(b == std::string::npos ? "" : data_.substr(b));
    }
    str rstrip(const str &chars) const {
        size_t e = data_.find_last_not_of(chars.data_);
        return str(e == std::string::npos ? "" : data_.substr(0, e + 1));
    }

    // ---- padding ------------------------------------------------------------
    str ljust(size_type width, const str &fill = " ") const {
        return pad(width, fill, 0);
    }
    str rjust(size_type width, const str &fill = " ") const {
        return pad(width, fill, 1);
    }
    str center(size_type width, const str &fill = " ") const {
        return pad(width, fill, 2);
    }
    str zfill(size_type width) const {
        _int extra = width - __len__();
        if (extra <= 0)
            return *this;
        bool signed_ = !data_.empty() && (data_[0] == '-' || data_[0] == '+');
        std::string out = signed_ ? std::string(1, data_[0]) : std::string();
        out += std::string(extra, '0');
        out += signed_ ? data_.substr(1) : data_;
        return str(std::move(out));
    }

    // ---- classification -----------------------------------------------------
    // All are false for the empty string, like Python.
    bool isalpha() const { return allOf(isAlpha); }
    bool isdigit() const { return allOf(isDigit); }
    bool isalnum() const {
        return allOf([](char c) { return isAlpha(c) || isDigit(c); });
    }
    bool isspace() const {
        return allOf([](char c) { return std::isspace((unsigned char)c) != 0; });
    }
    bool isdecimal() const { return isdigit(); }
    bool isnumeric() const { return isdigit(); }
    bool isascii() const {
        return std::all_of(data_.begin(), data_.end(),
                           [](char c) { return (unsigned char)c < 128; });
    }
    // Cased characters must agree, and there must be at least one.
    bool isupper() const { return casedAllAre(true); }
    bool islower() const { return casedAllAre(false); }

    // ---- list-returning: defined in strops.h --------------------------------
    ptr<list<str>> split() const;                  // on whitespace
    ptr<list<str>> split(const str &sep) const;
    ptr<list<str>> rsplit(const str &sep) const;
    ptr<list<str>> splitlines() const;
    str join(const ptr<list<str>> &parts) const;

    // ---- operators ----------------------------------------------------------
    str operator+(const str &o) const { return str(data_ + o.data_); }
    str &operator+=(const str &o) {
        data_ += o.data_;
        return *this;
    }
    str operator*(_int n) const {
        std::string out;
        for (_int k = 0; k < n; ++k)
            out += data_;
        return str(std::move(out));
    }
    bool operator==(const str &o) const { return data_ == o.data_; }
    bool operator!=(const str &o) const { return data_ != o.data_; }
    bool operator<(const str &o) const { return data_ < o.data_; }
    bool operator<=(const str &o) const { return data_ <= o.data_; }
    bool operator>(const str &o) const { return data_ > o.data_; }
    bool operator>=(const str &o) const { return data_ >= o.data_; }

    // Iterating a string yields its characters as length-1 strs.
    // Holds the bytes rather than a str, since str is incomplete here.
    class str_iterator {
      public:
        std::string s;
        _int i = 0;
        str_iterator(std::string s) : s(std::move(s)) {}
        str current() { return str(std::string(1, s[i])); }
        str next() { return str(std::string(1, s[i++])); }
        bool done() { return i >= static_cast<_int>(s.size()); }
    };
    str_iterator iter() const { return str_iterator(data_); }

  private:
    std::string data_;

    static bool isAlpha(char c) { return std::isalpha((unsigned char)c) != 0; }
    static bool isDigit(char c) { return std::isdigit((unsigned char)c) != 0; }
    static bool isUpper(char c) { return std::isupper((unsigned char)c) != 0; }
    static bool isLower(char c) { return std::islower((unsigned char)c) != 0; }
    static char up(char c) { return (char)std::toupper((unsigned char)c); }
    static char low(char c) { return (char)std::tolower((unsigned char)c); }

    template <typename F> str mapped(F f) const {
        std::string out = data_;
        for (char &c : out)
            c = (char)f((unsigned char)c);
        return str(std::move(out));
    }
    template <typename F> bool allOf(F f) const {
        return !data_.empty() && std::all_of(data_.begin(), data_.end(), f);
    }
    bool casedAllAre(bool wantUpper) const {
        bool seen = false;
        for (char c : data_) {
            if (!isUpper(c) && !isLower(c))
                continue;
            seen = true;
            if (isUpper(c) != wantUpper)
                return false;
        }
        return seen;
    }
    str pad(size_type width, const str &fill, int mode) const {
        _int extra = width - __len__();
        if (extra <= 0 || fill.data_.empty())
            return *this;
        char f = fill.data_[0];
        if (mode == 0)
            return str(data_ + std::string(extra, f));
        if (mode == 1)
            return str(std::string(extra, f) + data_);
        _int left = extra / 2;
        return str(std::string(left, f) + data_ + std::string(extra - left, f));
    }
    static _int toIndex(size_t at) {
        return at == std::string::npos ? -1 : static_cast<_int>(at);
    }
    static _int found(_int at) {
        if (at < 0)
            throw ValueError("substring not found");
        return at;
    }
    size_t clampStart(size_type start) const {
        _int n = __len__();
        if (start < 0)
            start += n;
        return static_cast<size_t>(start < 0 ? 0 : start);
    }
    size_t normIndex(size_type i) const {
        _int n = __len__();
        if (i < 0)
            i += n;
        if (i < 0 || i >= n)
            throw IndexError("string index out of range");
        return static_cast<size_t>(i);
    }
};

inline str operator*(_int n, const str &s) { return s * n; }
inline _int len(const str &s) { return s.__len__(); }
inline auto iter(const str &s) { return s.iter(); }
inline str operator+(const char *a, const str &b) { return str(a) + b; }
inline std::ostream &operator<<(std::ostream &os, const str &s) {
    return os << s.raw();
}

// ---- to_str() - Python's str() ---------------------------------------------
inline str to_str(_int x) { return str(std::to_string(x)); }

inline str to_str(_float x) {
    std::array<char, 32> buf;
    auto result = std::to_chars(buf.data(), buf.data() + buf.size(), x);
    std::string s(buf.data(), result.ptr);
    if (s.find('.') == std::string::npos && s.find('e') == std::string::npos &&
        s.find("inf") == std::string::npos &&
        s.find("nan") == std::string::npos) {
        s += ".0";
    }
    return str(std::move(s));
}

inline str to_str(bool x) { return str(x ? "True" : "False"); }
inline str to_str(const str &s) { return s; }
inline str to_str(const char *s) { return str(s); }
inline str to_str(const std::string &s) { return str(s); }

// repr() - like to_str(), but quotes strings. Containers render their
// elements with repr(), so Python shows {'a': 1} not {a: 1}.
inline str repr(const str &s) { return str("'" + s.raw() + "'"); }
inline str repr(const char *s) { return repr(str(s)); }
template <typename T> str repr(const T &x) { return to_str(x); }

} // namespace py
