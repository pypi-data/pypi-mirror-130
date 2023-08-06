#include "levenshtein.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(levenshtein, m) {
    std::string version = std::to_string(lev::VERSION_MAJOR) + ".";
    version += std::to_string(lev::VERSION_MINOR) + ".";
    version += std::to_string(lev::VERSION_PATCH);

    m.attr("__version__") = version;
    m.def("distance", &lev::distance, "Compute the levenshtein's distance between two strings");
    m.def("ratio", &lev::ratio, "Compute the levenshtein's ratio between two strings");
}
