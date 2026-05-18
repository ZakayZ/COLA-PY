#pragma once

#include <COLA.hh>

#include <memory>

namespace cola::python {

  class PythonGeneratorFactory : public cola::VGeneratorFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string NAME = "PythonGenerator";
      return NAME;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& metaData) final;
  };

  class PythonConverterFactory : public cola::VConverterFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string NAME = "PythonConverter";
      return NAME;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& metaData) final;
  };

  class PythonWriterFactory : public cola::VWriterFactory {
   public:
    const std::string& GetFilterName() const override {
      static const std::string NAME = "PythonWriter";
      return NAME;
    }

    std::unique_ptr<cola::VFilter> Create(const std::unordered_map<std::string, std::string>& metaData) final;
  };

}  // namespace cola::python
