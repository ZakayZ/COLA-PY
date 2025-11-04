#pragma once

#include "COLA.hh"

namespace cola {
    class COLAPyPlugin : public VPluginLibrary {
    public:
        FilterMap getLibraryFilters() const override;
    };
} // namespace cola
