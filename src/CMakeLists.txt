# COLA-Py plugin (loaded by COLA at runtime). Included from the repo root only.

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(COLA_MODULE_NAME COLA-Py)

file(GLOB COLA_PY_SRCS CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/${COLA_MODULE_NAME}/*.cpp")

add_library(${COLA_MODULE_NAME} SHARED ${COLA_PY_SRCS})

target_compile_features(${COLA_MODULE_NAME} PUBLIC cxx_std_17)

target_include_directories(
    ${COLA_MODULE_NAME} PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                               $<INSTALL_INTERFACE:${COLA_DIR}/${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}>
)

target_link_libraries(${COLA_MODULE_NAME} PUBLIC COLA pybind11::embed pybind11::pybind11)

target_compile_options(
    ${COLA_MODULE_NAME} PRIVATE -Wall -Werror -Wfloat-conversion -Wextra -Wpedantic
)

set_target_properties(
    ${COLA_MODULE_NAME}
    PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE
               BUILD_WITH_INSTALL_RPATH TRUE
               CXX_CLANG_TIDY "${COLA_CMAKE_CXX_CLANG_TIDY}"
)

install(
    TARGETS ${COLA_MODULE_NAME}
    EXPORT ${COLA_MODULE_NAME}Export
    LIBRARY DESTINATION ${COLA_DIR}/${CMAKE_INSTALL_LIBDIR}/${COLA_MODULE_NAME}
    INCLUDES DESTINATION ${COLA_DIR}/${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}
)

install(
    DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/${COLA_MODULE_NAME}"
    DESTINATION "${COLA_DIR}/${CMAKE_INSTALL_INCLUDEDIR}/${COLA_MODULE_NAME}"
    FILES_MATCHING
    PATTERN "*.hh"
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/data/${COLA_MODULE_NAME}Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
    INSTALL_DESTINATION "${COLA_DIR}/${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}"
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake
    COMPATIBILITY AnyNewerVersion
)

install(EXPORT ${COLA_MODULE_NAME}Export
        DESTINATION "${COLA_DIR}/${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}")

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}Config.cmake"
                "${CMAKE_CURRENT_BINARY_DIR}/${COLA_MODULE_NAME}ConfigVersion.cmake"
        DESTINATION "${COLA_DIR}/${CMAKE_INSTALL_LIBDIR}/cmake/${COLA_MODULE_NAME}"
)

if (BUILD_TESTING)
    add_subdirectory(${COLA_MODULE_NAME}/tests)
endif ()
