#include <algorithm>
#include <bitset>
#include <iostream>
#include <set>
#include <string>
#include <vector>

#include "common.h"

template <std::size_t len, const char one, const char zero>
int
parseValue(std::string& line, std::size_t offset = 0)
{
    std::bitset<len> bits;
    for ( int idx = 0; idx < len; idx++ )
    {
        bits.set(len-1 - idx, line[idx+offset] == one ? true : false);
        for ( int j = 0; j < idx; j++ )
        {
            std::cout << " ";
        }
        std::cout << "v" << "\t";
        for ( int j = 0; j < idx; j++ )
        {
            std::cout << " ";
        }
        std::cout << "v" << std::endl;
        std::cout << bits << "\t" << line.substr(offset, len) << std::endl;
    }

    return bits.to_ulong();
}

int
main(int argc, char* argv[])
{
	std::vector<std::string> input;
	try {
		input = Acme::load_input(argc, argv);
	} catch(...) {
		return 1;
	}

    std::vector<int> rows;
    std::vector<int> cols;
    for ( auto& line: input )
    {
        if (line.empty()) { continue; }

        std::cout << "PASS: \t" << line << std::endl;

        int row = parseValue<7, 'B', 'F'>(line);
        rows.emplace_back(row);
        std::cout << "---row: " << rows.back() << "--------" << std::endl;

        int col = parseValue<3, 'R', 'L'>(line, 7);
        cols.emplace_back(col);
        std::cout << "---col: " << cols.back() << "--------" << std::endl;

        std::cout << std::endl;
    }

    std::set<int> seatIDs;
    for ( auto rit = rows.begin(), cit = cols.begin(); rit != rows.end() && cit != cols.end(); rit++, cit++ )
    {
        std::size_t seatID = (*rit) * 8 + (*cit);
        seatIDs.emplace(std::move(seatID));
    }

    auto maxSeatID = std::max_element(seatIDs.begin(), seatIDs.end());
    std::cout << "Max Seat ID: " << *maxSeatID << std::endl;

    std::set<int> possibleSeatIDs;
    for ( int i = 0; i < *maxSeatID; i++ )
    {
        possibleSeatIDs.insert(i);
    }

    std::vector<int> diffs;

    std::set_difference(possibleSeatIDs.begin(), possibleSeatIDs.end(),
                        seatIDs.begin(), seatIDs.end(),
                        std::back_inserter(diffs));

    for ( int i = 1, tmp = 0; i < diffs.size(); tmp = diffs[i], i++ )
    {
        if (diffs[i] - tmp != 1)
        { 
            std::cout << "Nonsequential missing seat: " << diffs[i] << std::endl;
        }
    }

	return 0;
}
