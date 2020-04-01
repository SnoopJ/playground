#include <iostream>
#include "foo.hpp"

using namespace baz;

void Foo::bar() {
    std::cout << "Hello from bar()!\n";
}

void Foo::bar(int v) {
    std::cout << "Hello from bar(v) with v=" << v << "!\n";
}

void Foo::bar(int a, int b) {
    std::cout << "Hello from bar(a, b) with a=" << a << ", b=" << b << "!\n";
}

int main(int argc, char** argv)
{
  Foo f;
  f.bar();
  f.bar(42);
}
