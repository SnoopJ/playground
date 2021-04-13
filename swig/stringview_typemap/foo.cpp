#include <iostream>
#include <string_view>
#include "foo.hpp"

void print_it(std::string_view s)
{
	std::cout << s << std::endl;
}

std::string_view get_it()
{
	return "猫 nyaa";
}

int main(int argv, char** argc)
{
	print_it(get_it());
	print_it("hey");
	print_it("42");
	print_it("猫");
    return 0;
}
