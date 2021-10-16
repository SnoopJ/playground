#include <random>
#include <vector>


std::vector<std::size_t> shared_vec;


std::vector<std::size_t>* _randvec(int N)
{
    std::mt19937 rand;
    rand.seed(20071969);

    for (int idx = 0; idx <= N; idx++)
    {
        shared_vec.push_back(rand());
    }

    return &shared_vec;
}

extern "C" void* randvec(int N) { return _randvec(N); }
