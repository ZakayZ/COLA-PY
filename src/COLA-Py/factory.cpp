#include "factory.hh"

#include "filters.hh"

#include <memory>

using namespace cola::python;

namespace {
  template <typename PythonFilter>
  std::unique_ptr<cola::VFilter> CreatePythonFilter(const std::unordered_map<std::string, std::string>& meta_data) {
    if (auto it = meta_data.find("class"); it != meta_data.end()) {
      return std::make_unique<PythonFilter>(it->second, meta_data);
    }

    throw std::runtime_error("class is not specified for Python Filter");
  }
}  // anonymous namespace

std::unique_ptr<cola::VFilter> PythonGeneratorFactory::Create(
    const std::unordered_map<std::string, std::string>& meta_data) {
  return CreatePythonFilter<PythonGenerator>(meta_data);
}

std::unique_ptr<cola::VFilter> PythonConverterFactory::Create(
    const std::unordered_map<std::string, std::string>& meta_data) {
  return CreatePythonFilter<PythonConverter>(meta_data);
}

std::unique_ptr<cola::VFilter> PythonWriterFactory::Create(
    const std::unordered_map<std::string, std::string>& meta_data) {
  return CreatePythonFilter<PythonWriter>(meta_data);
}
