class Foo {
    public:
	Foo(int val) : value(val) {}
        int bar();
	int value;
};

bool munge(Foo& f, int x);
