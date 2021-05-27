%module lib

%{
#include <iostream>
#include "lib.hpp"
%}

// This renaming causes generation of two classes in the target language
//    lib.Foo - wraps FooWrap
//    lib._real_Foo - wraps Foo

%rename("_real_Foo") Foo;
%rename("Foo") FooWrap;

// NOTE: _real_Foo will have a wrapper in the resulting module
// I'm not sure if there's a way to keep SWIG from generating *any* target
// language code for the base class. This spelling emits Python code like:
//      class _real_Foo(object):
//          ...
//
//      # Register _real_Foo in _lib:
//      _lib._real_Foo_swigregister(_real_Foo)
//
//      class Foo(_real_Foo):
//          ...
//      # Register Foo in _lib:
//      _lib.Foo_swigregister(Foo)
//
// The %ignore directive is the intuitive thing to try, and this does keep
// the base class from getting a target language wrapper, but it also means
// the derived class wrapper doesn't have any of the inherited functionality.
//
// I'm mostly searching for a way to relax an access specifier on a base class
// here, so in practice this isn't a problem for me.

%include "lib.hpp"

%inline %{
class FooWrap : public Foo {
    public:
        // C++11 would allow us to inherit Foo's constructor(s) by declaring
        // `using Foo::Foo` here, but SWIG can't keep track of that and codegen
        // goes awry. So instead we have to explicitly declare the deferral of
        // each constructor to the base class
        FooWrap() : Foo() {};
        FooWrap(int val) : Foo(val) {};

        void set_data(int val) {
            std::cout << "Inside derived setter\n";
            Foo::set_data(val);
        }
};
%}
