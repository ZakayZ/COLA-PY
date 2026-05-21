#ifndef COLA_PY_INTERPRETER_WRAPPER_HH
#define COLA_PY_INTERPRETER_WRAPPER_HH

#include <memory>
#include <string>
#include <unordered_map>

namespace pybind11 {
  class object;
}  // namespace pybind11

namespace cola::python {
  class PythonFilterBase {
   public:
    PythonFilterBase(const std::string& import_path, const std::unordered_map<std::string, std::string>& meta_data);

   protected:
    pybind11::object& Object() { return *imported_object_; }

   private:
    struct PythonInterpreterState;

    static std::unique_ptr<PythonInterpreterState> impl_;

    // default deleter fails for forward-declared classes
    struct PyObjectDeleter {
      void operator()(pybind11::object* ptr) const;
    };
    std::unique_ptr<pybind11::object, PyObjectDeleter> imported_object_;
  };
}  // namespace cola::python

#endif  // COLA_PY_INTERPRETER_WRAPPER_HH
