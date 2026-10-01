# Only an explicitly supplied prefix authorizes installing COLA.
if (NOT DEFINED COLA_INSTALL_PREFIX AND DEFINED ENV{COLA_INSTALL_PREFIX})
    set(COLA_INSTALL_PREFIX "$ENV{COLA_INSTALL_PREFIX}")
endif ()

if (NOT "${COLA_INSTALL_PREFIX}" STREQUAL "")
    if (NOT IS_ABSOLUTE "${COLA_INSTALL_PREFIX}" OR "${COLA_INSTALL_PREFIX}" MATCHES ";")
        message(FATAL_ERROR "COLA_INSTALL_PREFIX must be a single absolute path (expand ~ in your shell).")
    endif ()
    get_filename_component(COLA_INSTALL_PREFIX "${COLA_INSTALL_PREFIX}" ABSOLUTE)
    # A cached package directory must not redirect an explicit installation prefix.
    unset(COLA_DIR)
    unset(COLA_DIR CACHE)
    find_package(COLA CONFIG QUIET PATHS "${COLA_INSTALL_PREFIX}" NO_DEFAULT_PATH
                 NO_CMAKE_FIND_ROOT_PATH)
else ()
    find_package(COLA CONFIG QUIET)
endif ()

if (COLA_FOUND)
    return()
endif ()

if ("${COLA_INSTALL_PREFIX}" STREQUAL "")
    message(FATAL_ERROR
        "COLA was not found. Set COLA_INSTALL_PREFIX to an absolute installation path "
        "via the environment or -Ccmake.define.COLA_INSTALL_PREFIX=/path/to/COLA. "
        "No automatic installation is performed without an explicit path.")
endif ()

# DESTDIR would silently redirect installation away from the requested prefix.
if (NOT "$ENV{DESTDIR}" STREQUAL "")
    message(FATAL_ERROR "Unset DESTDIR for COLA auto-installation; COLA_INSTALL_PREFIX is the destination.")
endif ()

include(FetchContent)
message(STATUS "Building and installing COLA only to: ${COLA_INSTALL_PREFIX}")

# Use the direct population API: download only, followed by an explicit standalone
# configure/build/install. Pin the source so installations are reproducible.
FetchContent_Populate(cola
    GIT_REPOSITORY https://github.com/Spectator-matter-group-INR-RAS/COLA.git
    GIT_TAG 167334453a670a717640f6f3a4e43f99a7cc2e2e
    SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/cola-src"
    BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/cola-build"
)

# The pinned upstream config embeds unquoted paths. Fix the downloaded copy to
# support prefixes containing spaces; do not modify an existing COLA installation.
configure_file("${CMAKE_CURRENT_LIST_DIR}/COLAConfig.cmake.in"
               "${cola_SOURCE_DIR}/data/COLAConfig.cmake.in" COPYONLY)
# The pinned upstream's optional developer targets contain a multiline shell
# command that produces invalid Ninja syntax. They are not needed to build COLA.
file(READ "${cola_SOURCE_DIR}/CMakeLists.txt" _cola_project)
string(REPLACE "setup_cola_quality_tools(EXCLUDE_PATTERNS \".*/tinyxml2/.*\")" ""
       _cola_project "${_cola_project}")
file(WRITE "${cola_SOURCE_DIR}/CMakeLists.txt" "${_cola_project}")

set(_cola_config Release)
if (CMAKE_BUILD_TYPE)
    set(_cola_config "${CMAKE_BUILD_TYPE}")
endif ()

set(_cola_configure_args
    -S "${cola_SOURCE_DIR}" -B "${cola_BINARY_DIR}"
    -G "${CMAKE_GENERATOR}"
    "-DCMAKE_INSTALL_PREFIX:PATH=${COLA_INSTALL_PREFIX}"
    "-DCMAKE_BUILD_TYPE:STRING=${_cola_config}"
    -DCMAKE_INSTALL_LIBDIR:STRING=lib
    -DBUILD_TESTING:BOOL=OFF
    -Dtinyxml2_BUILD_TESTING:BOOL=OFF
)
if (CMAKE_GENERATOR_PLATFORM)
    list(APPEND _cola_configure_args -A "${CMAKE_GENERATOR_PLATFORM}")
endif ()
if (CMAKE_GENERATOR_TOOLSET)
    list(APPEND _cola_configure_args -T "${CMAKE_GENERATOR_TOOLSET}")
endif ()
# Keep the dependency on the same toolchain as the Python extension, including
# activated conda compilers and explicitly supplied toolchain/sysroot settings.
foreach (_cola_var IN ITEMS
    CMAKE_MAKE_PROGRAM CMAKE_TOOLCHAIN_FILE CMAKE_SYSROOT
    CMAKE_CXX_COMPILER CMAKE_CXX_COMPILER_ARG1 CMAKE_CXX_COMPILER_TARGET
    CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_RELEASE CMAKE_CXX_FLAGS_DEBUG
    CMAKE_CXX_FLAGS_RELWITHDEBINFO CMAKE_CXX_FLAGS_MINSIZEREL
    CMAKE_SHARED_LINKER_FLAGS CMAKE_EXE_LINKER_FLAGS
    CMAKE_OSX_SYSROOT CMAKE_OSX_ARCHITECTURES CMAKE_OSX_DEPLOYMENT_TARGET)
    if (DEFINED ${_cola_var})
        string(REPLACE ";" "\\;" _cola_value "${${_cola_var}}")
        list(APPEND _cola_configure_args "-D${_cola_var}:STRING=${_cola_value}")
    endif ()
endforeach ()

function (_cola_run stage)
    execute_process(COMMAND ${ARGN} RESULT_VARIABLE _cola_result)
    if (NOT "${_cola_result}" STREQUAL "0")
        message(FATAL_ERROR "COLA ${stage} failed (${_cola_result}); requested prefix: ${COLA_INSTALL_PREFIX}")
    endif ()
endfunction ()

_cola_run(configure "${CMAKE_COMMAND}" -E env --unset=COLA_FETCH_MODE
          "${CMAKE_COMMAND}" ${_cola_configure_args})
_cola_run(build "${CMAKE_COMMAND}" --build "${cola_BINARY_DIR}" --config "${_cola_config}")
_cola_run(install "${CMAKE_COMMAND}" --install "${cola_BINARY_DIR}"
          --config "${_cola_config}" --prefix "${COLA_INSTALL_PREFIX}")

unset(COLA_DIR)
unset(COLA_DIR CACHE)
find_package(COLA CONFIG REQUIRED PATHS "${COLA_INSTALL_PREFIX}" NO_DEFAULT_PATH
             NO_CMAKE_FIND_ROOT_PATH)
message(STATUS "COLA installed successfully to ${COLA_INSTALL_PREFIX}")
