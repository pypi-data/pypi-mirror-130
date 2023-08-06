#include "levenshtein.hpp"
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <iostream>

namespace lev {
int distance(std::string a, std::string b) {
    const int rows = a.length();
    const int cols = b.length();

    if (rows == 0)
        return cols;

    if (cols == 0)
        return rows;

    uint16_t* matrix = new uint16_t[rows * cols];
    std::memset(matrix, 0, rows * cols * sizeof(uint16_t));

    for (auto i = 0; i < rows; ++i)
        matrix[i * cols] = i;

    for (auto i = 0; i < cols; ++i)
        matrix[i] = i;

    for (auto j = 1; j < cols; ++j) {
        for (auto i = 1; i < rows; ++i) {
            matrix[i * cols + j] = std::min({
                matrix[(i - 1) * cols + j] + 1, // deletion
                matrix[i * cols + j - 1] + 1, // insertion
                matrix[(i - 1) * cols + j - 1] + (a[i - 1] != b[j - 1]) // substitution
            });
        }
    }

    return matrix[rows * cols - 1];
}

float ratio(std::string a, std::string b) {
    float dist   = (float)distance(a, b);
    float length = (float)std::max(a.length(), b.length());

    return (1 - dist / length) * 100;
}
} // namespace lev
