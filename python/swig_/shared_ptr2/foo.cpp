#include <iostream>
#include <memory>
#include "foo.hpp"

bool munge_num(std::shared_ptr<FooInt> n)
{
  std::cout << "Hello from munge_num()! The number passed was: " << (*n).value << "\n";
  return true;
}

int main(int argc, char** argv)
{
  auto mynum = FooInt(42);
  auto myptr = std::make_shared<FooInt>(mynum);
  munge_num(myptr);
}
