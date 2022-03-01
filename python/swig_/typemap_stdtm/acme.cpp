#include <iostream>

#include "acme.hpp"


std::tm time_out()
{
	std::tm t{};
	t.tm_sec = 1;
	t.tm_min = 2;
	t.tm_hour = 3;
	t.tm_mday = 4;
	t.tm_mon = 5;
	t.tm_year = 6;
	return t;
}

void time_in(std::tm t)
{
	std::cout << "sec: " << t.tm_sec << "\n";
	std::cout << "min: " << t.tm_min << "\n";
	std::cout << "hour: " << t.tm_hour << "\n";
	std::cout << "mday: " << t.tm_mday << "\n";
	std::cout << "mon: " << t.tm_mon << "\n";
	std::cout << "year: " << t.tm_year << "\n";
}

int main(int argc, char** argv) {
    return 0;
}
