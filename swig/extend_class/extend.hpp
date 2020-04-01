#include <unordered_map>

using MyMap = std::unordered_map<std::string, int>;

class Foo {
    public:
	Foo(){};
	~Foo(){};
        MyMap* get_bar();
    private:
    MyMap m_mymap{{"foo", 42}};
};
