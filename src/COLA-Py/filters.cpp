#include "filters.hh"

#include <pybind11/cast.h>
#include <pybind11/pybind11.h>  // NOLINT(misc-include-cleaner) symbols for cast (e.g. keep_alive_impl)

using namespace cola::python;
// NOLINTNEXTLINE(misc-unused-alias-decls)
namespace py = pybind11;

PythonConverter::PythonConverter(const std::string& import_path,
                                 const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonConverter::operator()(std::unique_ptr<cola::EventData>&& data) {
  return std::make_unique<cola::EventData>(Object()(py::cast(std::move(data))).cast<cola::EventData>());
}

PythonGenerator::PythonGenerator(const std::string& import_path,
                                 const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonGenerator::operator()() {
  return std::make_unique<cola::EventData>(Object()().cast<cola::EventData>());
}

PythonWriter::PythonWriter(const std::string& import_path,
                           const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

void PythonWriter::operator()(std::unique_ptr<cola::EventData>&& data) { Object()(py::cast(std::move(data))); }
