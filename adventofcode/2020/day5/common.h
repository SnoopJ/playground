#include <fstream>
#include <filesystem>
#include <iostream>
#include <string>
#include <vector>


namespace Acme {
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
        std::vector<std::string> input;
        std::string line;
        while (std::getline(infile, line))
        {
            input.push_back(std::move(line));
        }
        return input;
    }
} // namespace Acme
