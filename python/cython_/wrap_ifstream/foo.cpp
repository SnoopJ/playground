#include <iostream>
#include <string>

std::ifstream load(const std::string& fn)
{
	return std::ifstream(fn);
}
