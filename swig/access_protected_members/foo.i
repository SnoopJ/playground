%module foo

%{
#include "foo.hpp"
%}

%ignore Foo;

%include foo.hpp

//%{
//namespace mine {
//using _Foo = Foo;
//class Foo : private _Foo {
//    public:
//        int baz() {
//            return m_secret;
//        }
//};
//}
//%}

namespace mine{
class Foo : private _Foo {
    public:
        int baz() {
            return m_secret;
        }
};
}
