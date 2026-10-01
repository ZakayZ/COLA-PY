#ifndef COLA_PY_FILTERS_HH
#define COLA_PY_FILTERS_HH

#include "interpreter_wrapper.hh"

#include <COLA.hh>

namespace cola::python {
  class PythonConverter : public VConverter, public VTimedConverter, private PythonFilterBase {
   public:
    PythonConverter(const std::string& import_path, const std::unordered_map<std::string, std::string>& meta_data);

    std::unique_ptr<EventData> operator()(std::unique_ptr<EventData>&& data) override;

    std::uint64_t LastCallbackNanoseconds() const override { return last_callback_nanoseconds_; }

   private:
    std::uint64_t last_callback_nanoseconds_{};
  };

  class PythonGenerator : public VGenerator, private PythonFilterBase {
   public:
    PythonGenerator(const std::string& import_path, const std::unordered_map<std::string, std::string>& meta_data);

    std::unique_ptr<EventData> operator()() override;
  };

  class PythonUnsafeConverter : public VConverter, public VTimedConverter, private PythonFilterBase {
   public:
    PythonUnsafeConverter(const std::string& import_path,
                          const std::unordered_map<std::string, std::string>& meta_data);

    std::unique_ptr<EventData> operator()(std::unique_ptr<EventData>&& data) override;

    std::uint64_t LastCallbackNanoseconds() const override { return last_callback_nanoseconds_; }

   private:
    std::uint64_t last_callback_nanoseconds_{};
  };

  class PythonUnsafeGenerator : public VGenerator, private PythonFilterBase {
   public:
    PythonUnsafeGenerator(const std::string& import_path,
                          const std::unordered_map<std::string, std::string>& meta_data);

    std::unique_ptr<EventData> operator()() override;
  };

  class PythonWriter : public VWriter, private PythonFilterBase {
   public:
    PythonWriter(const std::string& import_path, const std::unordered_map<std::string, std::string>& meta_data);

    void operator()(std::unique_ptr<EventData>&& data) override;
  };
}  // namespace cola::python

#endif  // COLA_PY_FILTERS_HH
