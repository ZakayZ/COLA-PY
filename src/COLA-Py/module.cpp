#include "module.hh"

extern "C" cola::VModule* LoadCOLAModule() { return new cola::python::COLAPyModule(); }
