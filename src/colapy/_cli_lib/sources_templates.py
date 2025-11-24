CMAKE_TEMPLATE = '''
set(COLA_MODULE_NAME ${COLA_MODULE_NAME})
set(CMAKE_INSTALL_PREFIX ${COLA_DIR})

cmake_minimum_required(VERSION 3.15)
project(${COLA_MODULE_NAME} VERSION {{ version }})

# c++17 is recommended
set(CMAKE_CXX_STANDARD 17)

# Find COLA package
find_package(COLA)

# Include CMake module for config file generation
include(CMakePackageConfigHelpers)

# Modules can be installed whenever you please, however grouping them all in COLA directory is neat and
# makes further adjustments to CMAKE_PREFIX_PATH unnecessary. It is also advised to put module files to corresponding
# directories to avoid pollution.
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

file(
    GLOB SRCS
    src/*.cpp
)
add_library(
    "${COLA_MODULE_NAME}" SHARED
    ${SRCS}
)

target_include_directories(
    ${COLA_MODULE_NAME} PUBLIC
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include/${COLA_MODULE_NAME}>
)

# Set public header
set_target_properties("${COLA_MODULE_NAME}" PROPERTIES PUBLIC_HEADER "include/${COLA_MODULE_NAME}.hh")

# Link against COLA
target_link_libraries("${COLA_MODULE_NAME}" PUBLIC COLA)

# Fun begins
target_compile_options("${COLA_MODULE_NAME}" PRIVATE -Wall -Werror -Wfloat-conversion -Wextra -Wpedantic)

# Configure config files
configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/data/${COLA_MODULE_NAME}Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
    INSTALL_DESTINATION lib/cmake/${COLA_MODULE_NAME}
    #PATH_VARS, etc.
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake"
    COMPATIBILITY AnyNewerVersion
)

# Install library
install(
    TARGETS "${COLA_MODULE_NAME}"
    EXPORT "${COLA_MODULE_NAME}Export"
    LIBRARY DESTINATION "lib/${COLA_MODULE_NAME}"
    PUBLIC_HEADER DESTINATION "include/${COLA_MODULE_NAME}"
    INCLUDES DESTINATION "include/${COLA_MODULE_NAME}"
)

# Install includes
install(
    DIRECTORY include/
    DESTINATION "include/${COLA_MODULE_NAME}"
)

# Install export file and config files
install(
    EXPORT "${COLA_MODULE_NAME}Export"
    DESTINATION "lib/cmake/${COLA_MODULE_NAME}"
)

install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake"
    DESTINATION lib/cmake/${COLA_MODULE_NAME}
)

'''.lstrip()


GIT_IGNORE_TEMPLATE = '''
CMakeLists.txt.user
CMakeCache.txt
CMakeFiles
CMakeScripts
Testing
Makefile
cmake_install.cmake
install_manifest.txt
compile_commands.json
CTestTestfile.cmake
_deps
/build/
/.idea/
/cmake-build-debug/
/test/build/
/test/cmake-build-debug/
'''.lstrip()