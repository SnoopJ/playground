class Foo {
    public:
		Foo(){};
		~Foo(){};

		// this public member will be visible in SWIG's derived class
		int get_data() {
			return m_data;
		}
	protected:
		int m_data = -1;

		// the SWIG derived class will shadow this with a public member
		void set_data(int& val) {
            std::cout << "Inside base setter\n";
			m_data = val;
		}
};
