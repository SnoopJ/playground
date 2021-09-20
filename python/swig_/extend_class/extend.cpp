#include <iostream>
#include <unordered_map>
#include "extend.hpp"

using MyMap = std::unordered_map<std::string, int>;

MyMap* Foo::get_bar()
{
  return &m_mymap;
}

int main(int argc, char** argv)
{
    Foo f;
    f.get_bar()->insert({"taco", 42});
    std::cout << "Hello there!\n";
    for ( auto& val : *(f.get_bar()) ) {
      std::cout << val.first << ": " << val.second << "\n";
    }
}
