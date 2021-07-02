#include <iostream>
#include <chrono>

std::chrono::steady_clock::time_point get_time() {
    return std::chrono::steady_clock::now();
}

int main(int argc, char** argv)
{
    auto start = get_time();

    std::cout << "Hello, I'm going to print out some stars I guess\n";
    for(int i=0; i<1000; i++) {
        std::cout << "*";
    }
    std::cout << "\n\n";

    auto end = get_time();

    auto dt = end - start;
    auto dtsec = std::chrono::duration_cast<std::chrono::seconds>(dt);
    double conv = std::chrono::steady_clock::duration::period::num*1.0 / std::chrono::steady_clock::duration::period::den;

    std::cout << "That took " << dt.count() << " ticks\n";
    std::cout << "That took " << dt.count() * conv << " seconds\n";
}
