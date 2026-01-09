#pragma once

#include "factory.hh"

#include <COLA.hh>

namespace cola {
    using COLAPyModule =
        GenericModule<python::PythonWriterFactory, python::PythonConverterFactory, python::PythonGeneratorFactory>;
} // namespace cola
