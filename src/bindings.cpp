#include <COLA.hh>
#include <pybind11/attr.h>        // NOLINT(misc-include-cleaner)
#include <pybind11/functional.h>  // NOLINT(misc-include-cleaner)
#include <pybind11/native_enum.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // NOLINT(misc-include-cleaner)

#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace pybind11::literals;

class COLAPyRunManager {
 public:
  COLAPyRunManager() = default;

  COLAPyRunManager& LoadModule(const std::string& library_path, const std::string& library_prefix = "") {
    auto plugin =
        cola::LoadModule(library_path, !library_prefix.empty() ? std::make_optional(library_prefix) : std::nullopt);
    for (auto& [name, factory] : plugin->GetModuleFilters()) {
      meta_processor_.Register(std::move(factory), name);
    }
    return *this;
  }

  COLAPyRunManager& LoadConfigFile(const std::string& config_path) {
    cola_manager_.emplace(meta_processor_.Parse(config_path));
    return *this;
  }

  COLAPyRunManager& LoadConfigString(const std::string& config_xml) {
    std::istringstream stream(config_xml);
    cola_manager_.emplace(meta_processor_.Parse(stream));
    return *this;
  }

  void Run(int n) {
    if (cola_manager_.has_value()) {
      cola_manager_->Run(n);
    } else {
      throw std::runtime_error("The COLAPyRunManager wasn't initialized");
    }
  }

 private:
  cola::MetaProcessor meta_processor_;
  std::optional<cola::ColaRunManager> cola_manager_;
};

