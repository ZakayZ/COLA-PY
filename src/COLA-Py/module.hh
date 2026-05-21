#ifndef COLA_PY_MODULE_HH
#define COLA_PY_MODULE_HH

#include "factory.hh"

#include <COLA.hh>

namespace cola::python {
  using COLAPyModule = GenericModule<PythonWriterFactory, PythonConverterFactory, PythonGeneratorFactory>;
}  // namespace cola::python

#endif  // COLA_PY_MODULE_HH
