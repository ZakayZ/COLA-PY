#include "interpreter_wrapper.hh"

#include <pybind11/embed.h>

#include <memory>
#include <string>
#include <unordered_map>

using namespace cola::python;
namespace py = pybind11;

namespace cola::python::detail {
  struct PythonInterpreterState {
    PythonInterpreterState() {
      if (Py_IsInitialized() == 0) {
        guard_ = std::make_unique<py::scoped_interpreter>();
      }
    }

    std::unique_ptr<pybind11::scoped_interpreter> guard_;
  };
}  // namespace cola::python::detail

std::unique_ptr<detail::PythonInterpreterState> PythonFilterBase::impl = nullptr;

void PythonFilterBase::PyObjectDeleter::operator()(pybind11::object* ptr) const { delete ptr; }

namespace {
  py::object ImportFrom(const std::string& importPath) {
    auto lastDot = importPath.rfind('.');
    if (lastDot == std::string_view::npos) {
      if (pybind11::globals().contains(importPath.c_str())) {
        return pybind11::globals()[importPath.c_str()];
      }
      return py::module_::import(importPath.c_str());
    }

    const auto modulePath = importPath.substr(0, lastDot);
    const auto objectName = importPath.substr(lastDot + 1);
    py::module_ module = py::module_::import(modulePath.c_str());

    return module.attr(objectName.c_str());
  }

  py::dict ToPythonDict(const std::unordered_map<std::string, std::string>& map) {
    py::dict pythonMap;
    for (const auto& [key, value] : map) {
      pythonMap[py::str(key)] = py::str(value);
    }
    return pythonMap;
  }
}  // anonymous namespace

PythonFilterBase::PythonFilterBase(const std::string& importPath,
                                   const std::unordered_map<std::string, std::string>& metaData) {
  if (impl == nullptr) {
    impl = std::make_unique<detail::PythonInterpreterState>();
  }

  importedObject_ =
      std::unique_ptr<py::object, PyObjectDeleter>(new py::object(ImportFrom(importPath)(**ToPythonDict(metaData))));
}
