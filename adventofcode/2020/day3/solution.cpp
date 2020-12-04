#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

int numtrees(std::vector<std::string>& input, int hstep, int vstep)
{
	int height = input.size();
	int width = input.at(0).size();
	int ntrees = 0;
	auto tree = '#';
	for(int y = 0, x = 0; y < height; y = std::min(y+vstep, height), x = (x+hstep)%width)
	{
		if (input[y][x] == tree)
		{
// 			std::cout << "Encountered tree at (" << x << ", " << y << ")" << std::endl;
			ntrees++;
		}
	}
	return ntrees;
}

std::vector<std::string> load_input(int argc, char* argv[])
{
	if (argc != 2)
	{
		std::cerr << "Usage: " << argv[0] << " input.txt" << std::endl;
		throw;
	}
	if (!std::filesystem::exists(argv[1]))
	{
		std::cerr << "File " << argv[1] << " does not exist!" << std::endl;
		throw;
	}
	std::ifstream infile(argv[1], std::ios::in);
	const std::vector<std::string> input {std::istream_iterator<std::string>{infile}, {}};
	return input;
}

int main(int argc, char* argv[])
{
	std::vector<std::string> input;
	try {
		input = load_input(argc, argv);
	} catch(...) {
		return 1;
	}
	auto p1 = numtrees(input, 3, 1);
	std::size_t p2 = 1;  // I originally used `auto` here and had an integer overflow problem!

	std::vector<std::pair<int, int>> slopes{{1,1}, {3,1}, {5,1}, {7,1}, {1,2}};
	for ( auto&& [h, v] : slopes )
	{
		auto n = numtrees(input, h, v);
		p2 *= n;
		std::cout << h << ", " << v << ": " << n << std::endl;
	}
	std::cout << "Part one: " << p1 << std::endl;
	std::cout << "Part two: " << p2 << std::endl;
	return 0;
}
