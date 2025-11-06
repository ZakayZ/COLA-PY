#include <functional>
#include <memory>

#include <COLA.hh>
#include <unordered_map>

#include "factory.hh"
#include "export.hh"

static const std::unordered_map<std::string, std::pair<std::function<cola::VFactory*()>, cola::FilterType>> ModuleFactories = {
    {"PythonWriter", {[](){ return new cola::python::PythonWriterFactory(); }, cola::FilterType::writer}},
    {"PythonConverter", {[](){ return new cola::python::PythonConverterFactory(); }, cola::FilterType::converter}},
    {"PythonGenerator", {[](){ return new cola::python::PythonGeneratorFactory(); }, cola::FilterType::generator}},
};

cola::FilterMap cola::COLAPyPlugin::getLibraryFilters() const {
    cola::FilterMap filterMap;
    for (const auto& [name, factoryData] : ModuleFactories) {
        filterMap[name] = {std::unique_ptr<VFactory>(factoryData.first()), factoryData.second};
    }
    return filterMap;
}

extern "C" cola::VPluginLibrary* loadColaPlugin() {
    return new cola::COLAPyPlugin();
}
