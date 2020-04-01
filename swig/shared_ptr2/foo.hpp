#include <memory>


struct FooInt {
  int value;
  FooInt(int n) : value(n) {}

};


bool munge_num(std::shared_ptr<FooInt> n);
