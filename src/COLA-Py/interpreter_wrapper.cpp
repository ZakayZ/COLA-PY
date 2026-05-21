#include "interpreter_wrapper.hh"

#include <pybind11/embed.h>

#include <memory>
#include <string>
#include <unordered_map>

using namespace cola::python;
namespace py = pybind11;

#if defined(__GNUC__) || defined(__clang__)
#define COLA_PY_LOCAL __attribute__((visibility("hidden")))
#else
#define COLA_PY_LOCAL
#endif

struct COLA_PY_LOCAL PythonFilterBase::PythonInterpreterState {
  PythonInterpreterState() {
    if (Py_IsInitialized() == 0) {
      guard = std::make_unique<py::scoped_interpreter>();
    }
  }

  std::unique_ptr<pybind11::scoped_interpreter> guard;
};

std::unique_ptr<PythonFilterBase::PythonInterpreterState> PythonFilterBase::impl_ = nullptr;

void PythonFilterBase::PyObjectDeleter::operator()(pybind11::object* ptr) const { delete ptr; }

namespace {
  py::object ImportFrom(const std::string& import_path) {
    auto last_dot = import_path.rfind('.');
    if (last_dot == std::string_view::npos) {
      if (pybind11::globals().contains(import_path.c_str())) {
        return pybind11::globals()[import_path.c_str()];
      }
      return py::module_::import(import_path.c_str());
    }

    const auto module_path = import_path.substr(0, last_dot);
    const auto object_name = import_path.substr(last_dot + 1);
    py::module_ module = py::module_::import(module_path.c_str());

    return module.attr(object_name.c_str());
  }

  py::dict ToPythonDict(const std::unordered_map<std::string, std::string>& map) {
    py::dict python_map;
    for (const auto& [key, value] : map) {
      python_map[py::str(key)] = py::str(value);
    }
    return python_map;
  }
}  // anonymous namespace

PythonFilterBase::PythonFilterBase(const std::string& import_path,
                                   const std::unordered_map<std::string, std::string>& meta_data) {
  if (impl_ == nullptr) {
    impl_ = std::make_unique<PythonInterpreterState>();
  }

  imported_object_ =
      std::unique_ptr<py::object, PyObjectDeleter>(new py::object(ImportFrom(import_path)(**ToPythonDict(meta_data))));
}
