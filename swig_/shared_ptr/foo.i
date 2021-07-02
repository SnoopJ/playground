%module foo

%{
#include "foo.hpp"
%}

%include foo.hpp

%extend Foo {
  int bar(int x) {
    $self->bar(std::make_shared<int>(x));
  }
 }
