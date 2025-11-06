cmake_minimum_required(VERSION 3.15)

if (NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME "colapy")
endif()

if (NOT DEFINED SKBUILD_PROJECT_VERSION)
    set(SKBUILD_PROJECT_VERSION "1.0.0")
endif()

project(
    ${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(COLA QUIET)

include(cmake/InstallDirectory.cmake)

if (NOT COLA_FOUND)
    include(FetchContent)
    include(GNUInstallDirs)

    if (NOT DEFINED COLA_INSTALL_PREFIX)
        if (DEFINED ENV{COLA_INSTALL_PREFIX})
            set(COLA_INSTALL_PREFIX "$ENV{COLA_INSTALL_PREFIX}")
            list(APPEND CMAKE_PREFIX_PATH ${COLA_INSTALL_PREFIX})
        else()
            # Default to user's local directory (cross-platform)
            if (WIN32)
                set(COLA_INSTALL_PREFIX "$ENV{USERPROFILE}/.local")
            else()
                set(COLA_INSTALL_PREFIX "$ENV{HOME}/.local")
            endif()
        endif()
    endif()

    message(STATUS "COLA not found, installing it to \"${COLA_INSTALL_PREFIX}\"")

    FetchContent_Declare(
        COLA
        GIT_REPOSITORY https://github.com/ZakayZ/COLA.git
        GIT_TAG dev
        GIT_SHALLOW TRUE
    )
    FetchContent_GetProperties(cola)

    if (NOT COLA_POPULATED)
        FetchContent_Populate(cola)
        install_global_cmake("${cola_SOURCE_DIR}" "${cola_BINARY_DIR}" "${COLA_INSTALL_PREFIX}" "${CMAKE_BUILD_TYPE}" COLA_INSTALL_RESULT)
        if (COLA_INSTALL_RESULT)
            message(FATAL_ERROR "COLA: ${COLA_INSTALL_RESULT}")
        endif ()

        message(STATUS "COLA installed successfully to ${COLA_INSTALL_PREFIX}")

        find_package(COLA REQUIRED)
    endif()
endif()

install_global_cmake("${CMAKE_SOURCE_DIR}/src" "${CMAKE_BINARY_DIR}/src" "${COLA_DIR}" "${CMAKE_BUILD_TYPE}" COLAPY_INSTALL_RESULT)
if (COLAPY_INSTALL_RESULT)
    message(FATAL_ERROR "COLA-Py: ${COLAPY_INSTALL_RESULT}")
endif ()

# find_package(Python3 COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(
    _cola_impl
    src/bindings.cpp
)

target_link_libraries(_cola_impl PUBLIC COLA)
# set(CMAKE_INSTALL_RPATH "@loader_path;${COLA_DIR}")
message("COLA DIR = ${COLA_DIR} ${CMAKE_INSTALL_RPATH}")
set_target_properties(_cola_impl PROPERTIES
    INSTALL_RPATH "@loader_path;${COLA_DIR}/lib"
    BUILD_WITH_INSTALL_RPATH TRUE
)

target_compile_definitions(_cola_impl PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _cola_impl DESTINATION ${SKBUILD_PROJECT_NAME})
