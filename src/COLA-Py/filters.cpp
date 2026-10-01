#include "filters.hh"

#include <pybind11/cast.h>
#include <pybind11/pybind11.h>  // NOLINT(misc-include-cleaner) symbols for cast (e.g. keep_alive_impl)

#include <chrono>

using namespace cola::python;
// NOLINTNEXTLINE(misc-unused-alias-decls)
namespace py = pybind11;

PythonConverter::PythonConverter(const std::string& import_path,
                                 const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonConverter::operator()(std::unique_ptr<cola::EventData>&& data) {
  auto event = py::cast(std::move(data));
  const auto start = std::chrono::steady_clock::now();
  auto result = Object()(event);
  last_callback_nanoseconds_ =
      std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - start).count();
  return std::make_unique<cola::EventData>(result.cast<cola::EventData>());
}

PythonGenerator::PythonGenerator(const std::string& import_path,
                                 const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonGenerator::operator()() {
  return Object()().cast<std::unique_ptr<cola::EventData>>();
}

PythonUnsafeConverter::PythonUnsafeConverter(const std::string& import_path,
                                             const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonUnsafeConverter::operator()(std::unique_ptr<cola::EventData>&& data) {
  auto event = py::cast(data.get(), py::return_value_policy::reference);
  const auto start = std::chrono::steady_clock::now();
  Object()(event);
  last_callback_nanoseconds_ =
      std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - start).count();
  return std::move(data);
}

PythonUnsafeGenerator::PythonUnsafeGenerator(const std::string& import_path,
                                             const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

std::unique_ptr<cola::EventData> PythonUnsafeGenerator::operator()() {
  auto data = std::make_unique<cola::EventData>();
  Object()(py::cast(data.get(), py::return_value_policy::reference));
  return data;
}

PythonWriter::PythonWriter(const std::string& import_path,
                           const std::unordered_map<std::string, std::string>& meta_data)
    : PythonFilterBase(import_path, meta_data) {}

void PythonWriter::operator()(std::unique_ptr<cola::EventData>&& data) { Object()(py::cast(std::move(data))); }
