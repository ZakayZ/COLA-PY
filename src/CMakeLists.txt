cmake_minimum_required(VERSION 3.15)
project(COLA-Py VERSION 1.0.0)

# c++17 is recommended
set(CMAKE_CXX_STANDARD 17)

# Find COLA package
find_package(COLA)
# find_package(Python3 COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG REQUIRED)

# Include CMake module for config file generation
include(CMakePackageConfigHelpers)

# Modules can be installed whenever you please, however grouping them all in COLA directory is neat and
# makes further adjustments to CMAKE_PREFIX_PATH unnecessary. It is also advised to put module files to corresponding
# directories to avoid pollution.
set(CMAKE_INSTALL_PREFIX ${COLA_DIR})
set(COLA_MODULE_NAME COLA-Py)

file(
    GLOB SRCS
    COLA-Py/*.cpp
)
add_library(
    COLA-Py SHARED
    ${SRCS}
    bindings.cpp # makes casting (py->cpp, cpp->py) possible
)

target_include_directories(
    COLA-Py PUBLIC
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/>
    $<INSTALL_INTERFACE:include/${COLA_MODULE_NAME}>
)

# Link against COLA
target_link_libraries(COLA-Py PUBLIC COLA pybind11::embed)

# Fun begins
target_compile_options(COLA-Py PRIVATE -Wall -Werror -Wfloat-conversion -Wextra -Wpedantic)
set_source_files_properties(bindings.cpp PROPERTIES COMPILE_FLAGS -Wno-self-assign-overloaded)

# Configure config files
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/data/COLA-PyConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/COLA-PyConfig.cmake"
    INSTALL_DESTINATION lib/cmake/${COLA_MODULE_NAME}
    #PATH_VARS, etc.
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/COLA-PyConfigVersion.cmake
    COMPATIBILITY AnyNewerVersion
)

# Install library
install(
    TARGETS COLA-Py
    EXPORT COLA-PyExport
    LIBRARY DESTINATION lib/${COLA_MODULE_NAME}
    PUBLIC_HEADER DESTINATION include/${COLA_MODULE_NAME}
    INCLUDES DESTINATION include/${COLA_MODULE_NAME}
)

# Install includes
install(
    DIRECTORY COLA-Py
    DESTINATION include
    FILES_MATCHING
        PATTERN "*.hh"
)

# Install export file and config files
install(
    EXPORT COLA-PyExport
    DESTINATION lib/cmake/${COLA_MODULE_NAME}
)

install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/COLA-PyConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/COLA-PyConfigVersion.cmake"
    DESTINATION lib/cmake/${COLA_MODULE_NAME}
)