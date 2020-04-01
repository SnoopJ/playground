class Foo {
    public:
	Foo(){};
	~Foo(){};
        
	int bar();
	int taco();  // we want to ignore this one
    private:
	int baz{42};
};
