#include "cpp_to_expose.h"

void my_cpp_function(){
    std::cout << "Hello from Cpp" << std::endl << "We can also use functions from the external cpp lib\n";
    hello_from_lib();
}