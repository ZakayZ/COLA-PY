#pragma once

#include "interpreter_wrapper.hh"

#include <COLA.hh>

namespace cola::python {
    class PythonConverter: public VConverter, private PythonFilterBase {
        public:
            PythonConverter(const std::string_view importPath, const std::map<std::string, std::string>& metaData);

            std::unique_ptr<EventData> operator()(std::unique_ptr<EventData>&& data) override;
    };

    class PythonGenerator: public VGenerator, private PythonFilterBase {
        public:
            PythonGenerator(const std::string_view importPath, const std::map<std::string, std::string>& metaData);

            std::unique_ptr<EventData> operator()() override;
    };

    class PythonWriter: public VWriter, private PythonFilterBase {
        public:
            PythonWriter(const std::string_view importPath, const std::map<std::string, std::string>& metaData);

            void operator()(std::unique_ptr<EventData>&& data) override;
    };
} // namespace cola::python
