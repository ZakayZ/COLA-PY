# Requires: pip install .  (colapy + COLA-Py plugin) before running these tests.

find_package(GTest REQUIRED)
find_package(Python REQUIRED COMPONENTS Interpreter Development)

include(GoogleTest)

add_executable(COLAPyModuleTest cola_py_module_test.cc)

set_target_properties(
    COLAPyModuleTest
    PROPERTIES CXX_STANDARD 20
               CXX_STANDARD_REQUIRED YES
               CXX_EXTENSIONS NO
               CXX_CLANG_TIDY "${COLA_CMAKE_CXX_CLANG_TIDY}"
)

target_compile_definitions(
    COLAPyModuleTest PRIVATE "COLA_PY_TEST_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}\""
)

target_link_libraries(COLAPyModuleTest PRIVATE COLA-Py Python::Python)
target_link_libraries(COLAPyModuleTest PRIVATE GTest::GTest GTest::Main)

gtest_discover_tests(
    COLAPyModuleTest PROPERTIES ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}"
)
