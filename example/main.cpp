#include <COLA.hh>

int main() {
  auto module = cola::LoadModule("COLA-Py");
  cola::MetaProcessor meta_processor(std::move(module->GetModuleFilters()));

  cola::ColaRunManager manager(meta_processor.Parse("data/config.xml"));
  manager.Run();
}
