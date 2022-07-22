#include <stdexcept>
#include <utility>

namespace Acme
{
    constexpr auto kDigits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
    constexpr auto kHexDigits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"};
    constexpr auto kEyeColors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};

    std::size_t countChars(const std::string& s, std::vector<const char*> match)
    {
        std::size_t result = 0;
        for ( auto it = s.begin(); it != s.end(); it++ )
        {
            for ( auto t: match )
            {
                if ( *it == *t )
                {
                    result++;
                    break;
                }
            }
        }
        return result;
    }

    inline auto countDigits(const std::string& s) { return countChars(s, kDigits); }
    inline auto countHexDigits(const std::string& s) { return countChars(s, kHexDigits); }

    bool isDigits(const std::string& s)
    {
        return countDigits(s) == s.length();
    }

    bool isDigits(char& ipt)
    {
        const std::string s{ipt};
        return countDigits(s);
    }

    bool isDigits(const char* ipt)
    {
        const std::string s{ipt};
        return countDigits(s);
    }

    bool validHairColor(const std::string& s)
    {
        auto result = s.length() == 7 && s.at(0) == '#' && countHexDigits(s) == 6;
        if (!result) std::cerr << "Bad hair color " << s << std::endl;
        return result;
    }

    bool validEyeColor(const std::string& s)
    {
        for ( auto col: kEyeColors )
        {
            if ( s == col )
            {
                return true;
            }
        }
        std::cerr << "Bad eye color " << s << std::endl;
        return false;
    }

    inline bool validHeight(const std::string& s) { return validHeight(const_cast<std::string&>(s)); }

    bool validHeight(std::string& s)
    {
        std::string acc;
        std::string unit;
        for ( auto idx = 0; idx < s.length(); idx++ )
        {
            if ( isDigits(s.at(idx)) )
            {
                acc += s[idx];
            } else {
                unit = s.substr(idx);
                break;
            }
        }
        auto height = std::stoi(acc);
        if ((unit == "cm" && 150 <= height && height <= 193) ||
            (unit == "in" && 59  <= height && height <= 76 ))
        {
            return true;
        } else {
            std::cerr << "Bad height " << s << std::endl;
            return false;
        }
    }

    struct PassportInfo {
        static constexpr std::pair<int, int> kValidBirthYears{1920, 2002};
        static constexpr std::pair<int, int> kValidIssueYears{2010, 2020};
        static constexpr std::pair<int, int> kValidExpiryYears{2020, 2030};

        std::string byr = "";
        std::string iyr = "";
        std::string eyr = "";

        std::string hgt = "";
        std::string hcl = "";
        std::string ecl = "";

        std::string pid = "";
        std::string cid = "";

        void set(const std::string& member, const std::string value)
        {
//             std::cout << "Setting member " << member << "with value " << value << std::endl;
            if (member == "byr") byr = value;
            else if (member == "iyr") iyr = value;
            else if (member == "eyr") eyr = value;

            else if (member == "hgt") hgt = value;
            else if (member == "hcl") hcl = value;
            else if (member == "ecl") ecl = value;

            else if (member == "pid") pid = value;
            else if (member == "cid") cid = value;
            else throw std::invalid_argument("Unknown passport field" + member);
        }

        template<typename T>
        bool between(T val, int min, int max)
        {
            return min <= val && val <= max;
        }

        bool validDates()
        {
            for ( auto val: {byr, iyr, eyr} )
            {
                if ( !isDigits(val) )
                {
                    return false;
                }

            }
            auto b = std::stoi(byr);
            auto i = std::stoi(iyr);
            auto e = std::stoi(eyr);

            bool dateOK = between(b, 1920, 2002) &&
                          between(i, 2010, 2020) &&
                          between(e, 2020, 2030);

            return dateOK;
        }

        bool validID()
        {
            bool idOK = (pid.length() == 9 && countDigits(pid) == 9);
            return idOK;
        }

        bool validPersonInfo()
        {
            bool persinfoOK = validHairColor(hcl) && validEyeColor(ecl) && validHeight(hgt);
            return persinfoOK;
        }

        std::string
        dump()
        {
            std::string descr;
            descr += "byr=" + byr + ", ";
            descr += "iyr=" + iyr + ", ";
            descr += "eyr=" + eyr + ", ";

            descr += "hgt=" + hgt + ", ";
            descr += "hcl=" + hcl + ", ";
            descr += "ecl=" + ecl + ", ";

            descr += "pid=" + pid + ", ";
            descr += "cid=" + cid + ", ";

            return descr;
        }

        inline bool allParams()
        {
            auto allpresent = !byr.empty() && !iyr.empty() && !eyr.empty() &&
                              !hcl.empty() && !ecl.empty() && !hgt.empty() &&
                              !pid.empty();  // we don't care if cid is present
//             if (!allpresent) std::cout << "Parameters missing!" << std::endl << dump() << std::endl;
            return allpresent;
        }

        inline bool valid()
        {
            auto allpresent = allParams();
            if (!allpresent)
            {
                return false;
            }

            auto paramsvalid = validID() && validDates() && validPersonInfo();
//             if (!paramsvalid) std::cout << "Invalid passport" << std::endl << dump() << std::endl;
            return paramsvalid;
        }

    };

    std::pair<const std::string, const std::string>
    getPair(const std::string& token)
    {
        auto colonidx = token.find(":");
        auto key = token.substr(0, colonidx);
        auto value = token.substr(colonidx+1);
//         std::cout << "\tkey " << key << "=" << value << std::endl; 

        return {key, value};
    }

    std::vector<Acme::PassportInfo>
    parseInfo(std::vector<std::string>& document, bool validate = false)
    {
        std::vector<Acme::PassportInfo> result;

        Acme::PassportInfo acc;
        for(const std::string& line : document)
        {
//             std::cout << "line: " << line << std::endl;
            if (line.empty())
            {
//                 std::cout << "Emplacing: " << acc.dump() << std::endl;
                result.emplace_back(std::move(acc));
                continue;
            }

            auto L = 0;
            auto R = line.find(" ");
            auto it = 0;


            while (R != line.npos)
            {
                auto subs = line.substr(L, R-L);
                auto [key, value] = getPair(subs);
                acc.set(key, value);

                L = R;
                R = line.find(" ", L+1);
            }
            if (L != R)
            {
                auto subs = line.substr(L);
                auto [key, value] = getPair(subs);
                acc.set(key, value);
            }
        }

        // emplace the last one
        result.emplace_back(std::move(acc));

        return result;
    }
}; // namespace Acme
