#include "extend.hpp"
#include <iostream>

int main(int argc, char** argv)
{
    auto f = Foo();
    auto s = Foo::Bar();
    std::cout << s.x << "\n";
    std::cout << f.y << "\n";
}
