# Setup the project
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(Minimal)

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wall -Wextra --pedantic -fPIC")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Wall -Wextra --pedantic -fPIC")

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(pybind11 CONFIG REQUIRED)

set(HEADERS_DIR ${PROJECT_SOURCE_DIR}/source
                ${PROJECT_SOURCE_DIR}/source/lib
                 )

include_directories(${HEADERS_DIR} ${pybind11_INCLUDE_DIRS})

file(GLOB_RECURSE SOURCES   ${PROJECT_SOURCE_DIR}/source/cpp_to_expose.cpp
                            ${PROJECT_SOURCE_DIR}/source/lib/*.cpp)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
add_library(${PROJECT_NAME} STATIC ${SOURCES})
add_executable(main main/main.cpp)

target_link_libraries(main ${PROJECT_NAME})


add_library(cpp_to_expose STATIC ${PROJECT_SOURCE_DIR}/source/cpp_to_expose.cpp) 

pybind11_add_module (moduleCPP
                    ${PROJECT_SOURCE_DIR}/source/module_p.h
                    ${PROJECT_SOURCE_DIR}/source/module_p.cpp 
                    )

target_link_libraries(moduleCPP PUBLIC ${PROJECT_NAME})