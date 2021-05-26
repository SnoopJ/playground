%module lib

%{
#include <iostream>
#include "lib.hpp"
%}


%include "lib.hpp"

%inline %{
class FooWrap : public Foo {
  public:
        void set_data(int val) {
            std::cout << "Inside derived setter\n";
            Foo::set_data(val);
        }
};
%}
