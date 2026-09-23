cmake_minimum_required(VERSION 3.15)

if (NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME "colapy")
endif ()

if (NOT DEFINED SKBUILD_PROJECT_VERSION)
    set(SKBUILD_PROJECT_VERSION "1.0.0")
endif ()

project(
    ${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

include(cmake/FindOrInstallCOLA.cmake)

include(GNUInstallDirs)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

enable_testing()
add_subdirectory(src)

if (SKBUILD)
    pybind11_add_module(_cola_impl src/bindings.cpp)

    target_compile_features(_cola_impl PRIVATE cxx_std_17)
    target_link_libraries(_cola_impl PUBLIC COLA)
    set_target_properties(
        _cola_impl PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE INSTALL_RPATH_USE_LINK_PATH TRUE
    )
    target_compile_definitions(_cola_impl PRIVATE VERSION_INFO=${PROJECT_VERSION})

    install(TARGETS _cola_impl DESTINATION ${SKBUILD_PROJECT_NAME})
else ()
    set(COLA_CMAKE_CXX_CLANG_TIDY
        ""
        CACHE STRING "Passed to CMAKE_CXX_CLANG_TIDY for COLA-Py targets"
    )

    setup_cola_quality_tools(".*/COLA/.*")
endif ()
