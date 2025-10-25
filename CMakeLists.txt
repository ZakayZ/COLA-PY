cmake_minimum_required(VERSION 3.15)
project(
    ${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

find_package(COLA)

if (NOT COLA_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        COLA
        GIT_REPOSITORY https://github.com/Spectator-matter-group-INR-RAS/COLA.git
        GIT_TAG main
    )
    FetchContent_MakeAvailable(COLA)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Python and pybind11 setup
find_package(pybind11 CONFIG REQUIRED)

# Create Python module
pybind11_add_module(
    _cola_impl 
    src/bindings.cpp
)

# Include directories
# target_include_directories(_cola_impl PRIVATE src/cpp)
target_link_libraries(_cola_impl PUBLIC COLA)

target_compile_definitions(_cola_impl PRIVATE VERSION_INFO=${PROJECT_VERSION})

# Install configuration
install(TARGETS _cola_impl DESTINATION colapy)

# Installation for Python package
install(
    DIRECTORY src/python/colapy/
    DESTINATION .
    FILES_MATCHING PATTERN "*.py"
)

# Testing
# find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
# enable_testing()
#     if(Python_FOUND)
#         add_test(
#             NAME python_tests
#             COMMAND ${Python_EXECUTABLE} -m pytest tests/
#             WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
#         )
# endif()
