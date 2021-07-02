%module foo

%{
  #include <iostream>
  #include "foo.hpp"
%}

%ignore *::bar(int, int);

%include "foo.hpp"

%extend baz::Foo {
  void new_bar(int a, int b) {
    std::cout << "Hi from the wrapper\n";
  }
 }
