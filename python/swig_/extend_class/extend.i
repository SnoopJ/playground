%module extend


%{
#include <iostream>
#include <unordered_map>
#include "extend.hpp"

class FooWrap : public Foo {
  public:
    void munge_map() {
      m_mymap.insert({"o frabjous day!", -1});
    };
}

%}

%typemap(out) std::unordered_map<std::string, int>*
{
  auto* res = PyDict_New();
  auto& inpt = *$1;
  for ( auto& v : inpt ) {
    PyDict_SetItemString(res, v.first.c_str(), PyInt_FromLong((long) v.second));
  }

  $result = res;
}


