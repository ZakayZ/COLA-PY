#pragma once

#include <COLA.hh>

namespace cola::python {

    class PythonGeneratorFactory: public cola::VFactory {
    public:
        cola::VFilter* create(const std::map<std::string, std::string>&) final;
    };

    class PythonConverterFactory: public cola::VFactory {
    public:
        cola::VFilter* create(const std::map<std::string, std::string>&) final;
    };

    class PythonWriterFactory: public cola::VFactory {
    public:
        cola::VFilter* create(const std::map<std::string, std::string>&) final;
    };

} // namespace cola::python
