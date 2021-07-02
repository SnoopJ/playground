#include <utility>
#include <iostream>

class Foo {
public:
  Foo(){};
  explicit Foo(int&& v)
  {
    x = &v; std::cout << "In constructor, x=" << x, "*x=" << *x << "\n";
  }
  ~Foo(){};

  // remove every copy constructor, because e.g. Foo is a resource that
  // can't (or shouldn't) be copied
  Foo(const Foo&) = delete;
  Foo& operator=(const Foo&) = delete;
  Foo& operator=(Foo&& other) = delete;

  // define a move constructor; it's safe to take ownership of
  // the other object's pointer to the data if we also invalidate the
  // other reference by assigning NULL
  Foo(Foo&& other) {
    std::cout << "In move constructor (before), x=" << x << ", *(x)=" << *(x) << "\n";
    std::cout << "In move constructor (before), other.x=" << other.x << ", *(other.x)=" << *(other.x) << "\n";
    x = other.x;
    other.x = NULL;
    std::cout << "In move constructor (after), x=" << x << ", *(x)=" << *(x) << "\n";
    std::cout << "In move constructor (after), other.x=" << other.x << "\n";
  }
  
  int* x;
};

void frobnicate(Foo f)
{
  std::cout << "I'm frobnicate()ing with Foo(x=" << *(f.x) << ")!\n";
}

int main(int argc, char** argv)
{
  Foo f{42};
  frobnicate(std::move(f));
}
