#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <set>
#include <string>
#include <vector>

#include "common.h"

namespace Acme {
    using Questions = std::set<char>;

    std::string
    dump(Questions q)
    {
        std::string repr = "{";
        auto qspace = q.size() > 0 ? q.size() + (q.size()-1) : 0;
        repr.reserve(qspace + 2); // space for 2 braces + chars + interleaved commas
        for ( char c: q )
        {
            repr.push_back(c);
            repr.push_back(',');
        }

        if (repr.size() > 1)
        {
            // remove trailing comma, if there is one
            repr.pop_back(); 
        }
        repr.push_back('}');

        return repr;
    }

    Questions
    parseLine(std::string& line)
    {
        Questions acc;
        for ( char c: line )
        {
            acc.emplace(c);
        }
        return acc;
    }

    std::vector<Questions>
    partOne(std::vector<std::string> input)
    {
        Questions qacc;
        std::vector<Questions> group_questions;

        int grpnum = 1;
        for ( auto& line: input )
        {
            if (line.empty()) {
                group_questions.push_back(qacc);
                qacc.clear();

                grpnum++;
                continue;
            } else {
                qacc.merge(parseLine(line));
            }
        }
        if (!qacc.empty())
        {
            group_questions.push_back(qacc);
        }

        return group_questions;
    }

    std::vector<Questions>
    partTwo(std::vector<std::string> input)
    {
        Questions qacc;
        std::vector<Questions> group_questions;
        int grpnum = 1;
        
        bool isFirst = true;
        for ( auto& line: input )
        {
            if (line.empty()) {
                group_questions.emplace_back(qacc);
                qacc.clear();
                isFirst = true;
                continue;
            } else {
                if (isFirst) // first line of a group, consume all chars
                {
                    qacc = parseLine(line);
                    std::cout << "New group, starting from: " << dump(qacc) << std::endl;
                    isFirst = false;
                } else {  // non-first line of a group, consume only intersection
                    auto tmp = parseLine(line);
                    Questions result;
                    std::set_intersection(qacc.begin(), qacc.end(),
                                          tmp.begin(), tmp.end(),
                                          std::inserter(result, result.begin()));
                    qacc = result;
                    std::cout << "\tUpdated (" << line << "), running intersection: " << dump(qacc) << std::endl;
                }
            }
        }
        if (!qacc.empty())
        {
            group_questions.push_back(qacc);
        }

        return group_questions;
    }

    int
    countQuestions(std::vector<Questions>& qs)
    {
        auto sum = 0;
        for ( auto& q: qs )
        {
            sum += q.size();
        }

        return sum;
    }
} // Acme


int
main(int argc, char* argv[])
{
	std::vector<std::string> input;
	try {
		input = Acme::load_input(argc, argv);
	} catch(...) {
		return 1;
	}


    std::vector<Acme::Questions> p1 = Acme::partOne(input);
    auto p1sum = Acme::countQuestions(p1);
    std::cout << "Part one: " << p1sum << std::endl;

    std::vector<Acme::Questions> p2 = Acme::partTwo(input);
    auto p2sum = Acme::countQuestions(p2);
    std::cout << "Part two: " << p2sum << std::endl;

	return 0;
}
