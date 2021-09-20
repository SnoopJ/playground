#include <string>
#include <unordered_map>
#include <utility>
#include <variant>


// these helpers are taken directly from https://en.cppreference.com/w/cpp/utility/variant/visit
#ifndef SWIG
// helper type for the visitor #4
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
// explicit deduction guide (not needed as of C++20)
template<class... Ts> overloaded(Ts...) -> overloaded<Ts...>;
#endif // SWIG

// A class with move-only semantics
class MoveOnlyFoo {
	public:
		int m_data;

		MoveOnlyFoo(int data) : m_data{data} {};

		MoveOnlyFoo(const MoveOnlyFoo& other) = delete;         // copy ctor
		MoveOnlyFoo& operator=(MoveOnlyFoo& other) = delete;    // copy assign
		MoveOnlyFoo(MoveOnlyFoo&& other) = default;             // move ctor
		MoveOnlyFoo& operator=(MoveOnlyFoo&& other) = default;  // move assign
};


using MoveOnlyMemberMap = std::unordered_map<std::string, MoveOnlyFoo>;
using CopyableMember = int;  // trivially copyable
using CopyableMemberMap = std::unordered_map<std::string, CopyableMember>;
using MemberMap = std::variant<CopyableMemberMap, MoveOnlyMemberMap>;

// A class that holds one of the possible member maps and is tricky to correctly wrap from SWIG
class Bar {
	public:

		Bar(MoveOnlyMemberMap&& m) : m_map{std::move(m)} { std::cout << "move map" << std::endl; };
		Bar(CopyableMemberMap& m) : m_map{m} { std::cout << "copy map" << std::endl; };

		// this ctor is is a convenient way to make a Bar with move-only members from Python
		Bar(std::string a, int b) {
			MoveOnlyMemberMap mp;
			mp.emplace(a, std::move(MoveOnlyFoo(b)));
			this->m_map = std::move(mp);
		}

		MemberMap m_map;

		// this is a deliberately poorly-written function which SWIG will try to
		// wrap by default, triggering generation of a copy ctor for MoveOnlyMemberMap
		MemberMap baz() {
			return std::move(m_map);
		}

#ifndef SWIG
		void print_members()
		{
			std::visit(overloaded {
					[] (CopyableMemberMap& mp) {for( const auto& [k, v]: mp ) {std::cout << k << ": " << v << std::endl;}},
					[] (MoveOnlyMemberMap& mp) {for( const auto& [k, v]: mp ) {std::cout << k << ": " << v.m_data << std::endl;}}
					}, m_map);
		}
#endif // SWIG
};
