#include <iostream>
#include <memory>
#include "foo.hpp"

int Foo::bar(std::shared_ptr<int> x)
{
    std::cout << "Value at the end of the pointer: " << *x << "\n";
    (*x)++;
    return 42;
}

int main(int argv, char** argc)
{
    Foo f;
    Foo g;
    int kVal = -1;
    auto pVal = std::make_shared<int>(kVal);
    f.bar(pVal);
    g.bar(pVal);
    f.bar(pVal);
    return 0;
}
