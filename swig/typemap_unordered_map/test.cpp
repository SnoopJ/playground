#include "test.hpp"
#include <iostream>
#include <unordered_map>
#include <vector>

int foo() {
    return 5;
}

std::vector<int> do_the_thing() {
    return std::vector<int>{1,2,3};
}

std::unordered_map<std::string, int> foo_the_thing() {
    return std::unordered_map<std::string, int>{
        {"foo", 1},
        {"bar", 2},
        {"baz", 3}
    };
}

std::unordered_map<std::string, MyObj> umap_myobj() {
    MyObj o;
    return std::unordered_map<std::string, MyObj>{
        {"foo", o},
        {"bar", o},
        {"baz", o}
    };
}


int main(int argc, char** argv) {
    auto m = do_the_thing();
    for ( auto& val : m ) {
        std::cout << val << "\n";
    }
    return 0;
}
