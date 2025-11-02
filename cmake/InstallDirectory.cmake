function(install_global_cmake SOURCE_DIR BINARY_DIR INSTALL_DIR BUILD_TYPE RESULT_NAME)
    execute_process(
        COMMAND ${CMAKE_COMMAND}
            -S ${SOURCE_DIR}
            -B ${BINARY_DIR}
            -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR}
            -DCMAKE_BUILD_TYPE=${BUILD_TYPE}
        RESULT_VARIABLE result
    )

    if (result)
        set(${RESULT_NAME} "Failed to configure" PARENT_SCOPE)
        return ()
    endif()

    execute_process(
        COMMAND ${CMAKE_COMMAND} --build ${BINARY_DIR}
        RESULT_VARIABLE result
    )

    if (result)
        set(${RESULT_NAME} "Failed to build" PARENT_SCOPE)
        return ()
    endif()

    execute_process(
        COMMAND ${CMAKE_COMMAND} --install ${BINARY_DIR}
        RESULT_VARIABLE result
    )

    if (result)
        set(${RESULT_NAME} "Failed to install library to ${INSTALL_DIR}" PARENT_SCOPE)
        return ()
    endif()

    set(${RESULT_NAME} "" PARENT_SCOPE)

endfunction()
