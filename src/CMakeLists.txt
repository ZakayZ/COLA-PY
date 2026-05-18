cmake_minimum_required(VERSION 3.15)
project(COLA-Py VERSION 1.0.0)

find_package(COLA REQUIRED)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

include(CMakePackageConfigHelpers)

set(CMAKE_INSTALL_PREFIX ${COLA_DIR})
set(COLA_MODULE_NAME COLA-Py)

file(GLOB SRCS ${COLA_MODULE_NAME}/*.cpp)
add_library(${COLA_MODULE_NAME} SHARED ${SRCS} bindings.cpp)

target_compile_features(${COLA_MODULE_NAME} PUBLIC cxx_std_17)

target_include_directories(
    ${COLA_MODULE_NAME} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/>
                               $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}>
)

target_link_libraries(${COLA_MODULE_NAME} PUBLIC COLA pybind11::embed)

target_compile_options(
    ${COLA_MODULE_NAME} PRIVATE -Wall -Werror -Wfloat-conversion -Wextra -Wpedantic
)
set_source_files_properties(bindings.cpp PROPERTIES COMPILE_FLAGS -Wno-self-assign-overloaded)

configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/data/${COLA_MODULE_NAME}Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake
    COMPATIBILITY AnyNewerVersion
)

install(
    TARGETS ${COLA_MODULE_NAME}
    EXPORT ${COLA_MODULE_NAME}Export
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/${COLA_MODULE_NAME}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}
    INCLUDES
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}
)

install(
    DIRECTORY ${COLA_MODULE_NAME}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING
    PATTERN "*.hh"
)

install(EXPORT ${COLA_MODULE_NAME}Export
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}
)

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
              "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake"
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}
)
