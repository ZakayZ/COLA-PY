#pragma once

#include <map>
#include <memory>
#include <string>

namespace pybind11 {
    class object;
} // namespace pybind11

namespace cola::python {
    class PythonFilterBase {
        public:
            PythonFilterBase(const std::string_view importPath, const std::map<std::string, std::string>& metaData);

        protected:
            pybind11::object& object() {
                return *importedObject_;
            }

        private:
            std::unique_ptr<pybind11::object> importedObject_;

            class PythonHolder;
            static std::unique_ptr<PythonHolder> impl_;
    };
} // namespace cola::python