PYBIND11_MODULE(_cola_impl, mod) {
  mod.doc() = "COLA wrapper library";

#ifdef VERSION_INFO
  mod.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  mod.attr("__version__") = "dev";
#endif

  py::native_enum<cola::ParticleClass>(mod, "ParticleClass", "enum.Enum")
      .value("PRODUCED", cola::ParticleClass::kProduced)
      .value("ELASTIC_A", cola::ParticleClass::kElasticA)
      .value("ELASTIC_B", cola::ParticleClass::kElasticB)
      .value("NON_ELASTIC_A", cola::ParticleClass::kNonelasticA)
      .value("NON_ELASTIC_B", cola::ParticleClass::kNonelasticB)
      .value("SPECTATOR_A", cola::ParticleClass::kSpectatorA)
      .value("SPECTATOR_B", cola::ParticleClass::kSpectatorB)
      .export_values()
      .finalize();

  py::class_<cola::LorentzVector>(mod, "LorentzVector")
      .def(py::init<double, double, double, double>(), "e"_a = 0., "x"_a = 0., "y"_a = 0., "z"_a = 0.)
      .def(py::init<cola::LorentzVector>())
      .def_readwrite("x", &cola::LorentzVector::x, "x vector component")
      .def_readwrite("y", &cola::LorentzVector::y, "y vector component")
      .def_readwrite("z", &cola::LorentzVector::z, "z vector component")
      .def_readwrite("e", &cola::LorentzVector::e, "e vector component")
      .def_readwrite("t", &cola::LorentzVector::t, "t vector component")
      .def(py::self + py::self)
      .def(py::self - py::self)  // NOLINT(misc-redundant-expression)
      .def(py::self += py::self)
      .def(py::self -= py::self)
      .def(py::self *= double())
      .def(py::self /= double())
      .def(double() * py::self)
      .def(py::self * double())
      .def(py::self / double())
      .def(py::self == py::self)  // NOLINT(misc-redundant-expression)
      // .def(-py::self)
      .def("__copy__", [](const cola::LorentzVector& vec) { return vec; })
      .def(
          "__deepcopy__", [](const cola::LorentzVector& vec, const py::dict&) { return vec; }, "memo"_a)
      .def("__repr__", [](const cola::LorentzVector& particle) -> std::string {
        auto ss = std::stringstream();
        ss << particle;
        return std::move(ss).str();
      });

  py::class_<cola::Particle>(mod, "Particle")
      .def(py::init<cola::LorentzVector, cola::LorentzVector, int, cola::ParticleClass>(), "position"_a, "momentum"_a,
           "pdg_code"_a, "p_class"_a)
      .def(py::init<cola::Particle>())
      .def_readwrite("position", &cola::Particle::position)
      .def_readwrite("momentum", &cola::Particle::momentum)
      .def_readwrite("pdg_code", &cola::Particle::pdg_code)
      .def_readwrite("p_class", &cola::Particle::p_class)
      .def("get_az", [](const cola::Particle& particle) -> std::pair<int, int> { return particle.GetAZ(); })
      .def("__repr__", [](const cola::Particle& particle) -> std::string {
        auto ss = std::stringstream();
        ss << "Particle(pdg=" << particle.pdg_code << ", class=" << static_cast<int>(particle.p_class) << ")";
        return std::move(ss).str();
      });

  py::class_<cola::EventIniState>(mod, "EventInitialState")
      .def(py::init<int, int, double, double, double, float, float, int, int, int, int, int, int, int, float, float,
                    float, float, cola::EventParticles>(),
           "pdg_code_a"_a = 0, "pdg_code_b"_a = 0, "pz_a"_a = 0., "pz_b"_a = 0., "energy"_a = 0., "sect_nn"_a = 0.f,
           "b"_a = 0.f, "num_coll"_a = 0, "num_coll_pp"_a = 0, "num_coll_pn"_a = 0, "num_coll_nn"_a = 0,
           "num_part"_a = 0, "num_part_a"_a = 0, "num_part_b"_a = 0, "phi_rot_a"_a = 0.f, "theta_rot_a"_a = 0.f,
           "phi_rot_b"_a = 0.f, "theta_rot_b"_a = 0.f, "ini_state_particles"_a = cola::EventParticles())
      .def_readwrite("pdg_code_a", &cola::EventIniState::pdg_code_a, "PDG code of the projectile")
      .def_readwrite("pdg_code_b", &cola::EventIniState::pdg_code_b, "PDG code of the target")
      .def_readwrite("pz_a", &cola::EventIniState::pz_a, "Axial momentum of the projectile")
      .def_readwrite("pz_b", &cola::EventIniState::pz_b, "Axial momentum of the target")
      .def_readwrite("energy", &cola::EventIniState::energy, "Incident energy of the event")
      .def_readwrite("sect_nn", &cola::EventIniState::sect_nn, "Nucleon-Nucleon cross section from generator")
      .def_readwrite("b", &cola::EventIniState::b, "Impact parameter of the event")
      .def_readwrite("num_coll", &cola::EventIniState::num_coll, "Total number of collisions")
      .def_readwrite("num_coll_pp", &cola::EventIniState::num_coll_pp, "Number of proton-proton collisions")
      .def_readwrite("num_coll_pn", &cola::EventIniState::num_coll_pn, "Number of proton-neutron collisions")
      .def_readwrite("num_coll_nn", &cola::EventIniState::num_coll_nn, "Number of neutron-neutron collisions")
      .def_readwrite("num_part", &cola::EventIniState::num_part, "Total number of participants")
      .def_readwrite("num_part_a", &cola::EventIniState::num_part_a, "Number of participants from projectile nucleus")
      .def_readwrite("num_part_b", &cola::EventIniState::num_part_b, "Number of participants from target nucleus")
      .def_readwrite("phi_rot_a", &cola::EventIniState::phi_rot_a, "Polar angle φ of rotation of projectile nucleon")
      .def_readwrite("theta_rot_a", &cola::EventIniState::theta_rot_a,
                     "Polar angle Θ of rotation of projectile nucleon")
      .def_readwrite("phi_rot_b", &cola::EventIniState::phi_rot_b, "Polar angle φ of rotation of target nucleon")
      .def_readwrite("theta_rot_b", &cola::EventIniState::theta_rot_b, "Polar angle Θ of rotation of target nucleon")
      .def_readwrite("ini_state_particles", &cola::EventIniState::ini_state_particles,
                     "Array of all particles just before the event");

  py::class_<cola::EventData>(mod, "EventData")
      .def(py::init<cola::EventIniState, cola::EventParticles>(), "ini_state"_a = cola::EventIniState(),
           "particles"_a = cola::EventParticles())
      .def_readwrite("ini_state", &cola::EventData::ini_state)
      .def_readwrite("particles", &cola::EventData::particles);

  py::class_<COLAPyRunManager>(mod, "RunManager")
      .def(py::init<>())
      .def("run", &COLAPyRunManager::Run, "n"_a = 1)
      .def("load_module", &COLAPyRunManager::LoadModule, "library_path"_a, "library_prefix"_a = "")
      .def("load_config_file", &COLAPyRunManager::LoadConfigFile, "config_path"_a)
      .def("load_config_xml", &COLAPyRunManager::LoadConfigString, "config_xml"_a);
}
