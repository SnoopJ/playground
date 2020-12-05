#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

#include "common.h"
#include "PassportInfo.h"

int
main(int argc, char* argv[])
{
	std::vector<std::string> input;
	try {
		input = Acme::load_input(argc, argv);
	} catch(...) {
		return 1;
	}

    auto passports = Acme::parseInfo(input);
    std::cout << passports.size() << " passports parsed" << std::endl;

    auto nump1 = std::count_if(passports.begin(), passports.end(), [](Acme::PassportInfo& p) { return p.allParams(); });
	std::cout << "Part one: " << nump1 << " passports with all required fields defined" << std::endl;

    auto nump2 = std::count_if(passports.begin(), passports.end(), [](Acme::PassportInfo& p) { return p.valid(); });
	std::cout << "Part two: " << nump2 << " passports with all fields validated" << std::endl;

	return 0;
}
