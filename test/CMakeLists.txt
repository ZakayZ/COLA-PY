cmake_minimum_required(VERSION 3.15)

project(
    runner
    VERSION 1.0.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(COLA REQUIRED)

add_executable(
    runner
    main.cpp
)
target_link_libraries(runner PUBLIC COLA)
