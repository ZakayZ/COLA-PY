cmake_minimum_required(VERSION 3.15)

project(
    runner
    VERSION 1.0.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(COLA REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

add_executable(
    embedded_app
    main.cpp
    factory.cpp
    filters.cpp
    interpreter_wrapper.cpp
    ../src/bindings.cpp
)
target_link_libraries(embedded_app PUBLIC COLA pybind11::embed)
