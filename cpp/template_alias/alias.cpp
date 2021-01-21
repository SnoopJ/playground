#include <iostream>

enum class EColor 
{
    red = 0,
    blue,
    green
};

enum class EFlavor
{
    umami = 0,
    sweet,
    sour
};

template<EColor T, int U, EFlavor V>
class Treat {
    public:
        EColor m_color = T;
        EFlavor m_flavor = V;
};

template<EColor T, int U>
using Umami = Treat<T, U, EFlavor::umami>;

int main(int argc, char** argv)
{
    std::cout << "Color: " << static_cast<int>(Umami<EColor::green, 42>().m_color) << std::endl;
    std::cout << "Flavor: " << static_cast<int>(Umami<EColor::green, 42>().m_flavor)  << std::endl;
    std::cout << std::endl;

    std::cout << "Color: " << static_cast<int>(Treat<EColor::blue, 42, EFlavor::umami>().m_color) << std::endl;
    std::cout << "Flavor: " << static_cast<int>(Treat<EColor::blue, 42, EFlavor::umami>().m_flavor)  << std::endl;
    std::cout << std::endl;

    return 0;
}
