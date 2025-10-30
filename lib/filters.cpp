#include "filters.hh"

#include <pybind11/pybind11.h>

using namespace cola::python;
namespace py = pybind11;

PythonConverter::PythonConverter(
    const std::string_view importPath,
    const std::map<std::string, std::string>& metaData
)
    : PythonFilterBase(importPath, metaData)
{
}

std::unique_ptr<cola::EventData> PythonConverter::operator()(std::unique_ptr<cola::EventData>&& data) {
    return std::make_unique<cola::EventData>(object()(py::cast(std::move(data))).cast<cola::EventData>());
}

PythonGenerator::PythonGenerator(
    const std::string_view importPath,
    const std::map<std::string, std::string>& metaData
)
    : PythonFilterBase(importPath, metaData)
{
}

std::unique_ptr<cola::EventData> PythonGenerator::operator()() {
    return std::make_unique<cola::EventData>(object()().cast<cola::EventData>());
}

PythonWriter::PythonWriter(
    const std::string_view importPath,
    const std::map<std::string, std::string>& metaData
)
    : PythonFilterBase(importPath, metaData)
{
}

void PythonWriter::operator()(std::unique_ptr<cola::EventData>&& data) {
    object()(py::cast(std::move(data)));
}
