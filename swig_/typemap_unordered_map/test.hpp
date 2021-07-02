#include <unordered_map>
#include <vector>

struct MyObj {
    int x = 42;
    int y = -1;
};

std::vector<int> do_the_thing(); 
std::unordered_map<std::string, int> foo_the_thing();
std::unordered_map<std::string, MyObj> umap_myobj();

int foo();

