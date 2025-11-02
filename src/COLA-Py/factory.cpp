#include "factory.hh"
#include "filters.hh"

using namespace cola::python;

namespace {
    template <typename T>
    cola::VFilter* CreatePythonFilter(const std::map<std::string, std::string>& metaData) {
        if (auto it = metaData.find("class"); it != metaData.end()) {
            return new T(it->second, metaData);
        } else {
            throw std::runtime_error("class is not specified");
        }
    }
} // anonymous namespace

cola::VFilter* PythonGeneratorFactory::create(const std::map<std::string, std::string>& metaData) {
    return CreatePythonFilter<PythonGenerator>(metaData);
}

cola::VFilter* PythonConverterFactory::create(const std::map<std::string, std::string>& metaData) {
    return CreatePythonFilter<PythonConverter>(metaData);
}

cola::VFilter* PythonWriterFactory::create(const std::map<std::string, std::string>& metaData) {
    return CreatePythonFilter<PythonWriter>(metaData);
}
