#include <COLA.hh>

int main() {
    cola::MetaProcessor metaProcessor(cola::loadLibrary("COLA-Py")->getLibraryFilters());

    cola::ColaRunManager manager(metaProcessor.parse("data/config.xml"));
    manager.run();
}
