#include <iostream>
#include <unordered_map>
#include "foo.hpp"

int main(int argv, char** argc)
{
	CopyableMemberMap cmp;
	cmp.emplace("taco", -1);
	cmp.emplace("cat", 1337);
	auto cb = Bar(cmp);
	cb.print_members();

	MoveOnlyMemberMap mmp;
	mmp.emplace("taco", MoveOnlyFoo{-1});
	mmp.emplace("cat", MoveOnlyFoo{1337});
	auto mb = Bar(std::move(mmp));
	mb.print_members();

    return 0;
}
