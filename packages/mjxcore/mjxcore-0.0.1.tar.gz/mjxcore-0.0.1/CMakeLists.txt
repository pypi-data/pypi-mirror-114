cmake_minimum_required(VERSION 3.4...3.18)

project(mjxcore)

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS "-fPIC")

add_subdirectory(pybind11)
pybind11_add_module(mjxcore src/main.cpp)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(mjxcore PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
