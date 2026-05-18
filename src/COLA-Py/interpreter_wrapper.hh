#pragma once

#include <memory>
#include <string>
#include <unordered_map>

namespace pybind11 {
  class object;
}  // namespace pybind11

namespace cola::python {
  namespace detail {
    struct PythonInterpreterState;
  }

  class PythonFilterBase {
   public:
    PythonFilterBase(const std::string& importPath, const std::unordered_map<std::string, std::string>& metaData);

   protected:
    pybind11::object& Object() { return *importedObject_; }

   private:
    static std::unique_ptr<detail::PythonInterpreterState> impl;

    // default deleter fails for forward-declared classes
    struct PyObjectDeleter {
      void operator()(pybind11::object* ptr) const;
    };
    std::unique_ptr<pybind11::object, PyObjectDeleter> importedObject_;
  };
}  // namespace cola::python
