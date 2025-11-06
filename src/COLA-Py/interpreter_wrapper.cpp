#include "interpreter_wrapper.hh"

#include <memory>
#include <pybind11/embed.h>
#include <string>

using namespace cola::python;
namespace py = pybind11;

std::unique_ptr<PythonFilterBase::PythonHolder> PythonFilterBase::impl_ = nullptr;

PythonFilterBase::PythonHolder::PythonHolder() {
    if (!Py_IsInitialized()) {
        guard_ = std::make_unique<py::scoped_interpreter>();
    }
}

namespace {
    py::object ImportFrom(const std::string_view importPath) {
        auto last_dot = importPath.rfind('.');
        if (last_dot == std::string_view::npos) {
            if (pybind11::globals().contains(importPath.data())) {
                return pybind11::globals()[importPath.data()];
            }
            return py::module_::import(importPath.data());
        }

        const auto module_path = importPath.substr(0, last_dot);
        const auto object_name = importPath.substr(last_dot + 1);
        py::module_ module = py::module_::import(std::string(module_path).c_str());
        
        return module.attr(std::string(object_name).c_str());
    }

    py::dict ToPythonDict(const std::map<std::string, std::string>& map) {
        py::dict pythonMap;
        for (const auto& [key, value] : map) {
            pythonMap[py::str(key)] = py::str(value);
        }
        return pythonMap;
    }
} // anonymous namespace

PythonFilterBase::PythonFilterBase(const std::string_view importPath, const std::map<std::string, std::string>& metaData) {
    if (impl_ == nullptr) {
        impl_ = std::make_unique<PythonHolder>();
    }

    importedObject_ = std::make_unique<py::object>(ImportFrom(importPath)(**ToPythonDict(metaData)));
}

