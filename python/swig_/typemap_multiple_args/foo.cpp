#include <iostream>
#include "foo.hpp"

int Foo::bar()
{
    return 42;
}

bool munge(Foo& f, int x)
{
  std::cout << "Foo value: " << f.value << "\n";
  std::cout << "Some value: " << x << "\n";
}


int main(int argv, char** argc)
{
    return 0;
}
