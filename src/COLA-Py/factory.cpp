#include "factory.hh"

#include "filters.hh"

#include <memory>

using namespace cola::python;

namespace {
  template <typename PythonFilter>
  std::unique_ptr<cola::VFilter> CreatePythonFilter(const std::unordered_map<std::string, std::string>& metaData) {
    if (auto it = metaData.find("class"); it != metaData.end()) {
      return std::make_unique<PythonFilter>(it->second, metaData);
    }

    throw std::runtime_error("class is not specified for Python Filter");
  }
}  // anonymous namespace

std::unique_ptr<cola::VFilter> PythonGeneratorFactory::Create(
    const std::unordered_map<std::string, std::string>& metaData) {
  return CreatePythonFilter<PythonGenerator>(metaData);
}

std::unique_ptr<cola::VFilter> PythonConverterFactory::Create(
    const std::unordered_map<std::string, std::string>& metaData) {
  return CreatePythonFilter<PythonConverter>(metaData);
}

std::unique_ptr<cola::VFilter> PythonWriterFactory::Create(
    const std::unordered_map<std::string, std::string>& metaData) {
  return CreatePythonFilter<PythonWriter>(metaData);
}
