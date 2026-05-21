#ifndef COLA_PY_FACTORY_HH
#define COLA_PY_FACTORY_HH

#include <COLA.hh>

#include <memory>

namespace cola::python {

  class PythonGeneratorFactory : public cola::VGeneratorFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string name = "PythonGenerator";
      return name;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& meta_data) final;
  };

  class PythonConverterFactory : public cola::VConverterFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string name = "PythonConverter";
      return name;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& meta_data) final;
  };

  class PythonWriterFactory : public cola::VWriterFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string name = "PythonWriter";
      return name;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& meta_data) final;
  };

}  // namespace cola::python

#endif  // COLA_PY_FACTORY_HH
