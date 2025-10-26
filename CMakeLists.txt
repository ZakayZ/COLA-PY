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

find_package(COLA)

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

    message(STATUS "COLA not found ${COLA_INSTALL_PREFIX}")

    FetchContent_Declare(
        COLA
        GIT_REPOSITORY https://github.com/Spectator-matter-group-INR-RAS/COLA.git
        GIT_TAG main
        GIT_SHALLOW TRUE
    )
    FetchContent_GetProperties(cola)

    if(NOT COLA_POPULATED)
        FetchContent_Populate(COLA)
        
        execute_process(
            COMMAND ${CMAKE_COMMAND} 
                -S ${cola_SOURCE_DIR}
                -B ${cola_BINARY_DIR}
                -DCMAKE_INSTALL_PREFIX=${COLA_INSTALL_PREFIX}
                -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
            RESULT_VARIABLE result
        )
        
        if(result)
            message(FATAL_ERROR "Failed to configure COLA")
        endif()
        
        execute_process(
            COMMAND ${CMAKE_COMMAND} --build ${cola_BINARY_DIR}
            RESULT_VARIABLE result
        )
        
        if(result)
            message(FATAL_ERROR "Failed to build COLA")
        endif()
        
        execute_process(
            COMMAND ${CMAKE_COMMAND} --install ${cola_BINARY_DIR}
            RESULT_VARIABLE result
        )
        
        if(result)
            message(FATAL_ERROR "Failed to install COLA to ${COLA_INSTALL_PREFIX}")
        endif()

        message(STATUS "COLA installed successfully to ${COLA_INSTALL_PREFIX}")

        find_package(COLA REQUIRED)
    endif()
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

install(TARGETS _cola_impl DESTINATION ${SKBUILD_PROJECT_NAME})
