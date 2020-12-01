#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int main()
{
	std::ifstream infile("input.txt", std::ios::in);
	std::string line;
	std::vector<int> nums;
	while (std::getline(infile, line))
	{
		nums.emplace_back(std::stoi(line));
	}
	for (auto it = nums.begin(); it != nums.end(); it++)
	{
		int first = *it;
		for (auto it2 = it+1; it2 != nums.end(); it2++)
		{
			int second = *it2;
			if (first+second == 2020)
			{
				std::cout << "Part one:" << std::endl;
				std::cout << first*second << std::endl;
			}
		}
	}


	for (auto it = nums.begin(); it != nums.end(); it++)
	{
		int first = *it;
		for (auto it2 = it+1; it2 != nums.end(); it2++)
		{
			int second = *it2;
			for (auto it3 = it2+1; it3 != nums.end(); it3++)
			{
				int third = *it3;
				if (first+second+third == 2020)
				{
					std::cout << "Part two:" << std::endl;
					std::cout << first*second*third << std::endl;
				}
			}
		}
	}
	return 0;
}

