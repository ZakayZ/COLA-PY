#include <COLA.hh>
#include <COLA-Py/factory.hh>

int main() {
    cola::MetaProcessor metaProcessor;
    metaProcessor.reg(std::unique_ptr<cola::VFactory>(new cola::python::PythonGeneratorFactory), "py_generator", cola::FilterType::generator);
    metaProcessor.reg(std::unique_ptr<cola::VFactory>(new cola::python::PythonConverterFactory), "py_converter", cola::FilterType::converter);
    metaProcessor.reg(std::unique_ptr<cola::VFactory>(new cola::python::PythonWriterFactory), "py_writer", cola::FilterType::writer);

    cola::ColaRunManager manager(metaProcessor.parse("data/config.xml"));
    manager.run();
}
