#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/attr.h>
#include <pybind11/native_enum.h>

#include <COLA.hh>

#include <sstream>
#include <memory>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(_cola_impl, m) {
    m.doc() = "COLA wrapper library";

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif

    py::native_enum<cola::ParticleClass>(m, "ParticleClass", "enum.Enum")
        .value("PRODUCED", cola::ParticleClass::produced)
        .value("ELASTIC_A", cola::ParticleClass::elasticA)
        .value("ELASTIC_B", cola::ParticleClass::elasticB)
        .value("NON_ELASTIC_A", cola::ParticleClass::nonelasticA)
        .value("NON_ELASTIC_B", cola::ParticleClass::nonelasticB)
        .value("SPECTATOR_A", cola::ParticleClass::spectatorA)
        .value("SPECTATOR_B", cola::ParticleClass::spectatorB)
        .export_values()
        .finalize()
        ;

    py::class_<cola::LorentzVector>(m, "LorentzVector")
        .def(py::init<double, double, double, double>(), "e"_a = 0., "x"_a = 0., "y"_a = 0., "z"_a = 0.)
        .def(py::init<cola::LorentzVector>())
        .def_readwrite("x", &cola::LorentzVector::x, "x vector component")
        .def_readwrite("y", &cola::LorentzVector::y, "y vector component")
        .def_readwrite("z", &cola::LorentzVector::z, "z vector component")
        .def_readwrite("e", &cola::LorentzVector::e, "e vector component")
        .def_readwrite("t", &cola::LorentzVector::t, "t vector component")
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def(py::self += py::self)
        .def(py::self -= py::self)
        .def(py::self *= double())
        .def(py::self /= double())
        .def(double() * py::self)
        .def(py::self * double())
        .def(py::self / double())
        .def(py::self == py::self)
        // .def(-py::self)
        .def("__copy__", [](const cola::LorentzVector& vec) {
            return vec;
        })
        .def("__deepcopy__", [](const cola::LorentzVector& vec, py::dict) {
            return vec;
        }, "memo"_a)
        .def("__repr__", [](const cola::LorentzVector& p) -> std::string {
            auto ss = std::stringstream();
            ss << p;
            return std::move(ss).str();
        })
        ;

    py::class_<cola::Particle>(m, "Particle")
        .def(py::init<cola::LorentzVector, cola::LorentzVector, int, cola::ParticleClass>(),
            "position"_a, "momentum"_a, "pdg_code"_a, "p_class"_a)
        .def(py::init<cola::Particle>())
        .def_readwrite("position", &cola::Particle::position)
        .def_readwrite("momentum", &cola::Particle::momentum)
        .def_readwrite("pdg_code", &cola::Particle::pdgCode)
        .def_readwrite("p_class", &cola::Particle::pClass)
        .def("get_az", [](const cola::Particle& p) -> std::pair<int, int> { return p.getAZ(); })
        .def("__repr__", [](const cola::Particle& p) -> std::string {
            auto ss = std::stringstream();
            ss << "Particle(pdg=" << p.pdgCode << ", class=" << static_cast<int>(p.pClass) << ")";
            return std::move(ss).str();
        })
        ;

    py::class_<cola::EventIniState>(m, "EventInitialState")
        .def(py::init<>())
        .def_readwrite("pdg_code_a", &cola::EventIniState::pdgCodeA,
                      "PDG code of the projectile")
        .def_readwrite("pdg_code_b", &cola::EventIniState::pdgCodeB,
                      "PDG code of the target")
        .def_readwrite("pz_a", &cola::EventIniState::pZA,
                      "Axial momentum of the projectile")
        .def_readwrite("pz_b", &cola::EventIniState::pZB,
                      "Axial momentum of the target")
        .def_readwrite("energy", &cola::EventIniState::energy,
                      "Incident energy of the event")
        .def_readwrite("sect_nn", &cola::EventIniState::sectNN,
                      "Nucleon-Nucleon cross section from generator")
        .def_readwrite("b", &cola::EventIniState::b,
                      "Impact parameter of the event")
        .def_readwrite("n_coll", &cola::EventIniState::nColl,
                      "Total number of collisions")
        .def_readwrite("n_coll_pp", &cola::EventIniState::nCollPP,
                      "Number of proton-proton collisions")
        .def_readwrite("n_coll_pn", &cola::EventIniState::nCollPN,
                      "Number of proton-neutron collisions")
        .def_readwrite("n_coll_nn", &cola::EventIniState::nCollNN,
                      "Number of neutron-neutron collisions")
        .def_readwrite("n_part", &cola::EventIniState::nPart,
                      "Total number of participants")
        .def_readwrite("n_part_a", &cola::EventIniState::nPartA,
                      "Number of participants from projectile nucleus")
        .def_readwrite("n_part_b", &cola::EventIniState::nPartB,
                      "Number of participants from target nucleus")
        .def_readwrite("phi_rot_a", &cola::EventIniState::phiRotA,
                      "Polar angle φ of rotation of projectile nucleon")
        .def_readwrite("theta_rot_a", &cola::EventIniState::thetaRotA,
                      "Polar angle Θ of rotation of projectile nucleon")
        .def_readwrite("phi_rot_b", &cola::EventIniState::phiRotB,
                      "Polar angle φ of rotation of target nucleon")
        .def_readwrite("theta_rot_b", &cola::EventIniState::thetaRotB,
                      "Polar angle Θ of rotation of target nucleon")
        .def_readwrite("initial_particles", &cola::EventIniState::iniStateParticles,
                      "Array of all particles just before the event")
        ;

    py::class_<cola::EventData>(m, "EventData")
        .def(py::init<>())
        .def_readwrite("initial_state", &cola::EventData::iniState)
        .def_readwrite("particles", &cola::EventData::particles);
}
