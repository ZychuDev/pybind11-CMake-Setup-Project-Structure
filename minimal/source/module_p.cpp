#include "module_p.h"

namespace py = pybind11;


PYBIND11_MODULE(moduleCPP, m){
    m.doc() = "Module write in cpp with external lib";
    m.def("my_cpp_function", &my_cpp_function, "Function to test build process.");
}