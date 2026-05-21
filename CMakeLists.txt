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

find_package(COLA QUIET)

if (NOT COLA_FOUND)
    include(FetchContent)
    include(GNUInstallDirs)

    if (NOT DEFINED COLA_INSTALL_PREFIX)
        if (DEFINED ENV{COLA_INSTALL_PREFIX})
            set(COLA_INSTALL_PREFIX "$ENV{COLA_INSTALL_PREFIX}")
            list(APPEND CMAKE_PREFIX_PATH ${COLA_INSTALL_PREFIX})
        else ()
            # Default to user's local directory (cross-platform)
            if (WIN32)
                set(COLA_INSTALL_PREFIX "$ENV{USERPROFILE}/.local")
            else ()
                set(COLA_INSTALL_PREFIX "$ENV{HOME}/.local")
            endif ()
        endif ()
    endif ()

    message(STATUS "COLA not found, installing it to \"${COLA_INSTALL_PREFIX}\"")

    FetchContent_Declare(
        COLA
        GIT_REPOSITORY https://github.com/Spectator-matter-group-INR-RAS/COLA.git
        GIT_TAG main
        GIT_SHALLOW TRUE
    )
    FetchContent_GetProperties(cola)

    if (NOT COLA_POPULATED)
        FetchContent_Populate(cola)

        message(STATUS "COLA installed successfully to ${COLA_INSTALL_PREFIX}")

        find_package(COLA REQUIRED)
    endif ()
endif ()

find_package(COLA REQUIRED)

include(GNUInstallDirs)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

enable_testing()
add_subdirectory(src)

if (SKBUILD)
    pybind11_add_module(_cola_impl src/bindings.cpp)

    target_compile_features(_cola_impl PRIVATE cxx_std_17)
    target_link_libraries(_cola_impl PUBLIC COLA)
    set_target_properties(
        _cola_impl PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE BUILD_WITH_INSTALL_RPATH TRUE
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
