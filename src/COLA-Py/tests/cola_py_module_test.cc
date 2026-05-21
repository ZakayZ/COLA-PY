#include <COLA-Py/module.hh>
#include <COLA.hh>
#include <gtest/gtest.h>
#include <pybind11/embed.h>

#include <memory>
#include <sstream>

namespace py = pybind11;

namespace {

  void EnsurePythonInterpreter() {
    static std::unique_ptr<py::scoped_interpreter> interpreter;
    if (interpreter == nullptr) {
      interpreter = std::make_unique<py::scoped_interpreter>();
    }
  }

  void SetupTestPythonPath() {
    static bool initialized = false;
    if (initialized) {
      return;
    }

    EnsurePythonInterpreter();
    py::module_::import("colapy");

    py::module_ sys = py::module_::import("sys");
    sys.attr("path").cast<py::list>().append(COLA_PY_TEST_DIR);
    py::module_::import("pylib");

    initialized = true;
  }

  cola::FactoryMap ModuleFactories() {
    cola::python::COLAPyModule module;
    return module.GetModuleFilters();
  }

}  // namespace

TEST(COLAPyModuleTest, ModuleExposesNamedFactories) {
  const cola::FactoryMap factories = ModuleFactories();

  ASSERT_NE(factories.find("PythonGenerator"), factories.end());
  ASSERT_NE(factories.find("PythonConverter"), factories.end());
  ASSERT_NE(factories.find("PythonWriter"), factories.end());
}

TEST(COLAPyModuleTest, CreateFilterThrowsWithoutClass) {
  EnsurePythonInterpreter();
  cola::python::PythonGeneratorFactory factory;
  EXPECT_THROW(factory.Create({{"name", "PythonGenerator"}}), std::runtime_error);
}

TEST(COLAPyModuleTest, GeneratorProducesParticle) {
  SetupTestPythonPath();

  cola::python::COLAPyModule module;
  cola::MetaProcessor processor(module.GetModuleFilters());
  std::istringstream stream(R"(<?xml version="1.0"?>
<program>
    <generator name="PythonGenerator" class="pylib.Generator"/>
    <converter name="PythonConverter" class="pylib.Converter"/>
    <writer name="PythonWriter" class="pylib.Writer"/>
</program>
)");
  cola::FilterEnsemble ensemble = processor.Parse(stream);
  ASSERT_NE(ensemble.generator, nullptr);

  auto event = (*ensemble.generator)();
  ASSERT_NE(event, nullptr);
  ASSERT_EQ(event->particles.size(), 1u);
  EXPECT_FLOAT_EQ(event->particles[0].momentum.e, 10.0f);
}

TEST(COLAPyModuleTest, FiltersProcessKwargsFromXml) {
  SetupTestPythonPath();

  cola::python::COLAPyModule module;
  cola::MetaProcessor processor(module.GetModuleFilters());
  std::istringstream stream(R"(<?xml version="1.0"?>
<program>
    <generator name="PythonGenerator" class="pylib.Generator"
               pdg_a="42" pdg_b="2212" momentum_e="3.0"/>
    <converter name="PythonConverter" class="pylib.Converter" delta_e="7.0"/>
    <writer name="PythonWriter" class="pylib.Writer"/>
</program>
)");
  cola::FilterEnsemble ensemble = processor.Parse(stream);
  ASSERT_NE(ensemble.generator, nullptr);
  ASSERT_GT(ensemble.converters.size(), 0);

  auto event = (*ensemble.generator)();
  ASSERT_NE(event, nullptr);
  EXPECT_EQ(event->ini_state.pdg_code_a, 42);
  EXPECT_EQ(event->ini_state.pdg_code_b, 2212);
  EXPECT_FLOAT_EQ(event->particles[0].momentum.e, 3.0f);

  auto converted = (*ensemble.converters[0])(std::move(event));
  ASSERT_NE(converted, nullptr);
  EXPECT_FLOAT_EQ(converted->particles[0].momentum.e, 10.0f);
}
