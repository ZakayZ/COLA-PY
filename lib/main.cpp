#include "factory.hh"
#include <COLA.hh>

int main() {
    auto factory = cola::python::PythonWriterFactory();
    std::map<std::string, std::string> config;
    config["class"] = "pylib.TestWriter";
    auto ptr = reinterpret_cast<cola::VWriter*>(factory.create(config));
    ptr->operator()(std::make_unique<cola::EventData>());
    delete ptr;
}
