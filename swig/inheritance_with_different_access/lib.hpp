class Foo {
    public:
		Foo() : m_data(-1) {};
		Foo(int val) : m_data(val) {};

		// this public member will be visible in SWIG's derived class
		int get_data() {
			return m_data;
		}
	protected:
		int m_data;

		// the SWIG derived class will shadow this with a public member
		void set_data(int& val) {
            std::cout << "Inside base setter\n";
			m_data = val;
		}
};
