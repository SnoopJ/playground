#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

bool is_valid1(const std::string& s);
bool is_valid2(const std::string& s);
void partone();
void parttwo();

int main()
{
	partone();
	parttwo();
}

void partone()
{
	std::ifstream infile("input.txt", std::ios::in);
	std::string line;
	int numvalid = 0;
	while (std::getline(infile, line))
	{
		if (is_valid1(line))
		{
			numvalid += 1;
		}
	}
	std::cout << "Part one: " << numvalid << " valid passwords" << std::endl;
}

void parttwo()
{
	std::ifstream infile("input.txt", std::ios::in);
	std::string line;
	int numvalid = 0;
	while (std::getline(infile, line))
	{
		if (is_valid2(line))
		{
			numvalid += 1;
		}
	}
	std::cout << "Part two: " << numvalid << " valid passwords" << std::endl;
}

bool is_valid1(const std::string& line)
{
	auto dashpos = line.find("-");
	auto spacepos = line.find(" ", dashpos);
	auto colonpos = line.find(":", spacepos);
	int min = std::stoi(line.substr(0, dashpos));
	int max = std::stoi(line.substr(dashpos+1, spacepos));
	const char c = line[spacepos+1];

	int num = std::count(line.begin() + colonpos+2, line.end(), c);

	if (min <= num && num <= max)
	{
// 		std::cout << "valid: \t" << line << std::endl;
		return true;
	} else {
// 		std::cout << "invalid: \t" << line << std::endl;
// 		std::cout << std::quoted(line.substr(colonpos+2)) << " is invalid (" << min << "-" << max << " of " << c << ", found " << num << ")" << std::endl;
		return false;
	}
}

bool is_valid2(const std::string& line)
{
	auto dashpos = line.find("-");
	auto spacepos = line.find(" ", dashpos);
	auto colonpos = line.find(":", spacepos);
	int first = std::stoi(line.substr(0, dashpos)) - 1;
	int second = std::stoi(line.substr(dashpos+1, spacepos)) - 1;

	auto passwd = line.substr(colonpos+2);
	const char c = line[spacepos+1];

	std::cout << c << ", " << passwd[first] << ", " << passwd[second] << std::endl;
	if ( (passwd[first] == c && passwd[second] != c) || (passwd[first] != c && passwd[second] == c) )
	{
		return true;
	} else {
		return false;
	}
}
